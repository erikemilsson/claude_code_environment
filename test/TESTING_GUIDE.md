# Testing Guide for Universal Project

This guide explains how to test the Universal Project template system comprehensively.

## Quick Validation

For a rapid check that everything is working:

```bash
python3 test/quick_test.py
```

This validates:
- Directory structure exists
- All templates are present
- Test suite is complete
- Basic functionality works

## Comprehensive Testing

### 1. Run All Tests

```bash
python3 test/run_tests.py
```

This runs the complete test suite including unit, integration, E2E, and performance tests.

### 2. Test Specific Components

#### Template System
Test template detection and generation:
```bash
python3 test/run_tests.py -c unit
```

Key tests:
- `test_template_validation.py` - Template structure and detection
- Auto-detection from specifications
- Component integration

#### Task Management
Test task lifecycle:
```bash
python3 -m pytest test/unit/test_task_management.py -v
```

Tests cover:
- Task creation and status transitions
- Task breakdown (difficulty ≥ 7)
- Auto-completion of parent tasks
- Dependency management
- Belief and momentum tracking

#### Command Execution
Test command workflows:
```bash
python3 -m pytest test/unit/test_command_execution.py -v
```

Tests cover:
- Bootstrap command
- Complete-task workflow
- Breakdown logic
- Sync-tasks functionality
- Validation gates

### 3. Integration Testing

Test component interactions:
```bash
python3 test/run_tests.py -c integration
```

Key scenarios:
- Complete project bootstrap from spec
- Task lifecycle with breakdowns
- Agent system coordination
- Checkpoint and recovery
- Error handling

### 4. End-to-End Testing

Test complete workflows:
```bash
python3 test/run_tests.py -c e2e
```

Scenarios tested:
- Power Query project (data transformation)
- Research project (analysis workflow)
- Life project (personal planning)
- Documentation project (API docs)
- Multi-template integration

### 5. Performance Testing

Benchmark system performance:
```bash
python3 test/run_tests.py -c benchmarks
```

Metrics tracked:
- Template detection speed (< 1ms)
- Task creation speed (< 10ms)
- Parallel vs sequential execution
- System scalability

## Manual Testing Scenarios

### Scenario 1: Create Power Query Project

1. Create a specification file:
```markdown
# Power BI Dashboard

## Requirements
- Import Excel data
- Transform with Power Query
- Create DAX measures
```

2. Bootstrap the project:
```bash
# In Claude Code
Create environment from spec: /path/to/spec.md
```

3. Verify structure:
- Check `.claude/context/llm-pitfalls.md` exists
- Check `.claude/commands/validate-query.md` exists
- Verify `.vscode/settings.json` created

### Scenario 2: Task Management Flow

1. Create a complex task (difficulty 8)
2. Verify it gets broken down into subtasks
3. Complete all subtasks
4. Verify parent auto-completes
5. Run sync-tasks to update overview

### Scenario 3: Error Recovery

1. Create invalid task (difficulty 15)
2. Verify error is caught
3. Create checkpoint
4. Make changes
5. Rollback to checkpoint
6. Verify state restored

## Testing New Features

When adding new features:

### 1. Write Unit Test First

```python
# test/unit/test_new_feature.py
from utils.test_base import TestBase

class TestNewFeature(TestBase):
    def test_feature_works(self):
        self.setup()
        try:
            # Test implementation
            result = self.new_feature_function()
            assert result == expected
        finally:
            self.teardown()
```

### 2. Add Integration Test

```python
# test/integration/test_full_workflow.py
def test_new_feature_integration(self):
    # Test with other components
    pass
```

### 3. Update E2E Test

```python
# test/e2e/test_universal_project.py
def test_workflow_with_new_feature(self):
    # Test in complete scenario
    pass
```

### 4. Run Full Suite

```bash
python3 test/run_tests.py -v
```

## Debugging Failed Tests

### Enable Verbose Output

```bash
python3 test/run_tests.py -v
```

### Run Single Test File

```bash
python3 test/unit/test_task_management.py
```

### Add Debug Breakpoints

```python
import pdb; pdb.set_trace()
```

### Check Test Results

Results saved to `test/test_results.json`:
```bash
cat test/test_results.json | python3 -m json.tool
```

## Performance Monitoring

### Run Benchmarks

```bash
python3 test/benchmarks/test_performance.py
```

### Check Results

```bash
cat test/benchmarks/benchmark_results.json | python3 -m json.tool
```

### Performance Targets

- Template detection: < 1ms
- Task creation: < 10ms
- File operations: < 20ms
- JSON processing (100 tasks): < 50ms
- Overview generation (100 tasks): < 20ms

## Continuous Testing

### Pre-Commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 test/quick_test.py || exit 1
```

### GitHub Actions

```yaml
name: Test Universal Project

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: python3 test/run_tests.py
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-results
          path: test/test_results.json
```

## Test Coverage Goals

Aim for:
- 100% template coverage
- 100% command coverage
- 90%+ task management coverage
- 80%+ integration scenarios
- All critical paths tested E2E

## Troubleshooting

### Import Errors
- Run from project root
- Check Python path includes test/utils

### File Not Found
- Tests use temp directories
- Check setup() creates proper structure

### Performance Failures
- May vary by system
- Adjust thresholds if needed
- Run benchmarks in isolation

### Template Detection Issues
- Check keywords in specifications
- Verify detection logic matches templates

## Summary

The Universal Project test suite ensures:
1. **Correctness** - All features work as designed
2. **Performance** - System remains fast
3. **Reliability** - Error handling works
4. **Scalability** - Handles increasing load
5. **Maintainability** - Easy to test new features

Run tests frequently during development to catch issues early!