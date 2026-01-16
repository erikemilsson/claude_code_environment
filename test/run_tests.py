#!/usr/bin/env python3
"""
Universal Project Test Suite Runner
Tests the Claude Code environment template system comprehensively
"""

import sys
import json
import os
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import importlib.util
import argparse
import time

# Test categories
TEST_CATEGORIES = {
    'unit': 'Unit tests for individual components',
    'integration': 'Integration tests for component interactions',
    'e2e': 'End-to-end tests for complete workflows',
    'benchmarks': 'Performance benchmarks'
}

class TestRunner:
    def __init__(self, verbose: bool = False, filter_category: str = None):
        self.verbose = verbose
        self.filter_category = filter_category
        self.results = {
            'passed': [],
            'failed': [],
            'skipped': [],
            'errors': []
        }
        self.start_time = None
        self.test_root = Path(__file__).parent

    def load_test_module(self, test_file: Path):
        """Dynamically load a test module"""
        spec = importlib.util.spec_from_file_location(
            test_file.stem,
            test_file
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[test_file.stem] = module
        spec.loader.exec_module(module)
        return module

    def discover_tests(self) -> List[Path]:
        """Discover all test files"""
        tests = []

        if self.filter_category:
            categories = [self.filter_category]
        else:
            categories = TEST_CATEGORIES.keys()

        for category in categories:
            category_path = self.test_root / category
            if category_path.exists():
                tests.extend(category_path.glob('test_*.py'))

        return sorted(tests)

    def run_test_file(self, test_file: Path) -> Tuple[int, int, int]:
        """Run all tests in a single file"""
        passed = failed = errors = 0

        try:
            module = self.load_test_module(test_file)

            # Find all test classes and functions
            for attr_name in dir(module):
                if attr_name.startswith('Test'):
                    test_class = getattr(module, attr_name)
                    if callable(test_class):
                        instance = test_class()

                        # Run all test methods
                        for method_name in dir(instance):
                            if method_name.startswith('test_'):
                                method = getattr(instance, method_name)
                                if callable(method):
                                    test_name = f"{test_file.stem}::{attr_name}::{method_name}"

                                    try:
                                        if self.verbose:
                                            print(f"  Running {method_name}...", end=' ')

                                        method()

                                        if self.verbose:
                                            print("✓")

                                        self.results['passed'].append(test_name)
                                        passed += 1

                                    except AssertionError as e:
                                        if self.verbose:
                                            print(f"✗ {str(e)}")

                                        self.results['failed'].append({
                                            'test': test_name,
                                            'error': str(e),
                                            'traceback': traceback.format_exc()
                                        })
                                        failed += 1

                                    except Exception as e:
                                        if self.verbose:
                                            print(f"E {str(e)}")

                                        self.results['errors'].append({
                                            'test': test_name,
                                            'error': str(e),
                                            'traceback': traceback.format_exc()
                                        })
                                        errors += 1

                elif attr_name.startswith('test_'):
                    # Standalone test function
                    test_func = getattr(module, attr_name)
                    if callable(test_func):
                        test_name = f"{test_file.stem}::{attr_name}"

                        try:
                            if self.verbose:
                                print(f"  Running {attr_name}...", end=' ')

                            test_func()

                            if self.verbose:
                                print("✓")

                            self.results['passed'].append(test_name)
                            passed += 1

                        except AssertionError as e:
                            if self.verbose:
                                print(f"✗ {str(e)}")

                            self.results['failed'].append({
                                'test': test_name,
                                'error': str(e),
                                'traceback': traceback.format_exc()
                            })
                            failed += 1

                        except Exception as e:
                            if self.verbose:
                                print(f"E {str(e)}")

                            self.results['errors'].append({
                                'test': test_name,
                                'error': str(e),
                                'traceback': traceback.format_exc()
                            })
                            errors += 1

        except Exception as e:
            print(f"Error loading test file {test_file}: {e}")
            self.results['errors'].append({
                'test': str(test_file),
                'error': f"Failed to load: {str(e)}",
                'traceback': traceback.format_exc()
            })
            errors += 1

        return passed, failed, errors

    def run(self) -> bool:
        """Run all discovered tests"""
        self.start_time = time.time()

        tests = self.discover_tests()

        if not tests:
            print("No tests found!")
            return False

        print(f"\n{'='*60}")
        print(f"Running {len(tests)} test file(s)")
        if self.filter_category:
            print(f"Category filter: {self.filter_category}")
        print(f"{'='*60}\n")

        total_passed = total_failed = total_errors = 0

        for test_file in tests:
            category = test_file.parent.name
            print(f"[{category}] {test_file.name}")

            passed, failed, errors = self.run_test_file(test_file)

            total_passed += passed
            total_failed += failed
            total_errors += errors

            if not self.verbose:
                summary = []
                if passed: summary.append(f"{passed} passed")
                if failed: summary.append(f"{failed} failed")
                if errors: summary.append(f"{errors} errors")
                print(f"  {', '.join(summary)}")

            print()

        self.print_results(total_passed, total_failed, total_errors)
        self.save_results()

        return total_failed == 0 and total_errors == 0

    def print_results(self, passed: int, failed: int, errors: int):
        """Print test results summary"""
        elapsed = time.time() - self.start_time

        print(f"{'='*60}")
        print("TEST RESULTS")
        print(f"{'='*60}")
        print(f"Passed:  {passed}")
        print(f"Failed:  {failed}")
        print(f"Errors:  {errors}")
        print(f"Total:   {passed + failed + errors}")
        print(f"Time:    {elapsed:.2f}s")
        print(f"{'='*60}")

        if self.results['failed']:
            print("\nFAILED TESTS:")
            for failure in self.results['failed']:
                print(f"\n  {failure['test']}")
                print(f"    {failure['error']}")
                if self.verbose:
                    print(f"    {failure['traceback']}")

        if self.results['errors']:
            print("\nERRORS:")
            for error in self.results['errors']:
                print(f"\n  {error['test']}")
                print(f"    {error['error']}")
                if self.verbose:
                    print(f"    {error['traceback']}")

    def save_results(self):
        """Save test results to JSON file"""
        results_file = self.test_root / 'test_results.json'

        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'elapsed_time': time.time() - self.start_time,
                'filter': self.filter_category,
                'passed': len(self.results['passed']),
                'failed': len(self.results['failed']),
                'errors': len(self.results['errors']),
                'details': self.results
            }, f, indent=2)

        print(f"\nResults saved to: {results_file}")

def main():
    parser = argparse.ArgumentParser(description='Run Universal Project tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('-c', '--category', choices=list(TEST_CATEGORIES.keys()),
                        help='Run only tests in specified category')
    parser.add_argument('--list', action='store_true',
                        help='List available test categories')

    args = parser.parse_args()

    if args.list:
        print("\nAvailable test categories:")
        for cat, desc in TEST_CATEGORIES.items():
            print(f"  {cat}: {desc}")
        return

    runner = TestRunner(verbose=args.verbose, filter_category=args.category)
    success = runner.run()

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()