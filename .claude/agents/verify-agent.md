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

## How This Workflow Is Invoked

This file is read by `/work` during the Verify phase. **You are reading this file because `/work` directed you here.** Follow every step below in order — do not skip steps, write verification-result.json without performing actual verification, or declare pass without checking acceptance criteria.

Each step produces a required output. The verification-result.json file (Step 7) must contain real per-criterion data from Step 3, not fabricated results.

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

**Required artifact:** A per-criterion pass/fail table. Every acceptance criterion from the spec must appear in this table with an explicit PASS or FAIL status and a note explaining how it was verified. This table feeds into verification-result.json (Step 7) — the `criteria_passed` and `criteria_failed` counts must match this table.

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
3. **Mark recommendation tasks as out-of-spec** — tasks created by verify-agent that go beyond the spec's acceptance criteria must include `"out_of_spec": true` and `"source": "verify-agent"` in the task JSON:
   ```json
   {
     "out_of_spec": true,
     "source": "verify-agent",
     "status": "Pending"
   }
   ```
   These tasks require explicit user approval before `/work` will execute them. See the out-of-spec consent flow in `work.md`.
4. **Regenerate dashboard.md** - Read all task-*.json files and update dashboard
   - Preserve Notes & Ideas section between `<!-- USER SECTION -->` markers
   - Update overall completion percentage, Critical Path, and Recently Completed
   - Show out-of-spec tasks with ⚠️ prefix in the task list

### Step 7: Persist Verification Result

Write the verification outcome to `.claude/verification-result.json` so other commands (`/status`, `/work`) can distinguish "ready for verification" from "verified/complete":

```json
{
  "result": "pass",
  "timestamp": "2026-01-27T14:30:00Z",
  "spec_version": "spec_v1",
  "spec_fingerprint": "sha256:abc123...",
  "summary": "All acceptance criteria passed. 1 minor issue noted.",
  "criteria_passed": 5,
  "criteria_failed": 0,
  "issues": {
    "critical": 0,
    "major": 0,
    "minor": 1
  },
  "tasks_created": []
}
```

**Field definitions:**

| Field | Values | Description |
|-------|--------|-------------|
| `result` | `"pass"`, `"fail"`, `"pass_with_issues"` | Overall verification outcome |
| `timestamp` | ISO 8601 | When verification completed |
| `spec_version` | e.g., `"spec_v1"` | Which spec version was verified against |
| `spec_fingerprint` | SHA-256 hash | Fingerprint of spec at verification time |
| `summary` | Free text | Human-readable summary of findings |
| `criteria_passed` | Number | Count of acceptance criteria that passed |
| `criteria_failed` | Number | Count of acceptance criteria that failed |
| `issues` | Object | Count of issues by severity |
| `tasks_created` | Array of task IDs | Tasks created for issues found |

**Rules:**
- **Overwrite on each verification run** — only the latest result matters
- **Result is invalidated** when spec fingerprint changes (spec was modified after verification)
- **Result is invalidated** when new tasks are created or existing tasks change status
- `/work` and `/status` check this file to determine phase (see below)

### Step 8: Report Results

Display the verification report to the user:

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
- Verification result written to `.claude/verification-result.json` (Step 7)
- Human approves release readiness

Verification fails when:
- Critical issues found
- Core acceptance criteria fail
- Human must review before proceeding
- Verification result written with `"result": "fail"` (Step 7)

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
7. Writes verification-result.json with result: "pass_with_issues"
8. Reports: "Verification PASS with issues.
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
