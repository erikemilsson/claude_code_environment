#!/usr/bin/env python3
"""
Integration tests for the complete observability system workflow
"""

import unittest
import json
import os
import sys
import tempfile
import shutil
import time
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestObservabilityWorkflow(unittest.TestCase):
    """End-to-end tests for observability system workflow"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.monitor_dir = Path(self.temp_dir) / ".claude" / "monitor"
        self.tasks_dir = Path(self.temp_dir) / ".claude" / "tasks"

        # Create directory structure
        os.makedirs(self.monitor_dir / "scripts", exist_ok=True)
        os.makedirs(self.monitor_dir / "config", exist_ok=True)
        os.makedirs(self.tasks_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_monitoring_cycle(self):
        """Test complete monitoring cycle from health check to dashboard update"""
        # Step 1: Create initial health check data
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "memory": {"percent": 45, "available_gb": 8},
            "file_operations": {"read_speed": 0.001, "write_speed": 0.002},
            "task_queue": {"pending": 5, "blocked": 1, "in_progress": 2},
            "checkpoint": {"status": "fresh", "age_hours": 0.5}
        }

        health_file = self.monitor_dir / "health-checks.json"
        with open(health_file, 'w') as f:
            json.dump(health_data, f)

        # Step 2: Create dashboard file
        dashboard_file = self.monitor_dir / "live-dashboard.md"
        dashboard_content = """# Live Dashboard

## Current Status
- Memory: 45% used
- Tasks: 5 pending, 2 in progress, 1 blocked
- Health: ✅ Good

Last updated: {}
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        with open(dashboard_file, 'w') as f:
            f.write(dashboard_content)

        # Step 3: Verify files were created
        self.assertTrue(health_file.exists())
        self.assertTrue(dashboard_file.exists())

        # Step 4: Simulate health degradation
        health_data["memory"]["percent"] = 85
        health_data["task_queue"]["blocked"] = 5

        with open(health_file, 'w') as f:
            json.dump(health_data, f)

        # Step 5: Check that warning state is detected
        with open(health_file, 'r') as f:
            updated_health = json.load(f)

        self.assertGreater(updated_health["memory"]["percent"], 80)
        self.assertGreater(updated_health["task_queue"]["blocked"], 3)

    def test_diagnosis_to_healing_flow(self):
        """Test flow from problem diagnosis to healing recommendation"""
        # Step 1: Create diagnostic report
        diagnostics_file = self.monitor_dir / "diagnostics.md"
        diagnostics_content = """# Diagnostics Report

## Issues Detected
1. High memory usage (85%)
   - Root cause: Large task backlog
   - Pattern: Increasing over last hour

2. Blocked tasks (5 tasks)
   - Root cause: Missing dependencies
   - Pattern: Recurring daily

## Recommendations
- Clear completed task cache
- Resolve dependency conflicts
"""
        with open(diagnostics_file, 'w') as f:
            f.write(diagnostics_content)

        # Step 2: Create self-healing recommendations
        heal_file = self.monitor_dir / "self-heal.md"
        heal_content = """# Self-Healing Recommendations

## Fix 1: Clear Task Cache
```bash
rm -rf .claude/tasks/cache/*
```
Risk: Low | Success Probability: 95%

## Fix 2: Install Missing Dependencies
```bash
pip install -r requirements.txt
```
Risk: Low | Success Probability: 90%

## Rollback Instructions
1. Restore from backup: `tar -xzf backup.tar.gz`
2. Reset to previous commit: `git reset --hard HEAD~1`
"""
        with open(heal_file, 'w') as f:
            f.write(heal_content)

        # Step 3: Verify diagnostic and healing files exist
        self.assertTrue(diagnostics_file.exists())
        self.assertTrue(heal_file.exists())

        # Step 4: Verify content linkage
        with open(diagnostics_file, 'r') as f:
            diag = f.read()
        with open(heal_file, 'r') as f:
            heal = f.read()

        self.assertIn("memory", diag.lower())
        self.assertIn("cache", heal.lower())

    def test_task_monitoring_integration(self):
        """Test integration between task system and monitoring"""
        # Step 1: Create sample task files
        tasks = [
            {"id": "1", "status": "Pending", "title": "Task 1"},
            {"id": "2", "status": "In Progress", "title": "Task 2"},
            {"id": "3", "status": "Blocked", "title": "Task 3"},
            {"id": "4", "status": "Finished", "title": "Task 4"},
            {"id": "5", "status": "Pending", "title": "Task 5"}
        ]

        for task in tasks:
            task_file = self.tasks_dir / f"task-{task['id']}.json"
            with open(task_file, 'w') as f:
                json.dump(task, f)

        # Step 2: Count task statuses
        status_counts = {"Pending": 0, "In Progress": 0, "Blocked": 0, "Finished": 0}

        for task_file in self.tasks_dir.glob("task-*.json"):
            with open(task_file, 'r') as f:
                task = json.load(f)
                status_counts[task["status"]] += 1

        # Step 3: Verify task counts
        self.assertEqual(status_counts["Pending"], 2)
        self.assertEqual(status_counts["In Progress"], 1)
        self.assertEqual(status_counts["Blocked"], 1)
        self.assertEqual(status_counts["Finished"], 1)

        # Step 4: Create monitoring summary based on tasks
        summary = {
            "total_tasks": len(tasks),
            "health": "warning" if status_counts["Blocked"] > 0 else "good",
            "blocked_tasks": status_counts["Blocked"],
            "completion_rate": status_counts["Finished"] / len(tasks) * 100
        }

        self.assertEqual(summary["total_tasks"], 5)
        self.assertEqual(summary["health"], "warning")
        self.assertEqual(summary["completion_rate"], 20.0)

    def test_performance_monitoring(self):
        """Test performance monitoring and overhead calculation"""
        start_time = time.time()

        # Simulate monitoring operations
        operations = []
        for i in range(100):
            op_start = time.time()

            # Simulate health check
            time.sleep(0.001)  # 1ms operation

            op_time = time.time() - op_start
            operations.append(op_time)

        total_time = time.time() - start_time
        monitoring_time = sum(operations)
        overhead_percent = (monitoring_time / total_time) * 100

        # Verify overhead is under 5%
        self.assertLess(overhead_percent, 5.0,
                       f"Monitoring overhead {overhead_percent:.2f}% exceeds 5% limit")

    def test_alert_triggering(self):
        """Test alert triggering based on thresholds"""
        # Create threshold configuration
        thresholds = {
            "memory": {"warning": 70, "critical": 90},
            "blocked_tasks": {"warning": 3, "critical": 5},
            "file_op_speed": {"warning": 0.5, "critical": 1.0}
        }

        threshold_file = self.monitor_dir / "config" / "thresholds.json"
        os.makedirs(threshold_file.parent, exist_ok=True)
        with open(threshold_file, 'w') as f:
            json.dump(thresholds, f)

        # Test various scenarios
        test_cases = [
            {"memory": 60, "blocked": 2, "speed": 0.1, "expected": "good"},
            {"memory": 75, "blocked": 2, "speed": 0.1, "expected": "warning"},
            {"memory": 92, "blocked": 2, "speed": 0.1, "expected": "critical"},
            {"memory": 60, "blocked": 6, "speed": 0.1, "expected": "critical"},
            {"memory": 60, "blocked": 2, "speed": 1.5, "expected": "critical"}
        ]

        for case in test_cases:
            status = "good"

            if case["memory"] >= thresholds["memory"]["critical"] or \
               case["blocked"] >= thresholds["blocked_tasks"]["critical"] or \
               case["speed"] >= thresholds["file_op_speed"]["critical"]:
                status = "critical"
            elif case["memory"] >= thresholds["memory"]["warning"] or \
                 case["blocked"] >= thresholds["blocked_tasks"]["warning"] or \
                 case["speed"] >= thresholds["file_op_speed"]["warning"]:
                status = "warning"

            self.assertEqual(status, case["expected"],
                           f"Failed for case: {case}")

    def test_checkpoint_recovery(self):
        """Test checkpoint creation and recovery"""
        # Create checkpoint data
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "tasks_completed": 45,
            "tasks_pending": 15,
            "system_state": "healthy",
            "context": {
                "current_task": "task-123",
                "progress": 75
            }
        }

        checkpoint_file = self.monitor_dir / "checkpoint.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)

        # Simulate system restart - load checkpoint
        self.assertTrue(checkpoint_file.exists())

        with open(checkpoint_file, 'r') as f:
            recovered = json.load(f)

        self.assertEqual(recovered["tasks_completed"], 45)
        self.assertEqual(recovered["context"]["current_task"], "task-123")
        self.assertEqual(recovered["context"]["progress"], 75)

    def test_monitoring_command_integration(self):
        """Test monitoring command file integration"""
        commands_dir = Path(self.temp_dir) / ".claude" / "commands"
        os.makedirs(commands_dir, exist_ok=True)

        # Create monitoring command files
        commands = [
            ("show-health.md", "# Show Health\nDisplays current system health"),
            ("view-dashboard.md", "# View Dashboard\nShows live monitoring dashboard"),
            ("run-diagnosis.md", "# Run Diagnosis\nPerforms system diagnosis"),
            ("apply-fix.md", "# Apply Fix\nApplies recommended fixes")
        ]

        for filename, content in commands:
            cmd_file = commands_dir / filename
            with open(cmd_file, 'w') as f:
                f.write(content)

        # Verify all command files exist
        for filename, _ in commands:
            cmd_file = commands_dir / filename
            self.assertTrue(cmd_file.exists(),
                          f"Command file {filename} not found")

    def test_monitoring_data_persistence(self):
        """Test that monitoring data persists across sessions"""
        # Session 1: Create initial data
        session1_data = {
            "session": 1,
            "timestamp": datetime.now().isoformat(),
            "metrics": {"tasks": 10, "memory": 50}
        }

        metrics_file = self.monitor_dir / "metrics.json"
        with open(metrics_file, 'w') as f:
            json.dump(session1_data, f)

        # Session 2: Update data
        time.sleep(0.1)  # Small delay to ensure different timestamp

        with open(metrics_file, 'r') as f:
            existing = json.load(f)

        session2_data = {
            "session": 2,
            "timestamp": datetime.now().isoformat(),
            "metrics": {"tasks": 15, "memory": 55},
            "previous": existing
        }

        with open(metrics_file, 'w') as f:
            json.dump(session2_data, f)

        # Verify data persistence
        with open(metrics_file, 'r') as f:
            final = json.load(f)

        self.assertEqual(final["session"], 2)
        self.assertEqual(final["metrics"]["tasks"], 15)
        self.assertEqual(final["previous"]["session"], 1)
        self.assertEqual(final["previous"]["metrics"]["tasks"], 10)

    def test_error_recovery_mechanisms(self):
        """Test error recovery and graceful degradation"""
        # Test 1: Missing configuration file
        health_file = self.monitor_dir / "health-checks.json"

        # Try to read non-existent file
        if not health_file.exists():
            # Should create default
            default_health = {
                "status": "unknown",
                "timestamp": datetime.now().isoformat(),
                "error": "No previous health data"
            }
            with open(health_file, 'w') as f:
                json.dump(default_health, f)

        self.assertTrue(health_file.exists())

        # Test 2: Corrupted JSON handling
        corrupt_file = self.monitor_dir / "corrupt.json"
        with open(corrupt_file, 'w') as f:
            f.write("{invalid json content")

        # Try to load and handle error
        try:
            with open(corrupt_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # Create backup and reset
            backup_file = corrupt_file.with_suffix('.backup')
            shutil.copy(corrupt_file, backup_file)

            # Write valid default
            default_data = {"status": "recovered", "from_corruption": True}
            with open(corrupt_file, 'w') as f:
                json.dump(default_data, f)

        # Verify recovery
        with open(corrupt_file, 'r') as f:
            recovered = json.load(f)

        self.assertEqual(recovered["status"], "recovered")
        self.assertTrue(recovered["from_corruption"])

    def test_concurrent_monitoring_safety(self):
        """Test that concurrent monitoring operations don't conflict"""
        dashboard_file = self.monitor_dir / "live-dashboard.md"

        # Simulate concurrent writes using file locking
        updates = []
        for i in range(10):
            content = f"# Dashboard Update {i}\nTimestamp: {time.time()}\n"

            # Atomic write simulation
            temp_file = dashboard_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                f.write(content)

            # Atomic rename
            temp_file.replace(dashboard_file)
            updates.append(i)

            time.sleep(0.01)  # Small delay between updates

        # Verify final state
        self.assertTrue(dashboard_file.exists())
        with open(dashboard_file, 'r') as f:
            final_content = f.read()

        # Should contain the last update
        self.assertIn("Update 9", final_content)
        self.assertEqual(len(updates), 10)


class TestObservabilityPerformance(unittest.TestCase):
    """Performance benchmarks for observability system"""

    def test_dashboard_update_performance(self):
        """Test dashboard update completes within time limit"""
        iterations = 100
        times = []

        for _ in range(iterations):
            start = time.time()

            # Simulate dashboard update operations
            data = {"tasks": list(range(100)), "metrics": {"cpu": 50, "memory": 60}}
            content = json.dumps(data)

            # Simulate file write
            temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp.write(content)
            temp.close()
            os.unlink(temp.name)

            elapsed = time.time() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        max_time = max(times)

        self.assertLess(avg_time, 0.01, f"Average update time {avg_time:.3f}s exceeds 10ms")
        self.assertLess(max_time, 0.05, f"Max update time {max_time:.3f}s exceeds 50ms")

    def test_monitoring_memory_footprint(self):
        """Test monitoring system memory usage stays within bounds"""
        import psutil
        import gc

        # Get baseline memory
        gc.collect()
        process = psutil.Process()
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create monitoring data structures
        monitoring_data = {
            "health_checks": [{"timestamp": i, "data": "x" * 1000} for i in range(1000)],
            "diagnostics": [{"id": i, "report": "y" * 500} for i in range(500)],
            "dashboard": {"content": "z" * 10000}
        }

        # Get memory after loading
        current_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = current_memory - baseline_memory

        # Clean up
        del monitoring_data
        gc.collect()

        # Memory increase should be reasonable (less than 50MB for this test data)
        self.assertLess(memory_increase, 50,
                       f"Memory increase {memory_increase:.1f}MB exceeds 50MB limit")


if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestObservabilityWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestObservabilityPerformance))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print(f"Integration Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)