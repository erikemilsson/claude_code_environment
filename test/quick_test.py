#!/usr/bin/env python3
"""
Quick test to validate the Universal Project structure
Run this for a rapid check that everything is working
"""

import os
import sys
import json
from pathlib import Path

def check_structure():
    """Check that key directories and files exist"""
    print("Checking Universal Project structure...")

    required_paths = [
        "CLAUDE.md",
        "README.md",
        ".claude",
        ".claude/commands",
        ".claude/context",
        ".claude/tasks",
        ".claude/reference",
        "templates",
        "templates/power-query",
        "templates/research-analysis",
        "templates/life-projects",
        "templates/documentation-content",
        "components",
        "components/task-management",
        "components/validation-gates",
        "components/pattern-library",
        "test",
        "test/unit",
        "test/integration",
        "test/e2e",
        "test/benchmarks"
    ]

    project_root = Path(__file__).parent.parent
    missing = []

    for path_str in required_paths:
        path = project_root / path_str
        if not path.exists():
            missing.append(path_str)
            print(f"  ✗ Missing: {path_str}")
        else:
            print(f"  ✓ Found: {path_str}")

    return len(missing) == 0

def check_templates():
    """Verify template structures"""
    print("\nChecking templates...")

    project_root = Path(__file__).parent.parent
    templates_dir = project_root / "templates"

    templates = ["power-query", "research-analysis", "life-projects", "documentation-content"]
    all_good = True

    for template in templates:
        template_path = templates_dir / template
        if template_path.exists():
            # Check for README
            readme = template_path / "README.md"
            if readme.exists():
                print(f"  ✓ {template}: OK")
            else:
                print(f"  ⚠ {template}: Missing README.md")
                all_good = False
        else:
            print(f"  ✗ {template}: Not found")
            all_good = False

    return all_good

def check_test_suite():
    """Verify test suite is set up"""
    print("\nChecking test suite...")

    test_root = Path(__file__).parent

    test_files = [
        "run_tests.py",
        "utils/test_base.py",
        "unit/test_template_validation.py",
        "unit/test_task_management.py",
        "unit/test_command_execution.py",
        "integration/test_full_workflow.py",
        "e2e/test_universal_project.py",
        "benchmarks/test_performance.py"
    ]

    all_found = True
    for file_path in test_files:
        full_path = test_root / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ Missing: {file_path}")
            all_found = False

    return all_found

def run_simple_test():
    """Run a simple functionality test"""
    print("\nRunning simple functionality test...")

    try:
        # Test 1: Template detection
        test_specs = {
            "power query dax": "power-query",
            "research analysis": "research",
            "life project": "life-projects",
            "api documentation": "documentation",
            "python web app": "base"
        }

        for spec, expected in test_specs.items():
            detected = detect_template(spec)
            if detected == expected:
                print(f"  ✓ Template detection: '{spec}' → {detected}")
            else:
                print(f"  ✗ Template detection failed: '{spec}' → {detected} (expected {expected})")
                return False

        # Test 2: Task validation
        valid_task = {
            "id": "test-001",
            "title": "Test task",
            "status": "Pending",
            "difficulty": 5
        }

        if validate_task(valid_task):
            print(f"  ✓ Task validation: Valid task accepted")
        else:
            print(f"  ✗ Task validation: Valid task rejected")
            return False

        invalid_task = {
            "id": "test-002",
            "status": "InvalidStatus",
            "difficulty": 15
        }

        if not validate_task(invalid_task):
            print(f"  ✓ Task validation: Invalid task rejected")
        else:
            print(f"  ✗ Task validation: Invalid task accepted")
            return False

        return True

    except Exception as e:
        print(f"  ✗ Error during test: {e}")
        return False

def detect_template(spec_content: str) -> str:
    """Simple template detection"""
    content_lower = spec_content.lower()

    if any(term in content_lower for term in ["power query", "dax", "power bi"]):
        return "power-query"
    elif any(term in content_lower for term in ["research", "analysis", "study"]):
        return "research"
    elif any(term in content_lower for term in ["life project", "personal"]):
        return "life-projects"
    elif any(term in content_lower for term in ["documentation", "docs", "api doc"]):
        return "documentation"
    else:
        return "base"

def validate_task(task: dict) -> bool:
    """Simple task validation"""
    # Check required fields
    if "id" not in task:
        return False

    # Check status
    valid_statuses = ["Pending", "In Progress", "Finished", "Blocked", "Broken Down"]
    if task.get("status") not in valid_statuses:
        return False

    # Check difficulty
    difficulty = task.get("difficulty", 0)
    if not 1 <= difficulty <= 10:
        return False

    return True

def main():
    """Run all quick tests"""
    print("="*60)
    print("UNIVERSAL PROJECT QUICK TEST")
    print("="*60)

    results = []

    # Run checks
    results.append(("Structure", check_structure()))
    results.append(("Templates", check_templates()))
    results.append(("Test Suite", check_test_suite()))
    results.append(("Functionality", run_simple_test()))

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {name}: {status}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n🎉 All quick tests passed!")
        print("\nFor comprehensive testing, run: python test/run_tests.py")
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
        print("\nFor detailed testing, run: python test/run_tests.py -v")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())