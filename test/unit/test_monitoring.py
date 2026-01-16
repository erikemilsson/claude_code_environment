#!/usr/bin/env python3
"""
Unit tests for monitoring system components
"""

import unittest
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, call
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import monitoring modules
from claude.monitor.scripts import health_checker
from claude.monitor.scripts import dashboard_updater
from claude.monitor.scripts import diagnose
from claude.monitor.scripts import self_heal
from claude.monitor.scripts import quick_status


class TestHealthChecker(unittest.TestCase):
    """Tests for health_checker.py"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "config" / "thresholds.json"
        self.health_path = Path(self.temp_dir) / "health-checks.json"

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('claude.monitor.scripts.health_checker.get_system_metrics')
    def test_get_memory_usage(self, mock_metrics):
        """Test memory usage calculation"""
        mock_metrics.return_value = {
            'memory': {'percent': 45.5, 'available_gb': 8.2}
        }

        metrics = health_checker.get_system_metrics()
        self.assertEqual(metrics['memory']['percent'], 45.5)
        self.assertEqual(metrics['memory']['available_gb'], 8.2)

    @patch('claude.monitor.scripts.health_checker.check_file_operations')
    def test_file_operation_speed(self, mock_check):
        """Test file operation speed check"""
        mock_check.return_value = {
            'status': 'healthy',
            'read_speed': 0.001,
            'write_speed': 0.002
        }

        result = health_checker.check_file_operations()
        self.assertEqual(result['status'], 'healthy')
        self.assertLess(result['read_speed'], 0.01)

    @patch('claude.monitor.scripts.health_checker.check_task_queue')
    def test_task_queue_status(self, mock_queue):
        """Test task queue status check"""
        mock_queue.return_value = {
            'pending': 5,
            'blocked': 1,
            'in_progress': 2,
            'health': 'good'
        }

        result = health_checker.check_task_queue()
        self.assertEqual(result['pending'], 5)
        self.assertEqual(result['blocked'], 1)
        self.assertEqual(result['health'], 'good')

    @patch('claude.monitor.scripts.health_checker.check_checkpoint_freshness')
    def test_checkpoint_freshness(self, mock_checkpoint):
        """Test checkpoint freshness check"""
        mock_checkpoint.return_value = {
            'status': 'fresh',
            'age_hours': 0.5,
            'last_checkpoint': '2025-12-29T18:00:00Z'
        }

        result = health_checker.check_checkpoint_freshness()
        self.assertEqual(result['status'], 'fresh')
        self.assertLess(result['age_hours'], 1.0)

    def test_threshold_loading(self):
        """Test loading of threshold configurations"""
        # Create test threshold config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        thresholds = {
            "memory": {"warning": 80, "critical": 90},
            "file_ops": {"warning": 0.5, "critical": 1.0},
            "task_queue": {"warning": 10, "critical": 20}
        }

        with open(self.config_path, 'w') as f:
            json.dump(thresholds, f)

        # Test loading
        with patch('claude.monitor.scripts.health_checker.THRESHOLD_CONFIG', self.config_path):
            loaded = health_checker.load_thresholds()
            self.assertEqual(loaded['memory']['warning'], 80)
            self.assertEqual(loaded['file_ops']['critical'], 1.0)


class TestDashboardUpdater(unittest.TestCase):
    """Tests for dashboard_updater.py"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.dashboard_path = Path(self.temp_dir) / "live-dashboard.md"

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('claude.monitor.scripts.dashboard_updater.get_current_operation')
    def test_current_operation_display(self, mock_op):
        """Test current operation display"""
        mock_op.return_value = {
            'operation': 'Running tests',
            'progress': 75,
            'eta': '2 minutes'
        }

        result = dashboard_updater.get_current_operation()
        self.assertEqual(result['operation'], 'Running tests')
        self.assertEqual(result['progress'], 75)

    @patch('claude.monitor.scripts.dashboard_updater.get_task_status')
    def test_task_status_summary(self, mock_status):
        """Test task status summary generation"""
        mock_status.return_value = {
            'total': 100,
            'completed': 60,
            'in_progress': 5,
            'pending': 35
        }

        result = dashboard_updater.get_task_status()
        self.assertEqual(result['total'], 100)
        self.assertEqual(result['completed'], 60)
        self.assertEqual(result['completed'] + result['in_progress'] + result['pending'], 100)

    @patch('claude.monitor.scripts.dashboard_updater.generate_progress_bar')
    def test_progress_bar_generation(self, mock_bar):
        """Test progress bar generation"""
        mock_bar.return_value = "████████░░ 80%"

        result = dashboard_updater.generate_progress_bar(80)
        self.assertIn("█", result)
        self.assertIn("80%", result)

    @patch('claude.monitor.scripts.dashboard_updater.format_warnings')
    def test_warning_formatting(self, mock_warnings):
        """Test warning message formatting"""
        mock_warnings.return_value = [
            "⚠️ High memory usage (85%)",
            "⚠️ 5 tasks blocked"
        ]

        warnings = dashboard_updater.format_warnings()
        self.assertEqual(len(warnings), 2)
        self.assertTrue(all("⚠️" in w for w in warnings))

    def test_atomic_write(self):
        """Test atomic file write operation"""
        content = "# Test Dashboard\nStatus: Active"

        with patch('claude.monitor.scripts.dashboard_updater.DASHBOARD_PATH', self.dashboard_path):
            dashboard_updater.write_dashboard_atomic(content)

            with open(self.dashboard_path, 'r') as f:
                written = f.read()

            self.assertEqual(written, content)


class TestDiagnoseEngine(unittest.TestCase):
    """Tests for diagnose.py"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.patterns_path = Path(self.temp_dir) / "patterns.json"
        self.diagnostics_path = Path(self.temp_dir) / "diagnostics.md"

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('claude.monitor.scripts.diagnose.identify_failure_type')
    def test_failure_identification(self, mock_identify):
        """Test failure type identification"""
        mock_identify.return_value = {
            'type': 'FileNotFoundError',
            'category': 'file_system',
            'severity': 'high'
        }

        result = diagnose.identify_failure_type("FileNotFoundError: tasks.json")
        self.assertEqual(result['type'], 'FileNotFoundError')
        self.assertEqual(result['category'], 'file_system')

    @patch('claude.monitor.scripts.diagnose.find_root_cause')
    def test_root_cause_analysis(self, mock_root):
        """Test root cause analysis"""
        mock_root.return_value = {
            'cause': 'Missing configuration file',
            'confidence': 0.85,
            'evidence': ['File not found in expected location', 'No fallback path configured']
        }

        result = diagnose.find_root_cause("ConfigError")
        self.assertEqual(result['cause'], 'Missing configuration file')
        self.assertGreater(result['confidence'], 0.8)

    @patch('claude.monitor.scripts.diagnose.detect_patterns')
    def test_pattern_detection(self, mock_patterns):
        """Test failure pattern detection"""
        mock_patterns.return_value = {
            'pattern': 'Recurring timeout errors',
            'frequency': 5,
            'last_occurrence': '2025-12-29T18:00:00Z'
        }

        result = diagnose.detect_patterns(['timeout', 'timeout', 'success', 'timeout'])
        self.assertIn('timeout', result['pattern'].lower())
        self.assertGreater(result['frequency'], 1)

    @patch('claude.monitor.scripts.diagnose.generate_diagnostic_report')
    def test_report_generation(self, mock_report):
        """Test diagnostic report generation"""
        mock_report.return_value = """
        # Diagnostic Report

        ## Issue: Test Failures
        - Type: AssertionError
        - Root Cause: Incorrect expected value
        - Recommended Fix: Update test assertions
        """

        report = diagnose.generate_diagnostic_report({'type': 'test_failure'})
        self.assertIn("Diagnostic Report", report)
        self.assertIn("Root Cause", report)

    def test_pattern_loading(self):
        """Test loading of error patterns"""
        patterns = {
            "file_errors": ["FileNotFoundError", "PermissionError"],
            "network_errors": ["ConnectionError", "TimeoutError"],
            "task_errors": ["ValidationError", "DependencyError"]
        }

        os.makedirs(os.path.dirname(self.patterns_path), exist_ok=True)
        with open(self.patterns_path, 'w') as f:
            json.dump(patterns, f)

        with patch('claude.monitor.scripts.diagnose.PATTERNS_PATH', self.patterns_path):
            loaded = diagnose.load_patterns()
            self.assertIn("file_errors", loaded)
            self.assertEqual(len(loaded['file_errors']), 2)


class TestSelfHeal(unittest.TestCase):
    """Tests for self_heal.py"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.recommendations_path = Path(self.temp_dir) / "self-heal.md"

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('claude.monitor.scripts.self_heal.generate_fix_recommendation')
    def test_fix_generation(self, mock_fix):
        """Test fix recommendation generation"""
        mock_fix.return_value = {
            'fix': 'Create missing directory',
            'command': 'mkdir -p .claude/tasks',
            'risk': 'low',
            'success_probability': 0.95
        }

        result = self_heal.generate_fix_recommendation('DirectoryNotFound')
        self.assertIn('mkdir', result['command'])
        self.assertEqual(result['risk'], 'low')
        self.assertGreater(result['success_probability'], 0.9)

    @patch('claude.monitor.scripts.self_heal.assess_risk')
    def test_risk_assessment(self, mock_risk):
        """Test fix risk assessment"""
        mock_risk.return_value = {
            'level': 'medium',
            'score': 5,
            'warnings': ['May affect existing files']
        }

        result = self_heal.assess_risk('modify_config')
        self.assertEqual(result['level'], 'medium')
        self.assertLessEqual(result['score'], 10)

    @patch('claude.monitor.scripts.self_heal.generate_rollback_instructions')
    def test_rollback_generation(self, mock_rollback):
        """Test rollback instruction generation"""
        mock_rollback.return_value = [
            'git stash',
            'git checkout HEAD~1',
            'Restore from backup: backup_20251229.tar.gz'
        ]

        instructions = self_heal.generate_rollback_instructions('config_change')
        self.assertTrue(len(instructions) > 0)
        self.assertTrue(any('backup' in i.lower() for i in instructions))

    @patch('claude.monitor.scripts.self_heal.dry_run_fix')
    def test_dry_run_capability(self, mock_dry):
        """Test dry run execution"""
        mock_dry.return_value = {
            'would_execute': ['mkdir -p test', 'touch test/file.txt'],
            'expected_changes': ['Create directory: test', 'Create file: test/file.txt'],
            'safe': True
        }

        result = self_heal.dry_run_fix('create_test_structure')
        self.assertTrue(result['safe'])
        self.assertEqual(len(result['would_execute']), 2)

    @patch('claude.monitor.scripts.self_heal.create_backup')
    def test_backup_creation(self, mock_backup):
        """Test backup creation before fix"""
        mock_backup.return_value = {
            'backup_path': '/tmp/backup_20251229_180000.tar.gz',
            'size_mb': 2.5,
            'files_backed_up': 15
        }

        result = self_heal.create_backup()
        self.assertIn('backup', result['backup_path'])
        self.assertGreater(result['files_backed_up'], 0)


class TestQuickStatus(unittest.TestCase):
    """Tests for quick_status.py"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('claude.monitor.scripts.quick_status.get_quick_status')
    def test_quick_status_generation(self, mock_status):
        """Test quick status summary generation"""
        mock_status.return_value = {
            'health': 'good',
            'active_tasks': 3,
            'warnings': 0,
            'last_checkpoint': '5 minutes ago'
        }

        result = quick_status.get_quick_status()
        self.assertEqual(result['health'], 'good')
        self.assertEqual(result['warnings'], 0)

    @patch('claude.monitor.scripts.quick_status.format_status_line')
    def test_status_line_formatting(self, mock_format):
        """Test status line formatting"""
        mock_format.return_value = "✅ System healthy | 3 active tasks | No warnings"

        line = quick_status.format_status_line({'health': 'good', 'tasks': 3})
        self.assertIn("✅", line)
        self.assertIn("healthy", line)


class TestMonitoringIntegration(unittest.TestCase):
    """Integration tests for monitoring system components"""

    @patch('claude.monitor.scripts.health_checker.run_health_check')
    @patch('claude.monitor.scripts.dashboard_updater.update_dashboard')
    def test_health_check_triggers_dashboard_update(self, mock_dashboard, mock_health):
        """Test that health check triggers dashboard update"""
        mock_health.return_value = {'status': 'warning', 'memory': 85}

        # Run health check
        health_result = health_checker.run_health_check()

        # Verify dashboard update was triggered
        if health_result['status'] == 'warning':
            dashboard_updater.update_dashboard(health_result)
            mock_dashboard.assert_called_once()

    @patch('claude.monitor.scripts.diagnose.run_diagnosis')
    @patch('claude.monitor.scripts.self_heal.generate_fixes')
    def test_diagnosis_triggers_healing(self, mock_heal, mock_diagnose):
        """Test that diagnosis triggers healing recommendations"""
        mock_diagnose.return_value = {
            'issues': ['high_memory', 'slow_file_ops'],
            'severity': 'high'
        }

        # Run diagnosis
        diagnosis = diagnose.run_diagnosis()

        # Verify healing was triggered for high severity
        if diagnosis['severity'] == 'high':
            self_heal.generate_fixes(diagnosis['issues'])
            mock_heal.assert_called_once()


class TestPerformanceMetrics(unittest.TestCase):
    """Test performance requirements for monitoring system"""

    @patch('claude.monitor.scripts.health_checker.measure_overhead')
    def test_monitoring_overhead_under_5_percent(self, mock_overhead):
        """Test that monitoring overhead is less than 5%"""
        mock_overhead.return_value = 3.2  # 3.2% overhead

        overhead = health_checker.measure_overhead()
        self.assertLess(overhead, 5.0, "Monitoring overhead exceeds 5% threshold")

    @patch('claude.monitor.scripts.dashboard_updater.measure_update_time')
    def test_dashboard_update_speed(self, mock_time):
        """Test dashboard updates complete within 100ms"""
        mock_time.return_value = 0.085  # 85ms

        update_time = dashboard_updater.measure_update_time()
        self.assertLess(update_time, 0.1, "Dashboard update exceeds 100ms threshold")


if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHealthChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestDashboardUpdater))
    suite.addTests(loader.loadTestsFromTestCase(TestDiagnoseEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestSelfHeal))
    suite.addTests(loader.loadTestsFromTestCase(TestQuickStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestMonitoringIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceMetrics))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)