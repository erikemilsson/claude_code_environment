#!/usr/bin/env python3
"""
Template Testing Framework - Automated tests for template generation

Features:
- Test template detection accuracy
- Validate file generation completeness
- Check cross-references
- Test task breakdown scenarios
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List
import sys

# Import modules to test
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import BootstrapAutomation
from task_manager import TaskManager


class TestTemplateDetection:
    """Test template detection accuracy"""

    def test_power_query_detection(self):
        """Test Power Query template detection"""
        bootstrap = BootstrapAutomation()
        spec = """
        # Power BI Dashboard Project
        We need to create DAX measures and Power Query transformations
        for our data model. The M language scripts will process Excel files.
        """
        template, scores = bootstrap.detect_template(spec)
        assert template == "power-query"
        assert scores["power-query"] > scores["base"]

    def test_research_template_detection(self):
        """Test research template detection"""
        bootstrap = BootstrapAutomation()
        spec = """
        # Research Study on Market Trends
        This analysis will investigate hypothesis about consumer behavior
        through data analysis and statistical findings.
        """
        template, scores = bootstrap.detect_template(spec)
        assert template == "research"

    def test_base_template_fallback(self):
        """Test fallback to base template"""
        bootstrap = BootstrapAutomation()
        spec = "Simple project without specific keywords"
        template, scores = bootstrap.detect_template(spec)
        assert template == "base"


class TestFileGeneration:
    """Test file generation completeness"""

    def test_base_structure_generation(self):
        """Test base structure creation"""
        bootstrap = BootstrapAutomation()
        structure = bootstrap.generate_base_structure("base")

        required_files = [
            ".claude/commands/complete-task.md",
            ".claude/commands/breakdown.md",
            ".claude/commands/sync-tasks.md",
            ".claude/context/overview.md",
            ".claude/tasks/task-overview.md",
            "CLAUDE.md",
            "README.md"
        ]

        for file_path in required_files:
            assert file_path in structure

    def test_power_query_additions(self):
        """Test Power Query specific files"""
        bootstrap = BootstrapAutomation()
        structure = bootstrap.generate_base_structure("power-query")

        assert ".claude/context/phase-0-checklist.md" in structure
        assert ".claude/reference/llm-pitfalls.md" in structure


class TestTaskBreakdown:
    """Test task breakdown scenarios"""

    def test_initial_task_creation(self):
        """Test initial task generation"""
        bootstrap = BootstrapAutomation()
        indicators = {
            "project_name": "Test Project",
            "requirements": [
                "Build user authentication",
                "Create data pipeline",
                "Implement dashboard"
            ],
            "technologies": ["python", "postgresql"],
            "complexity": "medium"
        }

        tasks = bootstrap.create_initial_tasks(indicators, "base")

        assert len(tasks) >= 3
        assert tasks[0]["title"] == "Initial Project Setup"
        assert all(task["status"] == "Pending" for task in tasks)

    def test_high_difficulty_task_creation(self):
        """Test creation of high-difficulty tasks"""
        bootstrap = BootstrapAutomation()
        indicators = {
            "project_name": "Complex System",
            "requirements": [
                "Integrate complex distributed systems",
                "Advanced machine learning pipeline"
            ],
            "technologies": [],
            "complexity": "high"
        }

        tasks = bootstrap.create_initial_tasks(indicators, "base")

        # Should have at least one high-difficulty task
        high_diff_tasks = [t for t in tasks if t["difficulty"] >= 7]
        assert len(high_diff_tasks) > 0


class TestIntegration:
    """Integration tests"""

    def test_full_bootstrap_workflow(self):
        """Test complete bootstrap workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create spec file
            spec_path = Path(tmpdir) / "spec.md"
            spec_content = """
            # Test Project

            ## Requirements
            - Build API endpoints
            - Add authentication
            - Create documentation
            """
            with open(spec_path, 'w') as f:
                f.write(spec_content)

            # Run bootstrap
            bootstrap = BootstrapAutomation()
            results = bootstrap.bootstrap_environment(str(spec_path), tmpdir)

            # Verify results
            assert results["template_detected"] in bootstrap.template_patterns
            assert len(results["files_created"]) > 0
            assert results["tasks_created"] > 0
            assert len(results["errors"]) == 0

            # Verify files exist
            claude_dir = Path(tmpdir) / ".claude"
            assert claude_dir.exists()
            assert (claude_dir / "commands").exists()
            assert (claude_dir / "tasks").exists()


def run_tests():
    """Run all tests without pytest"""
    test_classes = [
        TestTemplateDetection(),
        TestFileGeneration(),
        TestTaskBreakdown(),
        TestIntegration()
    ]

    passed = 0
    failed = 0
    errors = []

    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\nRunning {class_name}...")

        for method_name in dir(test_class):
            if method_name.startswith("test_"):
                method = getattr(test_class, method_name)
                try:
                    method()
                    print(f"  ✓ {method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed += 1
                    errors.append((class_name, method_name, str(e)))
                except Exception as e:
                    print(f"  ✗ {method_name}: Unexpected error: {e}")
                    failed += 1
                    errors.append((class_name, method_name, str(e)))

    print(f"\n{'=' * 50}")
    print(f"Test Results: {passed} passed, {failed} failed")

    if errors:
        print("\nFailed tests:")
        for class_name, method, error in errors:
            print(f"  {class_name}.{method}: {error}")

    return failed == 0


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Template Testing Framework")
    parser.add_argument("--pytest", action="store_true",
                       help="Run with pytest instead of built-in runner")
    parser.add_argument("--coverage", action="store_true",
                       help="Run with coverage (requires pytest)")

    args = parser.parse_args()

    if args.pytest:
        # Run with pytest
        import subprocess
        cmd = ["pytest", __file__, "-v"]
        if args.coverage:
            cmd.extend(["--cov=.", "--cov-report=term"])
        subprocess.run(cmd)
    else:
        # Run with built-in test runner
        success = run_tests()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()