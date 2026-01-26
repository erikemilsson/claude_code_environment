#!/usr/bin/env python3
"""
Trend Analyzer for Historical Analysis

Provides comprehensive trend analysis, anomaly detection, and insights
generation from historical monitoring data.
"""

import json
import statistics
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque

# Import history manager for data access
try:
    from history_manager import HistoryManager
except ImportError:
    HistoryManager = None


class TrendType(Enum):
    """Types of trends detected"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"
    SEASONAL = "seasonal"
    ANOMALY = "anomaly"


class TimeWindow(Enum):
    """Standard time windows for analysis"""
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"


@dataclass
class TrendAnalysis:
    """Represents a trend analysis result"""
    metric_name: str
    trend_type: TrendType
    slope: float  # Rate of change
    confidence: float  # 0.0 to 1.0
    start_value: float
    end_value: float
    average: float
    std_dev: float
    anomalies: List[Dict[str, Any]]
    seasonal_pattern: Optional[str]
    forecast_next_hour: Optional[float]
    insights: List[str]


@dataclass
class AnomalyScore:
    """Represents an anomaly detection result"""
    timestamp: datetime
    metric_name: str
    value: float
    expected: float
    z_score: float
    severity: str  # low, medium, high
    description: str


class TrendAnalyzer:
    """Comprehensive trend analysis system"""

    def __init__(self, history_path: Path = None):
        """Initialize the trend analyzer.

        Args:
            history_path: Path to historical data storage
        """
        if history_path is None:
            history_path = Path(__file__).parent.parent / "history"

        self.history_path = history_path
        self.history_manager = HistoryManager(history_path) if HistoryManager else None

        # Analysis parameters
        self.anomaly_z_threshold = 3.0  # Standard deviations for anomaly
        self.trend_min_samples = 10  # Minimum samples for trend detection
        self.seasonal_min_periods = 3  # Minimum periods for seasonal detection

        # Cache for analysis results
        self.analysis_cache = {}
        self.cache_ttl = 300  # 5 minutes

    def analyze_metric(self, metric_name: str, window: TimeWindow) -> TrendAnalysis:
        """Perform comprehensive analysis on a specific metric.

        Args:
            metric_name: Name of the metric to analyze
            window: Time window for analysis

        Returns:
            TrendAnalysis object with complete analysis
        """
        # Get historical data
        data = self._get_metric_data(metric_name, window)

        if len(data) < self.trend_min_samples:
            return self._create_insufficient_data_analysis(metric_name)

        # Extract values and timestamps
        values = [d['value'] for d in data]
        timestamps = [datetime.fromisoformat(d['timestamp']) for d in data]

        # Basic statistics
        avg = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0

        # Detect trend type and slope
        trend_type, slope = self._detect_trend(values, timestamps)

        # Detect anomalies
        anomalies = self._detect_anomalies(values, timestamps, avg, std_dev)

        # Check for seasonal patterns
        seasonal_pattern = self._detect_seasonal_pattern(values, timestamps)

        # Generate forecast
        forecast = self._forecast_next_value(values, slope, seasonal_pattern)

        # Generate insights
        insights = self._generate_insights(
            metric_name, trend_type, slope, anomalies,
            seasonal_pattern, values, avg
        )

        return TrendAnalysis(
            metric_name=metric_name,
            trend_type=trend_type,
            slope=slope,
            confidence=self._calculate_confidence(values, trend_type),
            start_value=values[0] if values else 0,
            end_value=values[-1] if values else 0,
            average=avg,
            std_dev=std_dev,
            anomalies=anomalies,
            seasonal_pattern=seasonal_pattern,
            forecast_next_hour=forecast,
            insights=insights
        )

    def _get_metric_data(self, metric_name: str, window: TimeWindow) -> List[Dict]:
        """Retrieve metric data for the specified window.

        Args:
            metric_name: Name of the metric
            window: Time window

        Returns:
            List of metric data points
        """
        if not self.history_manager:
            # Generate mock data for testing
            return self._generate_mock_data(metric_name, window)

        # Convert window to minutes
        window_minutes = {
            TimeWindow.HOUR: 60,
            TimeWindow.DAY: 1440,
            TimeWindow.WEEK: 10080,
            TimeWindow.MONTH: 43200
        }[window]

        # Get recent metrics
        metrics = self.history_manager.get_recent_metrics(
            minutes=window_minutes,
            metric_names=[metric_name]
        )

        # Extract the specific metric
        result = []
        for entry in metrics:
            if metric_name in entry.get('data', {}):
                result.append({
                    'timestamp': entry['timestamp'],
                    'value': entry['data'][metric_name]
                })

        return result

    def _detect_trend(self, values: List[float], timestamps: List[datetime]) -> Tuple[TrendType, float]:
        """Detect the trend type and calculate slope.

        Args:
            values: Metric values
            timestamps: Corresponding timestamps

        Returns:
            Tuple of (TrendType, slope)
        """
        if len(values) < 2:
            return TrendType.STABLE, 0.0

        # Convert timestamps to numeric (seconds from first)
        time_numeric = [(t - timestamps[0]).total_seconds() for t in timestamps]

        # Calculate linear regression
        n = len(values)
        sum_x = sum(time_numeric)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(time_numeric, values))
        sum_x2 = sum(x * x for x in time_numeric)

        # Calculate slope
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            slope = 0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / denominator

        # Convert slope to rate per hour
        slope_per_hour = slope * 3600 if time_numeric[-1] > 0 else 0

        # Calculate R-squared for confidence
        if statistics.stdev(values) > 0:
            # Calculate predicted values
            intercept = (sum_y - slope * sum_x) / n
            predicted = [slope * x + intercept for x in time_numeric]

            # Calculate R-squared
            ss_res = sum((y - pred) ** 2 for y, pred in zip(values, predicted))
            ss_tot = sum((y - statistics.mean(values)) ** 2 for y in values)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        else:
            r_squared = 1.0

        # Check for volatility
        avg = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        cv = std_dev / avg if avg != 0 else 0  # Coefficient of variation

        # Determine trend type
        if cv > 0.5:  # High volatility
            return TrendType.VOLATILE, slope_per_hour
        elif abs(slope_per_hour) < 0.01 and r_squared < 0.1:
            return TrendType.STABLE, 0.0
        elif slope_per_hour > 0 and r_squared > 0.3:
            return TrendType.INCREASING, slope_per_hour
        elif slope_per_hour < 0 and r_squared > 0.3:
            return TrendType.DECREASING, slope_per_hour
        else:
            return TrendType.STABLE, slope_per_hour

    def _detect_anomalies(self, values: List[float], timestamps: List[datetime],
                         mean: float, std_dev: float) -> List[Dict[str, Any]]:
        """Detect anomalies using statistical methods.

        Args:
            values: Metric values
            timestamps: Corresponding timestamps
            mean: Mean value
            std_dev: Standard deviation

        Returns:
            List of detected anomalies
        """
        if std_dev == 0 or len(values) < 3:
            return []

        anomalies = []

        # Use z-score method
        for i, (value, timestamp) in enumerate(zip(values, timestamps)):
            z_score = abs((value - mean) / std_dev)

            if z_score > self.anomaly_z_threshold:
                severity = "low" if z_score < 4 else "medium" if z_score < 5 else "high"

                anomalies.append({
                    'timestamp': timestamp.isoformat(),
                    'value': value,
                    'expected': mean,
                    'z_score': z_score,
                    'severity': severity,
                    'description': f"Value {value:.2f} is {z_score:.1f} standard deviations from mean"
                })

        # Use IQR method for additional detection
        if len(values) >= 4:
            q1 = statistics.quantiles(values, n=4)[0]
            q3 = statistics.quantiles(values, n=4)[2]
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            for i, (value, timestamp) in enumerate(zip(values, timestamps)):
                if value < lower_bound or value > upper_bound:
                    # Check if not already detected
                    if not any(a['timestamp'] == timestamp.isoformat() for a in anomalies):
                        anomalies.append({
                            'timestamp': timestamp.isoformat(),
                            'value': value,
                            'expected': (q1 + q3) / 2,
                            'z_score': 0,  # Not calculated for IQR method
                            'severity': "medium",
                            'description': f"Value {value:.2f} outside IQR bounds [{lower_bound:.2f}, {upper_bound:.2f}]"
                        })

        return sorted(anomalies, key=lambda x: x['timestamp'])

    def _detect_seasonal_pattern(self, values: List[float], timestamps: List[datetime]) -> Optional[str]:
        """Detect seasonal patterns in the data.

        Args:
            values: Metric values
            timestamps: Corresponding timestamps

        Returns:
            Description of seasonal pattern if detected
        """
        if len(values) < 24:  # Need at least 24 hours of data
            return None

        # Check for hourly patterns (24-hour cycle)
        hourly_buckets = defaultdict(list)
        for value, timestamp in zip(values, timestamps):
            hour = timestamp.hour
            hourly_buckets[hour].append(value)

        # Calculate variance between hours
        if len(hourly_buckets) >= 12:  # At least half the hours represented
            hourly_avgs = {h: statistics.mean(vals) for h, vals in hourly_buckets.items()}

            if hourly_avgs:
                max_hour = max(hourly_avgs.items(), key=lambda x: x[1])
                min_hour = min(hourly_avgs.items(), key=lambda x: x[1])

                overall_avg = statistics.mean(hourly_avgs.values())
                variation = (max_hour[1] - min_hour[1]) / overall_avg if overall_avg > 0 else 0

                if variation > 0.3:  # Significant variation
                    return f"Daily pattern: Peak at {max_hour[0]:02d}:00 ({max_hour[1]:.1f}), Low at {min_hour[0]:02d}:00 ({min_hour[1]:.1f})"

        # Check for weekly patterns if enough data
        if len(values) >= 168:  # At least a week of hourly data
            daily_buckets = defaultdict(list)
            for value, timestamp in zip(values, timestamps):
                weekday = timestamp.weekday()
                daily_buckets[weekday].append(value)

            if len(daily_buckets) >= 5:  # Most weekdays represented
                daily_avgs = {d: statistics.mean(vals) for d, vals in daily_buckets.items()}

                weekday_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                max_day = max(daily_avgs.items(), key=lambda x: x[1])
                min_day = min(daily_avgs.items(), key=lambda x: x[1])

                overall_avg = statistics.mean(daily_avgs.values())
                variation = (max_day[1] - min_day[1]) / overall_avg if overall_avg > 0 else 0

                if variation > 0.2:  # Significant weekly variation
                    return f"Weekly pattern: Peak on {weekday_names[max_day[0]]} ({max_day[1]:.1f}), Low on {weekday_names[min_day[0]]} ({min_day[1]:.1f})"

        return None

    def _forecast_next_value(self, values: List[float], slope: float,
                             seasonal_pattern: Optional[str]) -> Optional[float]:
        """Forecast the next value based on trend and patterns.

        Args:
            values: Historical values
            slope: Trend slope
            seasonal_pattern: Detected seasonal pattern

        Returns:
            Forecasted value for next hour
        """
        if len(values) < 3:
            return None

        # Simple forecast: last value + hourly slope
        base_forecast = values[-1] + slope

        # Apply moving average smoothing
        if len(values) >= 5:
            recent_avg = statistics.mean(values[-5:])
            # Weighted combination
            base_forecast = 0.7 * base_forecast + 0.3 * recent_avg

        # Apply seasonal adjustment if pattern detected
        if seasonal_pattern and "Daily pattern" in seasonal_pattern:
            # Simple seasonal adjustment (would be more sophisticated in production)
            current_hour = datetime.now().hour
            next_hour = (current_hour + 1) % 24

            # Extract peak hour from pattern string
            if "Peak at" in seasonal_pattern:
                peak_hour = int(seasonal_pattern.split("Peak at ")[1].split(":")[0])
                distance_to_peak = min(abs(next_hour - peak_hour), 24 - abs(next_hour - peak_hour))

                # Adjust forecast based on distance to peak
                seasonal_factor = 1.0 + (0.1 * math.cos(distance_to_peak * math.pi / 12))
                base_forecast *= seasonal_factor

        return max(0, base_forecast)  # Ensure non-negative

    def _calculate_confidence(self, values: List[float], trend_type: TrendType) -> float:
        """Calculate confidence score for the trend analysis.

        Args:
            values: Metric values
            trend_type: Detected trend type

        Returns:
            Confidence score between 0 and 1
        """
        if len(values) < self.trend_min_samples:
            return 0.3

        # Base confidence on sample size
        sample_confidence = min(1.0, len(values) / 100)

        # Adjust based on trend type
        if trend_type == TrendType.VOLATILE:
            confidence = sample_confidence * 0.5
        elif trend_type == TrendType.STABLE:
            confidence = sample_confidence * 0.9
        else:
            confidence = sample_confidence * 0.7

        return min(1.0, confidence)

    def _generate_insights(self, metric_name: str, trend_type: TrendType,
                          slope: float, anomalies: List[Dict],
                          seasonal_pattern: Optional[str],
                          values: List[float], avg: float) -> List[str]:
        """Generate actionable insights from the analysis.

        Args:
            Various analysis results

        Returns:
            List of insight strings
        """
        insights = []

        # Trend insights
        if trend_type == TrendType.INCREASING:
            rate = abs(slope)
            if metric_name in ['memory_usage', 'cpu_usage']:
                hours_to_limit = (100 - values[-1]) / rate if rate > 0 else float('inf')
                if hours_to_limit < 24:
                    insights.append(f"⚠️ {metric_name} will reach critical levels in {hours_to_limit:.1f} hours at current rate")
                else:
                    insights.append(f"📈 {metric_name} increasing at {rate:.1f}% per hour")
        elif trend_type == TrendType.DECREASING:
            insights.append(f"📉 {metric_name} improving, decreasing at {abs(slope):.1f}% per hour")
        elif trend_type == TrendType.VOLATILE:
            insights.append(f"⚡ High volatility detected in {metric_name}, consider investigation")
        elif trend_type == TrendType.STABLE:
            insights.append(f"✅ {metric_name} is stable at {avg:.1f}")

        # Anomaly insights
        if anomalies:
            recent_anomalies = [a for a in anomalies if
                               (datetime.now() - datetime.fromisoformat(a['timestamp'])).total_seconds() < 3600]
            if recent_anomalies:
                insights.append(f"🔍 {len(recent_anomalies)} anomalies detected in the last hour")

            high_severity = [a for a in anomalies if a['severity'] == 'high']
            if high_severity:
                insights.append(f"🚨 {len(high_severity)} high-severity anomalies require attention")

        # Seasonal insights
        if seasonal_pattern:
            insights.append(f"📅 {seasonal_pattern}")

        # Performance insights
        if metric_name == 'memory_usage' and avg > 70:
            insights.append("💡 Consider memory optimization or scaling")
        elif metric_name == 'cpu_usage' and avg > 60:
            insights.append("💡 CPU usage elevated, review resource-intensive operations")
        elif metric_name == 'error_rate' and avg > 2:
            insights.append("💡 Error rate above normal, investigate root causes")
        elif metric_name == 'task_queue' and trend_type == TrendType.INCREASING:
            insights.append("💡 Task queue growing, consider scaling workers")

        # Capacity planning
        if metric_name in ['memory_usage', 'cpu_usage', 'disk_usage']:
            if values[-1] > 80:
                insights.append(f"⛔ {metric_name} at {values[-1]:.1f}%, immediate action needed")
            elif values[-1] > 70:
                insights.append(f"⚠️ {metric_name} at {values[-1]:.1f}%, plan for scaling")

        return insights

    def _create_insufficient_data_analysis(self, metric_name: str) -> TrendAnalysis:
        """Create analysis result when insufficient data is available.

        Args:
            metric_name: Name of the metric

        Returns:
            TrendAnalysis with limited information
        """
        return TrendAnalysis(
            metric_name=metric_name,
            trend_type=TrendType.STABLE,
            slope=0.0,
            confidence=0.1,
            start_value=0,
            end_value=0,
            average=0,
            std_dev=0,
            anomalies=[],
            seasonal_pattern=None,
            forecast_next_hour=None,
            insights=["Insufficient data for trend analysis (minimum 10 samples required)"]
        )

    def _generate_mock_data(self, metric_name: str, window: TimeWindow) -> List[Dict]:
        """Generate mock data for testing.

        Args:
            metric_name: Name of the metric
            window: Time window

        Returns:
            Mock metric data
        """
        import random

        # Determine number of samples based on window
        samples = {
            TimeWindow.HOUR: 12,  # 5-minute samples
            TimeWindow.DAY: 24,   # Hourly samples
            TimeWindow.WEEK: 168,  # Hourly samples
            TimeWindow.MONTH: 720  # Hourly samples
        }[window]

        now = datetime.now()
        data = []

        # Generate realistic patterns based on metric type
        base_values = {
            'memory_usage': 65,
            'cpu_usage': 40,
            'error_rate': 1.5,
            'task_queue': 5,
            'response_time': 50
        }

        base = base_values.get(metric_name, 50)

        for i in range(samples):
            # Add some trends and patterns
            trend = i * 0.1 if metric_name == 'memory_usage' else 0
            seasonal = 10 * math.sin(i * 2 * math.pi / 24) if window in [TimeWindow.DAY, TimeWindow.WEEK] else 0
            noise = random.gauss(0, base * 0.1)

            value = base + trend + seasonal + noise
            value = max(0, value)  # Ensure non-negative

            timestamp = now - timedelta(hours=samples-i)

            data.append({
                'timestamp': timestamp.isoformat(),
                'value': value
            })

        return data

    def generate_trend_report(self, metrics: List[str] = None) -> str:
        """Generate a comprehensive trend report.

        Args:
            metrics: List of metrics to analyze (None for all)

        Returns:
            Formatted trend report in markdown
        """
        if metrics is None:
            metrics = ['memory_usage', 'cpu_usage', 'error_rate', 'task_queue', 'response_time']

        report = "# 📊 Historical Trend Analysis Report\n\n"
        report += f"**Generated:** {datetime.now().isoformat()}\n\n"

        # Analyze each metric for different time windows
        for metric in metrics:
            report += f"## {metric.replace('_', ' ').title()}\n\n"

            for window in [TimeWindow.HOUR, TimeWindow.DAY, TimeWindow.WEEK]:
                analysis = self.analyze_metric(metric, window)

                report += f"### {window.value} Analysis\n"
                report += f"- **Trend:** {analysis.trend_type.value.title()}\n"
                report += f"- **Current:** {analysis.end_value:.2f}\n"
                report += f"- **Average:** {analysis.average:.2f} ± {analysis.std_dev:.2f}\n"

                if analysis.slope != 0:
                    report += f"- **Rate of Change:** {analysis.slope:+.2f} per hour\n"

                if analysis.forecast_next_hour:
                    report += f"- **1-Hour Forecast:** {analysis.forecast_next_hour:.2f}\n"

                if analysis.seasonal_pattern:
                    report += f"- **Pattern:** {analysis.seasonal_pattern}\n"

                if analysis.anomalies:
                    report += f"- **Anomalies:** {len(analysis.anomalies)} detected\n"

                report += f"- **Confidence:** {analysis.confidence*100:.0f}%\n"

                # Add insights
                if analysis.insights:
                    report += "\n**Insights:**\n"
                    for insight in analysis.insights[:3]:  # Top 3 insights
                        report += f"- {insight}\n"

                report += "\n"

            report += "---\n\n"

        # Add summary section
        report += "## Executive Summary\n\n"
        report += self._generate_executive_summary(metrics)

        return report

    def _generate_executive_summary(self, metrics: List[str]) -> str:
        """Generate executive summary of all trends.

        Args:
            metrics: List of analyzed metrics

        Returns:
            Executive summary text
        """
        summary = ""
        critical_issues = []
        warnings = []
        positive_trends = []

        # Analyze each metric for the day window
        for metric in metrics:
            analysis = self.analyze_metric(metric, TimeWindow.DAY)

            # Check for critical issues
            if metric in ['memory_usage', 'cpu_usage'] and analysis.end_value > 80:
                critical_issues.append(f"{metric}: {analysis.end_value:.1f}%")
            elif metric == 'error_rate' and analysis.end_value > 5:
                critical_issues.append(f"error_rate: {analysis.end_value:.1f}%")

            # Check for warnings
            if analysis.trend_type == TrendType.INCREASING and metric in ['memory_usage', 'cpu_usage', 'error_rate']:
                warnings.append(f"{metric} increasing at {analysis.slope:.1f}% per hour")
            elif analysis.trend_type == TrendType.VOLATILE:
                warnings.append(f"{metric} showing high volatility")

            # Check for positive trends
            if analysis.trend_type == TrendType.DECREASING and metric in ['memory_usage', 'cpu_usage', 'error_rate']:
                positive_trends.append(f"{metric} improving")
            elif analysis.trend_type == TrendType.STABLE and analysis.end_value < 50:
                positive_trends.append(f"{metric} stable and healthy")

        # Build summary
        if critical_issues:
            summary += "🚨 **CRITICAL ISSUES:**\n"
            for issue in critical_issues:
                summary += f"- {issue}\n"
            summary += "\n"

        if warnings:
            summary += "⚠️ **WARNINGS:**\n"
            for warning in warnings:
                summary += f"- {warning}\n"
            summary += "\n"

        if positive_trends:
            summary += "✅ **POSITIVE TRENDS:**\n"
            for trend in positive_trends:
                summary += f"- {trend}\n"
            summary += "\n"

        if not critical_issues and not warnings:
            summary += "✅ **System Status:** All metrics within normal parameters\n"

        return summary


def main():
    """Main entry point for testing"""
    analyzer = TrendAnalyzer()

    print("Trend Analysis System")
    print("=" * 50)

    # Generate and print trend report
    report = analyzer.generate_trend_report()
    print(report)

    # Analyze specific metric
    print("\nDetailed Analysis: Memory Usage (24h)")
    print("-" * 40)

    analysis = analyzer.analyze_metric('memory_usage', TimeWindow.DAY)

    print(f"Trend Type: {analysis.trend_type.value}")
    print(f"Current Value: {analysis.end_value:.2f}")
    print(f"Average: {analysis.average:.2f}")
    print(f"Slope: {analysis.slope:+.2f} per hour")
    print(f"Forecast (1h): {analysis.forecast_next_hour:.2f}" if analysis.forecast_next_hour else "Forecast: N/A")
    print(f"Anomalies: {len(analysis.anomalies)}")
    print(f"Confidence: {analysis.confidence*100:.0f}%")

    print("\nInsights:")
    for insight in analysis.insights:
        print(f"  • {insight}")


if __name__ == "__main__":
    main()