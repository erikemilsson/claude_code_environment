<!-- Type: Direct Execution -->
<!-- Based on: Anthropic Claude Code Best Practices -->

# Test-Driven Development Workflow

## Purpose
Implement features using strict TDD methodology: write failing tests first, then implement code to make them pass, with anti-overfitting verification.

## When to Use
- New feature implementation
- Bug fixes (write test that reproduces bug first)
- Refactoring with confidence
- API design (tests define contract)
- When code correctness is critical

## Process

### Phase 1: WRITE TESTS FIRST

**Goal:** Define expected behavior before implementation.

```markdown
TEST DESIGN PRINCIPLES:
□ Test behavior, not implementation
□ Avoid mocks unless essential (prefer real dependencies)
□ Cover edge cases and error conditions
□ Write descriptive test names (describe expected behavior)
□ Keep tests independent and isolated
```

**Actions:**
1. ANALYZE requirements/bug report
2. IDENTIFY test cases (happy path + edge cases)
3. WRITE test file with all test cases
4. INCLUDE assertions for expected behavior
5. AVOID implementation details in tests

**Test Types to Consider:**
```markdown
PRIORITY ORDER:
1. Unit tests - Core logic isolation
2. Integration tests - Component interaction
3. End-to-end tests - Full user flows (sparingly)

AVOID:
- Excessive mocking (hides integration issues)
- Testing private methods directly
- Brittle tests tied to implementation
```

### Phase 2: VERIFY TESTS FAIL

**Goal:** Confirm tests are actually testing something.

```markdown
FAILURE VERIFICATION:
□ All new tests fail (not error, but assertion failure)
□ Failure messages are clear and helpful
□ Tests fail for the right reason
□ No tests accidentally passing
```

**Actions:**
1. RUN test suite
2. VERIFY each new test fails
3. CHECK failure message clarity
4. FIX any tests that pass prematurely

**Red Flag:** If a test passes before implementation, either:
- Test is wrong
- Feature already exists
- Test isn't testing what you think

### Phase 3: COMMIT TESTS

**Goal:** Lock in test contract before implementation.

```markdown
COMMIT MESSAGE PATTERN:
"test: add tests for [feature/bug]

- Test case 1: [description]
- Test case 2: [description]
- Expected to fail until implementation complete

Part of #[issue-number]"
```

**Actions:**
1. REVIEW tests one more time
2. COMMIT tests separately from implementation
3. PUSH to create accountability

### Phase 4: IMPLEMENT UNTIL GREEN

**Goal:** Write minimum code to make tests pass.

```markdown
IMPLEMENTATION PRINCIPLES:
□ Write simplest code that passes tests
□ Don't over-engineer ahead of tests
□ Run tests frequently (after each change)
□ Stop when tests pass (resist gold-plating)
```

**Actions:**
1. IMPLEMENT incrementally
2. RUN tests after each significant change
3. DEBUG failures using test output
4. STOP when all tests pass
5. AVOID adding untested functionality

**Iterative Cycle:**
```
Write code → Run tests → Fix failures → Repeat until green
```

### Phase 5: VERIFY NO OVERFITTING

**Goal:** Ensure implementation is general, not test-specific.

```markdown
OVERFITTING INDICATORS:
□ Hardcoded values matching test data
□ Conditional logic only triggered by test cases
□ Implementation that would fail on different inputs
□ Magic numbers that match test assertions
```

**Actions:**
1. REVIEW implementation for test-specific code
2. ADD additional test cases with different data
3. USE property-based testing if available
4. SPAWN verification subagent (if available):
   ```
   "Review this implementation for overfitting.
   Tests are in [test-file]. Implementation in [impl-file].
   Check if implementation would work with different inputs."
   ```

### Phase 6: REFACTOR (Green to Green)

**Goal:** Improve code quality while tests stay green.

```markdown
REFACTORING CHECKLIST:
□ Extract common patterns
□ Improve naming
□ Remove duplication
□ Simplify complex logic
□ Run tests after each refactor
```

**Actions:**
1. IDENTIFY refactoring opportunities
2. MAKE one refactoring at a time
3. RUN tests after each change
4. COMMIT when tests still pass
5. ROLLBACK if tests fail

## Example Usage

### Bug Fix with TDD
```markdown
User: "Fix bug: users can submit empty forms"

Claude: "I'll use TDD to fix this bug.

**Phase 1: Write Test**
Creating test that reproduces the bug..."

[Creates test file]
```javascript
test('rejects form submission with empty required fields', () => {
  const emptyForm = { name: '', email: '' };
  expect(() => submitForm(emptyForm)).toThrow('Required fields missing');
});

test('accepts form with all required fields', () => {
  const validForm = { name: 'Test', email: 'test@example.com' };
  expect(submitForm(validForm)).toBe(true);
});
```

"**Phase 2: Verify Failure**
Running tests..."
[Tests fail as expected]

"**Phase 3: Commit Tests**
Committing test contract..."

"**Phase 4: Implement**
Adding validation..."
[Implements validation, runs tests until green]

"**Phase 5: Verify No Overfitting**
Checking implementation handles edge cases..."
[Reviews code, adds edge case tests]

"**Phase 6: Refactor**
Code is clean. Committing implementation."
```

## Anti-Patterns to Avoid

```markdown
DON'T:
❌ Write tests after implementation (defeats purpose)
❌ Mock everything (hides real bugs)
❌ Write tests that test implementation details
❌ Skip the "verify failure" step
❌ Refactor while tests are red
❌ Add features without tests first

DO:
✅ Write tests that describe behavior
✅ Use real dependencies when feasible
✅ Commit tests before implementation
✅ Keep tests fast and focused
✅ Refactor only when green
✅ Treat tests as documentation
```

## Mock Usage Guidelines

```markdown
WHEN TO USE MOCKS:
✅ External APIs (network calls)
✅ Time-dependent operations
✅ Random number generation
✅ File system operations (sometimes)
✅ Database (for unit tests only)

WHEN TO AVOID MOCKS:
❌ Internal module dependencies
❌ Simple pure functions
❌ Data transformation logic
❌ Business rules
❌ When integration test is more valuable
```

## Integration with Task System

When using TDD within the task management system:

1. **Task Start:** Mark task "In Progress" before writing tests
2. **Checkpoint:** Create checkpoint after test commit
3. **Progress:** Update task progress after each phase
4. **Completion:** Only mark complete when all phases done

## Output Location
- Tests: Project-specific test directory (e.g., `tests/`, `__tests__/`, `spec/`)
- Implementation: Source directories
- Coverage: `.coverage/` or project-specific location
