#!/usr/bin/env python3
"""
Performance Impact Monitor for Observability System

This module tracks the performance overhead of the monitoring system itself
to ensure it stays within acceptable bounds (< 5% impact).
"""

import time
import psutil
import os
import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class PerformanceMonitor:
    """Monitors the performance impact of the observability system."""

    def __init__(self, config_path: Path = None):
        """Initialize the performance monitor.

        Args:
            config_path: Path to configuration directory
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config"

        self.config_path = config_path
        self.thresholds = self._load_thresholds()

        # Performance tracking
        self.baseline_cpu = None
        self.baseline_memory = None
        self.monitoring_processes = set()
        self.overhead_history = []
        self.max_history_size = 100

        # Auto-disable state
        self.monitoring_enabled = True
        self.auto_disable_threshold = 5.0  # 5% overhead threshold
        self.consecutive_breaches = 0
        self.breach_threshold = 3  # Disable after 3 consecutive breaches

        # Thread safety
        self.lock = threading.Lock()

        # Initialize baseline measurements
        self.establish_baseline()

    def _load_thresholds(self) -> Dict:
        """Load threshold configuration."""
        threshold_file = self.config_path / "thresholds.json"
        if threshold_file.exists():
            with open(threshold_file, 'r') as f:
                config = json.load(f)
                # Add monitoring-specific thresholds if not present
                if 'monitoring_overhead' not in config:
                    config['monitoring_overhead'] = {
                        'cpu_percent': 5.0,
                        'memory_mb': 100,
                        'io_ops_per_sec': 50,
                        'auto_disable_threshold': 5.0
                    }
                return config
        return {
            'monitoring_overhead': {
                'cpu_percent': 5.0,
                'memory_mb': 100,
                'io_ops_per_sec': 50,
                'auto_disable_threshold': 5.0
            }
        }

    def establish_baseline(self) -> None:
        """Establish baseline resource usage without monitoring."""
        # Get current system state before monitoring starts
        self.baseline_cpu = psutil.cpu_percent(interval=1)
        self.baseline_memory = psutil.virtual_memory().used / (1024 * 1024)  # MB

    def register_monitoring_process(self, pid: int) -> None:
        """Register a monitoring process to track.

        Args:
            pid: Process ID of monitoring script
        """
        with self.lock:
            self.monitoring_processes.add(pid)

    def measure_overhead(self) -> Dict[str, float]:
        """Measure the current overhead of monitoring processes.

        Returns:
            Dictionary containing overhead metrics
        """
        overhead = {
            'cpu_percent': 0.0,
            'memory_mb': 0.0,
            'io_ops_per_sec': 0.0,
            'total_percent': 0.0,
            'timestamp': datetime.now().isoformat(),
            'monitoring_enabled': self.monitoring_enabled
        }

        try:
            # Track all monitoring script processes
            monitoring_pids = self._find_monitoring_processes()

            total_cpu = 0.0
            total_memory = 0.0
            total_io_ops = 0.0

            for pid in monitoring_pids:
                try:
                    process = psutil.Process(pid)

                    # CPU usage (percentage of single core)
                    cpu_percent = process.cpu_percent(interval=0.1)
                    total_cpu += cpu_percent

                    # Memory usage in MB
                    memory_info = process.memory_info()
                    memory_mb = memory_info.rss / (1024 * 1024)
                    total_memory += memory_mb

                    # I/O operations (if available)
                    try:
                        io_counters = process.io_counters()
                        # Simple I/O ops estimation
                        total_io_ops += (io_counters.read_count + io_counters.write_count) / 100
                    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                        pass

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Calculate overhead percentages
            overhead['cpu_percent'] = total_cpu
            overhead['memory_mb'] = total_memory
            overhead['io_ops_per_sec'] = total_io_ops

            # Calculate total overhead as weighted average
            # CPU is most important (60%), Memory (30%), I/O (10%)
            cpu_impact = min(total_cpu / 100.0 * 100, 100)  # Normalize to 0-100
            memory_impact = min(total_memory / 1000.0 * 100, 100)  # Assume 1GB is 100%
            io_impact = min(total_io_ops / 100.0 * 100, 100)  # 100 ops/sec is 100%

            overhead['total_percent'] = (
                cpu_impact * 0.6 +
                memory_impact * 0.3 +
                io_impact * 0.1
            )

            # Track history
            with self.lock:
                self.overhead_history.append(overhead)
                if len(self.overhead_history) > self.max_history_size:
                    self.overhead_history.pop(0)

            # Check for auto-disable
            self._check_auto_disable(overhead['total_percent'])

        except Exception as e:
            overhead['error'] = str(e)

        return overhead

    def _find_monitoring_processes(self) -> List[int]:
        """Find all monitoring-related processes.

        Returns:
            List of process IDs
        """
        monitoring_pids = []

        # Look for known monitoring scripts
        monitoring_scripts = [
            'health_checker.py',
            'dashboard_updater.py',
            'diagnose.py',
            'self_heal.py',
            'performance_monitor.py'
        ]

        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any(script in ' '.join(cmdline) for script in monitoring_scripts):
                    monitoring_pids.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Also include manually registered processes
        with self.lock:
            monitoring_pids.extend(self.monitoring_processes)

        return list(set(monitoring_pids))

    def _check_auto_disable(self, total_overhead: float) -> None:
        """Check if monitoring should be auto-disabled due to high overhead.

        Args:
            total_overhead: Current total overhead percentage
        """
        if total_overhead > self.auto_disable_threshold:
            self.consecutive_breaches += 1

            if self.consecutive_breaches >= self.breach_threshold and self.monitoring_enabled:
                self.disable_monitoring(f"Overhead exceeded {self.auto_disable_threshold}% "
                                       f"for {self.consecutive_breaches} consecutive checks")
        else:
            self.consecutive_breaches = 0

    def disable_monitoring(self, reason: str) -> None:
        """Disable monitoring due to high overhead.

        Args:
            reason: Reason for disabling
        """
        with self.lock:
            if self.monitoring_enabled:
                self.monitoring_enabled = False

                # Log the disable event
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'event': 'monitoring_disabled',
                    'reason': reason,
                    'overhead_history': self.overhead_history[-5:] if self.overhead_history else []
                }

                # Write to monitoring log
                log_path = self.config_path.parent / 'logs' / 'performance_monitor.log'
                log_path.parent.mkdir(exist_ok=True)

                with open(log_path, 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')

                # Create alert file for dashboard
                alert_path = self.config_path.parent / 'alerts' / 'monitoring_disabled.json'
                alert_path.parent.mkdir(exist_ok=True)

                with open(alert_path, 'w') as f:
                    json.dump({
                        'alert': 'MONITORING AUTO-DISABLED',
                        'reason': reason,
                        'timestamp': datetime.now().isoformat(),
                        'action': 'Review performance metrics and reduce monitoring scope'
                    }, f, indent=2)

                print(f"⚠️  MONITORING AUTO-DISABLED: {reason}")

    def re_enable_monitoring(self) -> None:
        """Re-enable monitoring after it was auto-disabled."""
        with self.lock:
            self.monitoring_enabled = True
            self.consecutive_breaches = 0

            # Clear alert
            alert_path = self.config_path.parent / 'alerts' / 'monitoring_disabled.json'
            if alert_path.exists():
                alert_path.unlink()

            print("✓ Monitoring re-enabled")

    def get_performance_report(self) -> Dict:
        """Generate a performance impact report.

        Returns:
            Performance report dictionary
        """
        current_overhead = self.measure_overhead()

        # Calculate averages from history
        avg_cpu = 0.0
        avg_memory = 0.0
        avg_total = 0.0

        if self.overhead_history:
            valid_history = [h for h in self.overhead_history if 'error' not in h]
            if valid_history:
                avg_cpu = sum(h['cpu_percent'] for h in valid_history) / len(valid_history)
                avg_memory = sum(h['memory_mb'] for h in valid_history) / len(valid_history)
                avg_total = sum(h['total_percent'] for h in valid_history) / len(valid_history)

        return {
            'current': current_overhead,
            'averages': {
                'cpu_percent': round(avg_cpu, 2),
                'memory_mb': round(avg_memory, 2),
                'total_percent': round(avg_total, 2)
            },
            'monitoring_enabled': self.monitoring_enabled,
            'consecutive_breaches': self.consecutive_breaches,
            'history_size': len(self.overhead_history),
            'thresholds': self.thresholds.get('monitoring_overhead', {}),
            'monitoring_processes': len(self._find_monitoring_processes())
        }

    def check_performance_gates(self) -> Tuple[bool, List[str]]:
        """Check if monitoring performance is within acceptable limits.

        Returns:
            Tuple of (all_passed, list_of_warnings)
        """
        warnings = []
        overhead = self.measure_overhead()
        thresholds = self.thresholds.get('monitoring_overhead', {})

        # Check CPU overhead
        if overhead['cpu_percent'] > thresholds.get('cpu_percent', 5.0):
            warnings.append(f"CPU overhead {overhead['cpu_percent']:.1f}% exceeds threshold")

        # Check memory usage
        if overhead['memory_mb'] > thresholds.get('memory_mb', 100):
            warnings.append(f"Memory usage {overhead['memory_mb']:.1f}MB exceeds threshold")

        # Check total overhead
        if overhead['total_percent'] > self.auto_disable_threshold:
            warnings.append(f"Total overhead {overhead['total_percent']:.1f}% exceeds auto-disable threshold")

        # Check if monitoring is disabled
        if not self.monitoring_enabled:
            warnings.append("Monitoring is currently DISABLED due to high overhead")

        return (len(warnings) == 0, warnings)


def main():
    """Main entry point for standalone execution."""
    monitor = PerformanceMonitor()

    print("Performance Impact Monitor Started")
    print("=" * 50)

    try:
        while True:
            report = monitor.get_performance_report()

            print(f"\nTimestamp: {datetime.now().isoformat()}")
            print(f"Monitoring Status: {'ENABLED' if report['monitoring_enabled'] else 'DISABLED'}")
            print(f"Monitoring Processes: {report['monitoring_processes']}")
            print("\nCurrent Overhead:")
            print(f"  CPU: {report['current']['cpu_percent']:.2f}%")
            print(f"  Memory: {report['current']['memory_mb']:.2f} MB")
            print(f"  Total: {report['current']['total_percent']:.2f}%")
            print("\nAverages:")
            print(f"  CPU: {report['averages']['cpu_percent']:.2f}%")
            print(f"  Memory: {report['averages']['memory_mb']:.2f} MB")
            print(f"  Total: {report['averages']['total_percent']:.2f}%")

            if report['consecutive_breaches'] > 0:
                print(f"\n⚠️  WARNING: {report['consecutive_breaches']} consecutive threshold breaches")

            # Check performance gates
            passed, warnings = monitor.check_performance_gates()
            if not passed:
                print("\n⚠️  Performance Warnings:")
                for warning in warnings:
                    print(f"  - {warning}")

            time.sleep(10)  # Check every 10 seconds

    except KeyboardInterrupt:
        print("\n\nPerformance monitor stopped")


if __name__ == "__main__":
    main()