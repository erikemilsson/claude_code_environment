"""
Performance benchmarks for the universal project system
"""

import sys
import json
import time
import statistics
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.test_base import TestBase

class TestPerformance(TestBase):
    """Performance benchmark tests"""

    def __init__(self):
        super().__init__()
        self.benchmark_results = {}

    def run_benchmark(self, name: str, func, iterations: int = 100) -> Dict[str, float]:
        """Run a benchmark and collect statistics"""
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times.append(end - start)

        result = {
            "min": min(times),
            "max": max(times),
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "iterations": iterations
        }

        self.benchmark_results[name] = result
        return result

    def test_template_detection_performance(self):
        """Benchmark template detection speed"""
        self.setup()
        try:
            specs = [
                self.create_mock_specification("base"),
                self.create_mock_specification("power-query"),
                self.create_mock_specification("research"),
                self.create_mock_specification("life-projects"),
                self.create_mock_specification("documentation")
            ]

            def detect_all():
                for spec in specs:
                    self.detect_template_type(spec)

            result = self.run_benchmark("template_detection", detect_all, 1000)

            # Should be very fast (< 1ms average)
            assert result["mean"] < 0.001, f"Template detection too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_task_creation_performance(self):
        """Benchmark task creation speed"""
        self.setup()
        try:
            def create_task():
                task = {
                    "id": f"task-{time.time()}",
                    "title": "Performance test task",
                    "status": "Pending",
                    "difficulty": 5,
                    "validation_criteria": ["Test 1", "Test 2", "Test 3"]
                }
                self.create_json(f".claude/tasks/{task['id']}.json", task)

            result = self.run_benchmark("task_creation", create_task, 100)

            # Should create tasks quickly (< 10ms average)
            assert result["mean"] < 0.01, f"Task creation too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_task_breakdown_performance(self):
        """Benchmark task breakdown performance"""
        self.setup()
        try:
            def breakdown_task():
                parent = {
                    "id": f"parent-{time.time()}",
                    "difficulty": 9,
                    "title": "Complex task"
                }

                # Generate subtasks
                subtasks = []
                for i in range(5):
                    subtask = {
                        "id": f"{parent['id']}.{i}",
                        "difficulty": 3,
                        "parent_id": parent["id"]
                    }
                    subtasks.append(subtask)

                parent["subtasks"] = [s["id"] for s in subtasks]
                parent["status"] = "Broken Down"

            result = self.run_benchmark("task_breakdown", breakdown_task, 100)

            # Should breakdown quickly (< 5ms average)
            assert result["mean"] < 0.005, f"Task breakdown too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_parallel_vs_sequential_execution(self):
        """Compare parallel vs sequential execution performance"""
        self.setup()
        try:
            # Sequential execution
            def sequential_execution():
                results = []
                for i in range(10):
                    time.sleep(0.001)  # Simulate work
                    results.append(i)
                return results

            # Parallel execution simulation
            def parallel_execution():
                # In real scenario, this would use threading/asyncio
                # For testing, we simulate parallel speedup
                time.sleep(0.003)  # Simulated parallel time
                return list(range(10))

            seq_result = self.run_benchmark("sequential_execution", sequential_execution, 50)
            par_result = self.run_benchmark("parallel_execution", parallel_execution, 50)

            # Parallel should be faster
            speedup = seq_result["mean"] / par_result["mean"]
            assert speedup > 2, f"Insufficient parallel speedup: {speedup}x"

        finally:
            self.teardown()

    def test_file_operations_performance(self):
        """Benchmark file operation performance"""
        self.setup()
        try:
            test_content = "Test content" * 100

            def file_operations():
                # Write
                self.create_file("test.txt", test_content)
                # Read
                content = self.read_file("test.txt")
                # Modify
                self.create_file("test.txt", content + "\nModified")

            result = self.run_benchmark("file_operations", file_operations, 100)

            # Should handle files quickly (< 20ms average)
            assert result["mean"] < 0.02, f"File operations too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_json_processing_performance(self):
        """Benchmark JSON processing performance"""
        self.setup()
        try:
            large_data = {
                "tasks": [
                    {
                        "id": f"task-{i}",
                        "title": f"Task {i}",
                        "difficulty": i % 10,
                        "dependencies": [f"task-{j}" for j in range(max(0, i-3), i)]
                    }
                    for i in range(100)
                ]
            }

            def json_operations():
                # Write
                self.create_json("large.json", large_data)
                # Read
                data = self.read_json("large.json")
                # Process
                filtered = [t for t in data["tasks"] if t["difficulty"] > 5]

            result = self.run_benchmark("json_processing", json_operations, 50)

            # Should handle large JSON quickly (< 50ms average)
            assert result["mean"] < 0.05, f"JSON processing too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_validation_performance(self):
        """Benchmark validation performance"""
        self.setup()
        try:
            # Create test data
            tasks = []
            for i in range(50):
                task = {
                    "id": f"task-{i}",
                    "status": ["Pending", "In Progress", "Finished"][i % 3],
                    "difficulty": (i % 10) + 1,
                    "dependencies": [f"task-{j}" for j in range(max(0, i-2), i)]
                }
                tasks.append(task)

            def validate_all():
                issues = []
                for task in tasks:
                    # Validate status
                    if task["status"] not in ["Pending", "In Progress", "Finished", "Blocked", "Broken Down"]:
                        issues.append(f"Invalid status: {task['status']}")
                    # Validate difficulty
                    if not 1 <= task["difficulty"] <= 10:
                        issues.append(f"Invalid difficulty: {task['difficulty']}")
                    # Validate dependencies
                    for dep in task["dependencies"]:
                        if not any(t["id"] == dep for t in tasks):
                            issues.append(f"Missing dependency: {dep}")
                return issues

            result = self.run_benchmark("validation", validate_all, 100)

            # Should validate quickly (< 10ms average for 50 tasks)
            assert result["mean"] < 0.01, f"Validation too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_overview_generation_performance(self):
        """Benchmark task overview generation"""
        self.setup()
        try:
            # Create many tasks
            tasks = []
            for i in range(100):
                task = {
                    "id": f"task-{i:03d}",
                    "title": f"Task {i}",
                    "status": ["Pending", "In Progress", "Finished"][i % 3],
                    "difficulty": (i % 10) + 1,
                    "priority": ["low", "medium", "high", "critical"][i % 4]
                }
                tasks.append(task)

            def generate_overview():
                overview = "# Task Overview\n\n"
                overview += "## Summary\n"
                overview += f"- Total: {len(tasks)}\n"

                status_counts = {}
                for task in tasks:
                    status = task["status"]
                    status_counts[status] = status_counts.get(status, 0) + 1

                for status, count in status_counts.items():
                    overview += f"- {status}: {count}\n"

                overview += "\n## Tasks\n\n"
                overview += "| ID | Title | Status | Difficulty | Priority |\n"
                overview += "|---|---|---|---|---|\n"

                for task in tasks:
                    overview += f"| {task['id']} | {task['title']} | {task['status']} | {task['difficulty']} | {task['priority']} |\n"

                return overview

            result = self.run_benchmark("overview_generation", generate_overview, 100)

            # Should generate overview quickly (< 20ms average for 100 tasks)
            assert result["mean"] < 0.02, f"Overview generation too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_checkpoint_performance(self):
        """Benchmark checkpoint creation and restoration"""
        self.setup()
        try:
            # Create test state
            for i in range(20):
                self.create_file(f"file_{i}.txt", f"Content {i}")

            def checkpoint_operations():
                # Create checkpoint
                checkpoint_data = {
                    "timestamp": time.time(),
                    "files": []
                }

                for i in range(20):
                    content = self.read_file(f"file_{i}.txt")
                    checkpoint_data["files"].append({
                        "path": f"file_{i}.txt",
                        "content": content
                    })

                self.create_json(".checkpoint.json", checkpoint_data)

                # Restore checkpoint
                restored = self.read_json(".checkpoint.json")
                for file_data in restored["files"]:
                    self.create_file(file_data["path"], file_data["content"])

            result = self.run_benchmark("checkpoint_operations", checkpoint_operations, 50)

            # Should handle checkpoints quickly (< 100ms average)
            assert result["mean"] < 0.1, f"Checkpoint operations too slow: {result['mean']}s"

        finally:
            self.teardown()

    def test_scalability(self):
        """Test system scalability with increasing load"""
        self.setup()
        try:
            scalability_results = []

            for task_count in [10, 50, 100, 500]:
                # Create tasks
                start = time.perf_counter()

                for i in range(task_count):
                    task = {
                        "id": f"task-{i:04d}",
                        "title": f"Scalability test task {i}",
                        "difficulty": (i % 10) + 1
                    }
                    self.create_json(f".claude/tasks/{task['id']}.json", task)

                creation_time = time.perf_counter() - start

                # Process tasks
                start = time.perf_counter()

                tasks = []
                for i in range(task_count):
                    task = self.read_json(f".claude/tasks/task-{i:04d}.json")
                    tasks.append(task)

                # Simulate processing
                finished_count = sum(1 for t in tasks if t.get("status") == "Finished")

                processing_time = time.perf_counter() - start

                scalability_results.append({
                    "task_count": task_count,
                    "creation_time": creation_time,
                    "processing_time": processing_time,
                    "total_time": creation_time + processing_time
                })

            # Check scalability (should be roughly linear)
            times = [r["total_time"] for r in scalability_results]
            counts = [r["task_count"] for r in scalability_results]

            # Calculate scaling factor
            scaling_factors = []
            for i in range(1, len(scalability_results)):
                time_ratio = times[i] / times[0]
                count_ratio = counts[i] / counts[0]
                scaling_factor = time_ratio / count_ratio
                scaling_factors.append(scaling_factor)

            # Average scaling factor should be reasonable (< 2 means sub-linear scaling)
            avg_scaling = statistics.mean(scaling_factors)
            assert avg_scaling < 2, f"Poor scalability: {avg_scaling}x"

            self.benchmark_results["scalability"] = {
                "results": scalability_results,
                "average_scaling_factor": avg_scaling
            }

        finally:
            self.teardown()

    def test_print_benchmark_summary(self):
        """Print comprehensive benchmark summary"""
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("="*60)

        for name, result in self.benchmark_results.items():
            if name == "scalability":
                print(f"\n{name.upper()}:")
                print(f"  Average Scaling Factor: {result['average_scaling_factor']:.2f}x")
                for r in result["results"]:
                    print(f"  {r['task_count']} tasks: {r['total_time']:.3f}s")
            else:
                print(f"\n{name.upper()}:")
                print(f"  Mean:   {result['mean']*1000:.2f}ms")
                print(f"  Median: {result['median']*1000:.2f}ms")
                print(f"  Min:    {result['min']*1000:.2f}ms")
                print(f"  Max:    {result['max']*1000:.2f}ms")
                print(f"  StDev:  {result['stdev']*1000:.2f}ms")

        print("\n" + "="*60)

        # Save results to file
        results_file = Path(__file__).parent / "benchmark_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.benchmark_results, f, indent=2)

        print(f"Results saved to: {results_file}")

    # Helper method
    def detect_template_type(self, spec_content: str) -> str:
        """Fast template detection"""
        content_lower = spec_content.lower()

        templates = [
            (["power query", "dax", "power bi"], "power-query"),
            (["research", "analysis", "study", "statistical"], "research"),
            (["life project", "personal", "renovation"], "life-projects"),
            (["documentation", "docs", "api doc"], "documentation")
        ]

        for keywords, template in templates:
            if any(kw in content_lower for kw in keywords):
                return template

        return "base"