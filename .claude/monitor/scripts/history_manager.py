#!/usr/bin/env python3
"""
Historical Data Manager for Predictive System

Manages collection, storage, and retrieval of historical metrics
for trend analysis and prediction validation.
"""

import json
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class HistoryManager:
    """Manages historical data for the monitoring system"""

    def __init__(self, base_path: Path = None):
        """Initialize history manager.

        Args:
            base_path: Base path for history storage
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent / "history"

        self.base_path = base_path
        self.base_path.mkdir(exist_ok=True)

        # Create subdirectories
        self.metrics_path = self.base_path / "metrics"
        self.predictions_path = self.base_path / "predictions"
        self.events_path = self.base_path / "events"
        self.checkpoints_path = self.base_path / "checkpoints"

        for path in [self.metrics_path, self.predictions_path,
                     self.events_path, self.checkpoints_path]:
            path.mkdir(exist_ok=True)

        # Configuration
        self.retention_days = 7
        self.compression_age_hours = 24

    def store_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Store system metrics snapshot.

        Args:
            metrics: Dictionary of metrics to store

        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            date_str = timestamp.strftime("%Y%m%d")
            time_str = timestamp.strftime("%H%M%S")

            # Daily file for metrics
            daily_file = self.metrics_path / f"metrics_{date_str}.jsonl"

            # Append metrics with timestamp
            metrics_entry = {
                'timestamp': timestamp.isoformat(),
                'data': metrics
            }

            with open(daily_file, 'a') as f:
                f.write(json.dumps(metrics_entry) + '\n')

            # Compress old files
            self._compress_old_files()

            return True

        except Exception as e:
            print(f"Error storing metrics: {e}")
            return False

    def store_prediction(self, prediction: Dict[str, Any]) -> bool:
        """Store a prediction for later validation.

        Args:
            prediction: Prediction data to store

        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            date_str = timestamp.strftime("%Y%m%d")

            # Daily file for predictions
            daily_file = self.predictions_path / f"predictions_{date_str}.jsonl"

            # Add metadata
            prediction_entry = {
                'timestamp': timestamp.isoformat(),
                'prediction': prediction,
                'validated': False,
                'outcome': None
            }

            with open(daily_file, 'a') as f:
                f.write(json.dumps(prediction_entry) + '\n')

            return True

        except Exception as e:
            print(f"Error storing prediction: {e}")
            return False

    def store_event(self, event_type: str, event_data: Dict[str, Any]) -> bool:
        """Store a system event.

        Args:
            event_type: Type of event (error, warning, recovery, etc.)
            event_data: Event details

        Returns:
            Success status
        """
        try:
            timestamp = datetime.now()
            date_str = timestamp.strftime("%Y%m%d")

            # Daily file for events
            daily_file = self.events_path / f"events_{date_str}.jsonl"

            event_entry = {
                'timestamp': timestamp.isoformat(),
                'type': event_type,
                'data': event_data
            }

            with open(daily_file, 'a') as f:
                f.write(json.dumps(event_entry) + '\n')

            return True

        except Exception as e:
            print(f"Error storing event: {e}")
            return False

    def get_metrics_range(self, start_time: datetime, end_time: datetime,
                          metric_names: List[str] = None) -> List[Dict]:
        """Retrieve metrics within a time range.

        Args:
            start_time: Start of time range
            end_time: End of time range
            metric_names: Optional list of specific metrics to retrieve

        Returns:
            List of metric entries
        """
        metrics = []

        # Determine which daily files to read
        current_date = start_time.date()
        end_date = end_time.date()

        while current_date <= end_date:
            date_str = current_date.strftime("%Y%m%d")

            # Check both compressed and uncompressed files
            for suffix in ['.jsonl', '.jsonl.gz']:
                daily_file = self.metrics_path / f"metrics_{date_str}{suffix}"

                if daily_file.exists():
                    metrics.extend(self._read_time_filtered_file(
                        daily_file, start_time, end_time, metric_names
                    ))

            current_date += timedelta(days=1)

        return sorted(metrics, key=lambda x: x['timestamp'])

    def get_recent_metrics(self, minutes: int = 60,
                           metric_names: List[str] = None) -> List[Dict]:
        """Get recent metrics.

        Args:
            minutes: Number of minutes of history
            metric_names: Optional list of specific metrics

        Returns:
            List of recent metrics
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=minutes)
        return self.get_metrics_range(start_time, end_time, metric_names)

    def validate_prediction(self, prediction_id: str, outcome: bool,
                           actual_event: Dict[str, Any] = None) -> bool:
        """Validate a previous prediction.

        Args:
            prediction_id: ID of the prediction to validate
            outcome: Whether the prediction was correct
            actual_event: Actual event data if it occurred

        Returns:
            Success status
        """
        # In production, would update the prediction record
        # with validation outcome for accuracy tracking
        validation_entry = {
            'timestamp': datetime.now().isoformat(),
            'prediction_id': prediction_id,
            'outcome': outcome,
            'actual_event': actual_event
        }

        date_str = datetime.now().strftime("%Y%m%d")
        validation_file = self.predictions_path / f"validations_{date_str}.jsonl"

        try:
            with open(validation_file, 'a') as f:
                f.write(json.dumps(validation_entry) + '\n')
            return True
        except Exception as e:
            print(f"Error validating prediction: {e}")
            return False

    def calculate_prediction_accuracy(self, days: int = 7) -> Dict[str, float]:
        """Calculate prediction accuracy over time period.

        Args:
            days: Number of days to analyze

        Returns:
            Accuracy statistics
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        total_predictions = 0
        correct_predictions = 0
        false_positives = 0
        false_negatives = 0

        # Read validation files
        current_date = start_date.date()
        while current_date <= end_date.date():
            date_str = current_date.strftime("%Y%m%d")
            validation_file = self.predictions_path / f"validations_{date_str}.jsonl"

            if validation_file.exists():
                with open(validation_file, 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            total_predictions += 1
                            if entry['outcome']:
                                correct_predictions += 1
                            else:
                                false_positives += 1
                        except:
                            continue

            current_date += timedelta(days=1)

        if total_predictions == 0:
            return {
                'accuracy': 0.0,
                'total_predictions': 0,
                'false_positive_rate': 0.0
            }

        return {
            'accuracy': correct_predictions / total_predictions,
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
            'false_positive_rate': false_positives / total_predictions,
            'period_days': days
        }

    def _read_time_filtered_file(self, file_path: Path, start_time: datetime,
                                 end_time: datetime, metric_names: List[str] = None) -> List[Dict]:
        """Read and filter entries from a daily file.

        Args:
            file_path: Path to the file
            start_time: Start time filter
            end_time: End time filter
            metric_names: Optional metric name filter

        Returns:
            Filtered entries
        """
        entries = []

        # Handle compressed files
        if file_path.suffix == '.gz':
            open_func = gzip.open
            mode = 'rt'
        else:
            open_func = open
            mode = 'r'

        try:
            with open_func(file_path, mode) as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        timestamp = datetime.fromisoformat(entry['timestamp'])

                        if start_time <= timestamp <= end_time:
                            # Apply metric filter if specified
                            if metric_names:
                                filtered_data = {
                                    k: v for k, v in entry.get('data', {}).items()
                                    if k in metric_names
                                }
                                if filtered_data:
                                    entry['data'] = filtered_data
                                    entries.append(entry)
                            else:
                                entries.append(entry)
                    except:
                        continue

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

        return entries

    def _compress_old_files(self):
        """Compress files older than compression_age_hours"""
        cutoff = datetime.now() - timedelta(hours=self.compression_age_hours)

        for path in [self.metrics_path, self.predictions_path, self.events_path]:
            for file in path.glob("*.jsonl"):
                # Check file age
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime < cutoff:
                    compressed_file = file.with_suffix('.jsonl.gz')
                    if not compressed_file.exists():
                        # Compress the file
                        with open(file, 'rb') as f_in:
                            with gzip.open(compressed_file, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        # Remove original
                        file.unlink()
                        print(f"Compressed {file.name}")

    def cleanup_old_data(self):
        """Remove data older than retention period"""
        cutoff = datetime.now() - timedelta(days=self.retention_days)

        for path in [self.metrics_path, self.predictions_path,
                     self.events_path, self.checkpoints_path]:
            for file in path.glob("*"):
                # Parse date from filename
                try:
                    date_str = file.stem.split('_')[1]
                    file_date = datetime.strptime(date_str, "%Y%m%d")

                    if file_date < cutoff:
                        file.unlink()
                        print(f"Removed old file: {file.name}")
                except:
                    continue

    def get_metric_aggregates(self, metric_name: str, start_time: datetime,
                              end_time: datetime, interval: str = 'hour') -> Dict[str, List]:
        """Get aggregated metrics over time intervals.

        Args:
            metric_name: Name of the metric
            start_time: Start of time range
            end_time: End of time range
            interval: Aggregation interval ('hour', 'day')

        Returns:
            Aggregated metrics by interval
        """
        metrics = self.get_metrics_range(start_time, end_time, [metric_name])

        aggregates = defaultdict(lambda: {'values': [], 'timestamps': []})

        for entry in metrics:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            value = entry.get('data', {}).get(metric_name)

            if value is not None:
                if interval == 'hour':
                    key = timestamp.strftime('%Y-%m-%d %H:00')
                elif interval == 'day':
                    key = timestamp.strftime('%Y-%m-%d')
                else:
                    key = timestamp.strftime('%Y-%m-%d %H:%M')

                aggregates[key]['values'].append(value)
                aggregates[key]['timestamps'].append(timestamp)

        # Calculate statistics for each interval
        result = {}
        for key, data in aggregates.items():
            if data['values']:
                import statistics
                result[key] = {
                    'count': len(data['values']),
                    'mean': statistics.mean(data['values']),
                    'min': min(data['values']),
                    'max': max(data['values']),
                    'std_dev': statistics.stdev(data['values']) if len(data['values']) > 1 else 0,
                    'first': data['values'][0],
                    'last': data['values'][-1]
                }

        return result

    def compare_time_periods(self, metric_names: List[str],
                            period1_start: datetime, period1_end: datetime,
                            period2_start: datetime, period2_end: datetime) -> Dict:
        """Compare metrics between two time periods.

        Args:
            metric_names: Metrics to compare
            period1_start/end: First period boundaries
            period2_start/end: Second period boundaries

        Returns:
            Comparison results
        """
        import statistics

        period1_metrics = self.get_metrics_range(period1_start, period1_end, metric_names)
        period2_metrics = self.get_metrics_range(period2_start, period2_end, metric_names)

        comparison = {}

        for metric in metric_names:
            p1_values = [m['data'].get(metric, 0) for m in period1_metrics
                        if metric in m.get('data', {})]
            p2_values = [m['data'].get(metric, 0) for m in period2_metrics
                        if metric in m.get('data', {})]

            if p1_values and p2_values:
                p1_avg = statistics.mean(p1_values)
                p2_avg = statistics.mean(p2_values)

                comparison[metric] = {
                    'period1': {
                        'average': p1_avg,
                        'min': min(p1_values),
                        'max': max(p1_values),
                        'samples': len(p1_values)
                    },
                    'period2': {
                        'average': p2_avg,
                        'min': min(p2_values),
                        'max': max(p2_values),
                        'samples': len(p2_values)
                    },
                    'change': {
                        'absolute': p2_avg - p1_avg,
                        'percentage': ((p2_avg - p1_avg) / p1_avg * 100) if p1_avg != 0 else 0,
                        'direction': 'increase' if p2_avg > p1_avg else 'decrease' if p2_avg < p1_avg else 'stable'
                    }
                }

        return comparison

    def get_metric_percentiles(self, metric_name: str,
                              start_time: datetime, end_time: datetime) -> Dict[str, float]:
        """Calculate percentiles for a metric over a time range.

        Args:
            metric_name: Name of the metric
            start_time: Start of time range
            end_time: End of time range

        Returns:
            Percentile values (p50, p75, p90, p95, p99)
        """
        import statistics

        metrics = self.get_metrics_range(start_time, end_time, [metric_name])
        values = [m['data'].get(metric_name, 0) for m in metrics
                 if metric_name in m.get('data', {})]

        if not values:
            return {}

        values.sort()
        n = len(values)

        def percentile(p):
            k = (n - 1) * p / 100
            f = int(k)
            c = f + 1 if f < n - 1 else f
            return values[f] + (k - f) * (values[c] - values[f]) if f != c else values[f]

        return {
            'p50': percentile(50),  # Median
            'p75': percentile(75),
            'p90': percentile(90),
            'p95': percentile(95),
            'p99': percentile(99),
            'mean': statistics.mean(values),
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0
        }

    def find_correlations(self, metrics: List[str],
                         start_time: datetime, end_time: datetime) -> Dict[str, float]:
        """Find correlations between different metrics.

        Args:
            metrics: List of metric names
            start_time: Start of time range
            end_time: End of time range

        Returns:
            Correlation matrix
        """
        import statistics

        data = self.get_metrics_range(start_time, end_time, metrics)

        # Extract values for each metric
        metric_values = defaultdict(list)
        for entry in data:
            for metric in metrics:
                if metric in entry.get('data', {}):
                    metric_values[metric].append(entry['data'][metric])

        correlations = {}

        # Calculate Pearson correlation coefficient for each pair
        for m1 in metrics:
            for m2 in metrics:
                if m1 != m2:
                    v1 = metric_values[m1]
                    v2 = metric_values[m2]

                    # Ensure equal length
                    min_len = min(len(v1), len(v2))
                    if min_len > 1:
                        v1 = v1[:min_len]
                        v2 = v2[:min_len]

                        # Calculate correlation
                        mean1 = statistics.mean(v1)
                        mean2 = statistics.mean(v2)

                        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(v1, v2))
                        denominator = (
                            sum((x - mean1) ** 2 for x in v1) *
                            sum((y - mean2) ** 2 for y in v2)
                        ) ** 0.5

                        if denominator > 0:
                            correlation = numerator / denominator
                            correlations[f"{m1}_vs_{m2}"] = round(correlation, 3)

        return correlations

    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a summary report of historical data.

        Returns:
            Summary statistics
        """
        now = datetime.now()
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)
        last_week = now - timedelta(days=7)

        # Gather statistics
        hourly_metrics = self.get_metrics_range(last_hour, now)
        daily_metrics = self.get_metrics_range(last_day, now)
        weekly_metrics = self.get_metrics_range(last_week, now)

        # Calculate averages
        def calculate_averages(metrics_list):
            if not metrics_list:
                return {}

            totals = defaultdict(float)
            counts = defaultdict(int)

            for entry in metrics_list:
                for key, value in entry.get('data', {}).items():
                    if isinstance(value, (int, float)):
                        totals[key] += value
                        counts[key] += 1

            return {k: totals[k] / counts[k] for k in totals}

        # Find correlations for the last day
        common_metrics = ['memory_usage', 'cpu_usage', 'error_rate', 'task_queue']
        correlations = self.find_correlations(common_metrics, last_day, now)

        # Get percentiles for key metrics
        percentiles = {}
        for metric in common_metrics:
            percentiles[metric] = self.get_metric_percentiles(metric, last_day, now)

        return {
            'timestamp': now.isoformat(),
            'data_points': {
                'last_hour': len(hourly_metrics),
                'last_day': len(daily_metrics),
                'last_week': len(weekly_metrics)
            },
            'averages': {
                'hourly': calculate_averages(hourly_metrics),
                'daily': calculate_averages(daily_metrics),
                'weekly': calculate_averages(weekly_metrics)
            },
            'percentiles': percentiles,
            'correlations': correlations,
            'prediction_accuracy': self.calculate_prediction_accuracy(7),
            'storage': {
                'metrics_files': len(list(self.metrics_path.glob("*"))),
                'prediction_files': len(list(self.predictions_path.glob("*"))),
                'event_files': len(list(self.events_path.glob("*"))),
                'total_size_mb': sum(
                    f.stat().st_size for f in self.base_path.rglob("*") if f.is_file()
                ) / (1024 * 1024)
            }
        }


def main():
    """Main entry point for testing"""
    manager = HistoryManager()

    print("Historical Data Manager")
    print("=" * 50)

    # Store sample metrics
    sample_metrics = {
        'memory_usage': 65.2,
        'cpu_usage': 42.1,
        'error_rate': 1.2,
        'task_queue': 5
    }

    if manager.store_metrics(sample_metrics):
        print("✅ Stored sample metrics")

    # Store sample prediction
    sample_prediction = {
        'type': 'memory_leak',
        'probability': 0.75,
        'time_to_impact': 30
    }

    if manager.store_prediction(sample_prediction):
        print("✅ Stored sample prediction")

    # Store sample event
    if manager.store_event('warning', {'message': 'High memory usage detected'}):
        print("✅ Stored sample event")

    # Get recent metrics
    recent = manager.get_recent_metrics(minutes=60)
    print(f"\n📊 Recent metrics (last hour): {len(recent)} data points")

    # Generate summary
    summary = manager.generate_summary_report()
    print(f"\n📈 Summary Report:")
    print(f"   Data points (last hour): {summary['data_points']['last_hour']}")
    print(f"   Storage size: {summary['storage']['total_size_mb']:.2f} MB")

    # Cleanup old data
    manager.cleanup_old_data()
    print("\n✅ Cleanup completed")


if __name__ == "__main__":
    main()