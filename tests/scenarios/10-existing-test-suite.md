# Scenario 10: Existing Test Suite Integration

Verify that verify-agent discovers and uses an existing pytest setup rather than creating redundant verification.

## Context

Many real projects already have a mature test suite before the template is applied. The verify-agent must integrate with the existing test infrastructure — running the project's own tests, respecting its configuration — rather than inventing new verification from scratch or duplicating coverage.

## State

- Spec exists with 3 tasks, task-1 in progress (implement-agent just completed it)
- Project has `pyproject.toml` with `[tool.pytest.ini_options]` configured (testpaths, markers, etc.)
- `tests/` directory contains 11 test files with existing coverage
- `requirements.txt` includes pytest, pytest-cov
- Task-1 modified `src/database/models.py` and added `src/database/queries.py`

## Trace 10A: Test infrastructure discovery

- **Path:** verify-agent invoked after implement-agent completes task-1
- verify-agent discovers the project's existing test configuration
- Identifies the test directory and existing test files

### Expected

- verify-agent uses the project's pytest configuration, not a custom command
- Runs `pytest` (or `python -m pytest`) respecting the project's `pyproject.toml` settings
- Reports test results referencing the project's actual test file paths

### Pass criteria

- [ ] Existing test infrastructure is discovered before any verification begins
- [ ] Test command matches what the project already uses
- [ ] `pyproject.toml` test configuration is respected (markers, testpaths, etc.)

### Fail indicators

- verify-agent runs `pytest` with custom flags that override project config
- verify-agent creates a new test runner script instead of using pytest
- Test discovery ignores the project's configured testpaths

---

## Trace 10B: No duplicate test files created

- **Path:** verify-agent checks whether existing tests already cover new code
- Task-1 added new source files to a module that already has test coverage

### Expected

- verify-agent does NOT create `tests/test_queries.py` or similar if existing tests already cover the module
- If new test coverage is genuinely needed, verify-agent notes the gap but does not auto-create test files
- Verification output references existing test results, not new synthetic checks

### Pass criteria

- [ ] No duplicate test files created
- [ ] Existing test coverage is acknowledged in verification output
- [ ] If gaps exist, they are reported as findings, not silently filled

### Fail indicators

- New test files appear that overlap with existing `test_database.py` coverage
- verify-agent ignores existing tests and creates its own verification suite
- Verification report doesn't mention the existing test results

---

## Trace 10C: Test failure reporting

- **Path:** verify-agent runs tests and some fail due to task-1 changes
- pytest runs and 2 of 45 tests fail due to task-1 changes

### Expected

- Failures reported with correct file paths and line numbers from pytest output
- verify-agent marks task-1 as failing verification with specific failure details
- Dashboard surfaces the failures in the attention section

### Pass criteria

- [ ] Test failures are reported with correct file paths and line numbers
- [ ] Failure details are specific enough for the implement-agent to act on
- [ ] Task status reflects the verification failure

### Fail indicators

- Failures reported without file paths or with incorrect references
- verify-agent passes the task despite test failures
- Generic "tests failed" message with no actionable detail
