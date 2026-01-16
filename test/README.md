# Universal Project Test Suite

Comprehensive test suite for the Claude Code Universal Project template system.

## Overview

This test suite provides complete coverage for the Universal Project structure, including:
- Template validation and generation
- Task management lifecycle
- Command execution workflows
- Agent system functionality
- Integration between components
- Performance benchmarks
- End-to-end scenarios

## Structure

```
test/
├── README.md              # This file
├── run_tests.py          # Main test runner
├── utils/                # Test utilities
│   └── test_base.py      # Base test class with helpers
├── unit/                 # Unit tests
│   ├── test_template_validation.py
│   ├── test_task_management.py
│   └── test_command_execution.py
├── integration/          # Integration tests
│   └── test_full_workflow.py
├── e2e/                  # End-to-end tests
│   └── test_universal_project.py
├── benchmarks/           # Performance tests
│   └── test_performance.py
└── fixtures/             # Test data and fixtures

```

## Running Tests

### Quick Start

Run all tests:
```bash
python test/run_tests.py
```

Run with verbose output:
```bash
python test/run_tests.py -v
```

### Run Specific Test Categories

```bash
# Unit tests only
python test/run_tests.py -c unit

# Integration tests only
python test/run_tests.py -c integration

# End-to-end tests only
python test/run_tests.py -c e2e

# Performance benchmarks only
python test/run_tests.py -c benchmarks
```

### List Available Categories

```bash
python test/run_tests.py --list
```

## Test Categories

### Unit Tests (`unit/`)

Tests individual components in isolation:

- **Template Validation** (`test_template_validation.py`)
  - Template structure validation
  - Template detection from specifications
  - File content validation
  - Component integration

- **Task Management** (`test_task_management.py`)
  - Task creation and lifecycle
  - Status transitions
  - Task breakdown for high difficulty
  - Auto-completion of parent tasks
  - Dependency management
  - Belief and momentum tracking

- **Command Execution** (`test_command_execution.py`)
  - Bootstrap command workflow
  - Complete-task workflow
  - Breakdown command logic
  - Sync-tasks functionality
  - Validation gates

### Integration Tests (`integration/`)

Tests how components work together:

- **Full Workflow** (`test_full_workflow.py`)
  - Project bootstrap from specification
  - Complete task lifecycle
  - Agent workflow execution
  - Validation gates throughout workflow
  - Pattern library usage
  - Checkpoint and recovery
  - Error handling and recovery
  - Parallel execution
  - Gemini API integration

### End-to-End Tests (`e2e/`)

Complete scenario testing:

- **Universal Project** (`test_universal_project.py`)
  - Power Query project complete workflow
  - Research project complete workflow
  - Life project complete workflow
  - Documentation project complete workflow
  - Multi-template integration
  - Error handling scenarios
  - Agent system E2E
  - Validation gates E2E
  - Belief tracking E2E
  - Complete universal workflow

### Performance Benchmarks (`benchmarks/`)

Performance and scalability testing:

- **Performance** (`test_performance.py`)
  - Template detection speed
  - Task creation performance
  - Task breakdown performance
  - Parallel vs sequential execution
  - File operations performance
  - JSON processing speed
  - Validation performance
  - Overview generation speed
  - Checkpoint operations
  - System scalability

## Test Coverage

### Templates Tested
- ✅ Base template
- ✅ Power Query template
- ✅ Research/Analysis template
- ✅ Life Projects template
- ✅ Documentation template

### Features Tested
- ✅ Template auto-detection
- ✅ Project bootstrapping
- ✅ Task management (create, update, breakdown, complete)
- ✅ Command execution
- ✅ Validation gates (pre/post execution)
- ✅ Agent system (Environment Architect, Task Orchestrator, Execution Guardian)
- ✅ Belief tracking
- ✅ Momentum tracking
- ✅ Checkpoint/recovery
- ✅ Error handling
- ✅ Parallel execution
- ✅ Performance optimization

## Test Results

Test results are saved to `test_results.json` after each run, including:
- Timestamp
- Execution time
- Pass/fail counts
- Detailed failure information

Performance benchmark results are saved to `benchmarks/benchmark_results.json`.

## Writing New Tests

### 1. Create Test File

Create a new file in the appropriate directory:
```python
# test/unit/test_new_feature.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.test_base import TestBase

class TestNewFeature(TestBase):
    def test_something(self):
        self.setup()
        try:
            # Your test code here
            assert True == True
        finally:
            self.teardown()
```

### 2. Use TestBase Utilities

The `TestBase` class provides helpful utilities:

```python
# File operations
self.create_file("path/to/file.txt", "content")
self.read_file("path/to/file.txt")
self.create_json("data.json", {"key": "value"})
self.read_json("data.json")

# Assertions
self.assert_file_exists("path/to/file.txt")
self.assert_file_contains("file.txt", "expected content")
self.assert_json_has_keys("data.json", ["key1", "key2"])
self.assert_directory_structure(expected_dict)

# Mock specifications
spec = self.create_mock_specification("power-query")
```

### 3. Follow Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

## Performance Targets

Based on benchmarks, the system should meet these targets:

- Template detection: < 1ms average
- Task creation: < 10ms average
- Task breakdown: < 5ms average
- File operations: < 20ms average
- JSON processing (100 tasks): < 50ms average
- Validation (50 tasks): < 10ms average
- Overview generation (100 tasks): < 20ms average
- Checkpoint operations: < 100ms average

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run tests
        run: python test/run_tests.py
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test/test_results.json
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure you're running tests from the project root
2. **File not found**: Tests use temporary directories; check `test_base.py` setup
3. **Performance failures**: May vary by system; adjust thresholds if needed

### Debug Mode

For debugging specific tests:
```python
# Add to test method
import pdb; pdb.set_trace()
```

Or run with Python debugger:
```bash
python -m pdb test/run_tests.py
```

## Contributing

When adding new features to the Universal Project:

1. Add corresponding unit tests
2. Update integration tests if needed
3. Add E2E scenario if it's a major feature
4. Run full test suite before committing
5. Update this README if adding new test categories

## Test Philosophy

Our testing approach follows these principles:

1. **Comprehensive Coverage**: Every feature should have tests
2. **Fast Feedback**: Unit tests run quickly for rapid development
3. **Real-World Scenarios**: E2E tests validate actual usage patterns
4. **Performance Awareness**: Benchmarks ensure system remains fast
5. **Maintainability**: Tests should be clear and easy to update

## License

Same as parent project.