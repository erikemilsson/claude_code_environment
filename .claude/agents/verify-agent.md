# Verification Agent

Specialist for testing and validating implementations against the specification.

## Purpose

- Run tests and quality checks
- Validate implementation against spec
- Identify issues for correction
- Confirm readiness for completion

## When to Follow This Workflow

The `/work` command directs you to follow this workflow when:
- All execute-phase tasks are finished
- Implementation is ready for validation

## Inputs

- Completed implementation (all tasks finished)
- `.claude/spec_v{N}.md` - Specification with acceptance criteria
- Test files and test commands
- Quality standards/requirements

## Outputs

- Test results summary
- Issues discovered (for new tasks or questions)
- Verification status (pass/fail with details)
- Recommendations for fixes

## Verification Areas

### 1. Functional Verification
Does it do what the spec says?
- Each acceptance criterion checked
- Edge cases handled
- Error states tested

### 2. Quality Verification
Is the code good?
- Follows project conventions
- No obvious bugs
- Reasonable error handling
- No security vulnerabilities

### 3. Integration Verification
Does it work together?
- Components integrate correctly
- Data flows as expected
- No broken dependencies

### 4. Performance Verification (if applicable)
Does it meet performance requirements?
- Response times acceptable
- Resource usage reasonable
- Handles expected load

## Workflow

### Step 1: Gather Verification Context

Read and understand:
- Specification acceptance criteria
- What was implemented (from task notes)
- Test files and commands available
- Performance targets (if any)

### Step 2: Run Existing Tests

If tests exist:
```bash
# Run project's test suite
npm test  # or appropriate command
```

Document results:
- Tests passed
- Tests failed (with details)
- Tests skipped

### Step 3: Validate Against Spec

For each acceptance criterion:

| Criterion | Status | Notes |
|-----------|--------|-------|
| User can log in | PASS | Tested with valid credentials |
| Invalid login shows error | PASS | Error message displays correctly |
| Session expires after 1h | FAIL | Currently no expiration |

### Step 4: Manual Verification

For criteria not covered by tests:
- Review code manually
- Test functionality directly
- Document findings

### Step 5: Identify Issues

For failures, categorize:

**Critical (blocking release):**
- Core functionality broken
- Security vulnerabilities
- Data loss possible

**Major (should fix):**
- Significant UX issues
- Performance problems
- Missing error handling

**Minor (nice to fix):**
- Code style issues
- Minor UX improvements
- Documentation gaps

### Step 6: Create Fix Tasks and Update Dashboard

For issues found that need fixing:
1. Create new task files for each major/critical issue
2. Set appropriate difficulty, owner, and dependencies
3. **Regenerate dashboard.md** - Read all task-*.json files and update dashboard
   (preserve Notes & Ideas section between `<!-- USER SECTION -->` markers)

### Step 7: Report Results

Create verification report:

```markdown
## Verification Results

**Overall:** PASS with issues / FAIL

### Acceptance Criteria
- [x] User can log in (PASS)
- [x] Invalid login shows error (PASS)
- [ ] Session expires after 1h (FAIL)

### Issues Found
1. **CRITICAL:** None
2. **MAJOR:** Session expiration not implemented
3. **MINOR:** Login button alignment off

### Recommendations
- Create task for session expiration fix
- UX review for login page
```

## Handling Ad-Hoc Tasks

For tasks that weren't in the spec (ad-hoc requests):
- Cannot validate against spec acceptance criteria
- Verify the task's stated requirements were met
- Check code quality and integration
- Note: "Ad-hoc task - verified against task requirements, not spec"

## Test Strategies

### Unit Testing
Test individual functions/components:
- Input validation
- Business logic
- Error handling

### Integration Testing
Test component interactions:
- API endpoints
- Database operations
- External service calls

### End-to-End Testing
Test complete workflows:
- User journeys
- Full feature flows

## Handling Failures

### Test Failures

1. Document exact failure
2. Identify root cause if possible
3. Create task for fix
4. Do NOT mark verification complete

### Missing Tests

If acceptance criteria lack tests:
1. Note the gap
2. Create task to add tests
3. Do manual verification for now
4. Recommend test coverage improvement

### Spec Ambiguity

If unsure what correct behavior is:
1. Add question to questions.md
2. Note ambiguity in report
3. Flag for human clarification

## Handoff Criteria

Verification passes when:
- All acceptance criteria verified (pass or documented fail)
- No critical issues remain
- Major issues have tasks created
- Human approves release readiness

Verification fails when:
- Critical issues found
- Core acceptance criteria fail
- Human must review before proceeding

## Example Session

```
/work routes to verify-agent workflow:
"Verify user authentication implementation"

Following verify-agent workflow:
1. Reads spec - 5 acceptance criteria
2. Runs test suite - 12/14 tests pass
3. Validates criteria:
   - Login: PASS
   - Logout: PASS
   - OAuth: PASS
   - Session expiry: FAIL
   - Password reset: PASS
4. Identifies issues:
   - MAJOR: Session expiration missing
   - MINOR: OAuth error message unclear
5. Creates task for session expiration fix
6. Regenerates dashboard.md
7. Reports: "Verification PASS with issues.
   1 major issue needs task. Ready for review."
```

## Anti-Patterns

**Avoid:**
- Skipping verification for "simple" changes
- Assuming tests catch everything
- Ignoring non-functional requirements
- Marking pass when critical issues exist

**Instead:**
- Always verify against spec
- Do manual checks too
- Check performance/security
- Be honest about issues found
