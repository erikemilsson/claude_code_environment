# Specification Test Schema

This document defines the standard structure for testing project specifications during the planning phase.

## Purpose

Specification testing provides:
- Validation of specification logic and consistency
- Early detection of ambiguities and gaps
- Automated generation of refinement tasks
- User flow verification before implementation

## Schema Structure

```yaml
# Specification Test: [Test Name]

## Test Metadata
- **Test ID**: spec-test-NNN (unique identifier)
- **Created**: YYYY-MM-DD
- **Specification Section**: Section N.N (reference to specification.md)
- **Test Type**: user_flow | logic_validation | consistency_check | completeness_check
- **Status**: pending | running | passed | failed | needs_review
- **Assigned Agent**: specification-architect | null

## Test Definition

### Objective
[Clear statement of what aspect of the specification is being validated]

### Scope
[Which sections of the specification are covered by this test]

### Test Cases

#### Test Case 1: [Scenario Name]
- **Scenario**: [Description of the scenario being tested]
- **Preconditions**:
  - Precondition 1
  - Precondition 2
- **Steps**:
  1. Step 1
  2. Step 2
  3. Step 3
- **Expected Outcome**: [What should happen according to the specification]
- **Actual Outcome**: [Filled after test execution]
- **Pass/Fail**: [pass | fail | unclear]
- **Notes**: [Additional observations]

#### Test Case 2: [Scenario Name]
[... repeat structure ...]

## Validation Logic

### Validation Rules
[Specific rules or criteria used to evaluate the specification]

### Agent Prompt
[Specific instructions for the agent executing this test]

## Test Results

### Execution Date
YYYY-MM-DD HH:MM

### Overall Result
[passed | failed | needs_review]

### Issues Found

#### Issue 1: [Issue Title]
- **Severity**: critical | major | minor
- **Location**: specification.md lines XX-YY or Section N.N
- **Description**: [What is wrong or unclear]
- **Impact**: [How this affects the specification or implementation]
- **Suggested Fix**: [Proposed resolution]
- **Generated Task**: task-XXX

#### Issue 2: [Issue Title]
[... repeat structure ...]

### Passed Validations
- Validation 1: [Description]
- Validation 2: [Description]

## Generated Tasks

### Task Summary
Total tasks generated: N

### Task List
- **task-XXX**: [Brief description] (Priority: [high|medium|low])
- **task-YYY**: [Brief description] (Priority: [high|medium|low])

## Recommendations
[Agent recommendations for improving the specification]

## Next Steps
[What should happen after this test]
```

## Field Definitions

### Test ID
- **Format**: `spec-test-NNN` where NNN is a zero-padded number (001, 002, ...)
- **Uniqueness**: Must be unique across all specification tests
- **Location**: `planning/tests/spec-test-NNN.md`

### Test Type
- **user_flow**: Tests a user journey through the system as described in spec
- **logic_validation**: Tests internal consistency of business logic
- **consistency_check**: Tests for contradictions across specification sections
- **completeness_check**: Tests for missing requirements or gaps

### Status
- **pending**: Test defined but not yet executed
- **running**: Test currently being executed by agent
- **passed**: All test cases passed, no issues found
- **failed**: One or more test cases failed
- **needs_review**: Test completed but results require human interpretation

### Assigned Agent
- **specification-architect**: Default agent for specification tests
- **null**: Manual test (user executes)

### Test Cases
- **Granularity**: Each test case covers one specific scenario
- **Format**: Given-When-Then style (preconditions, steps, expected outcome)
- **Traceability**: Each case maps to specific specification sections

### Issues Found
- **Severity Levels**:
  - `critical`: Specification is unimplementable or contradictory
  - `major`: Significant ambiguity or missing requirements
  - `minor`: Unclear wording or minor inconsistency
- **Each Issue**: Should generate exactly one task for resolution

### Generated Tasks
- **Location**: `planning/.claude/tasks/task-*.json`
- **Format**: Standard task JSON with `related_decisions` and `related_phases`
- **Priority**: Derived from issue severity

## Test Types Explained

### User Flow Tests

**Purpose**: Validate that user journeys make sense and are complete

**Example Test Case:**
```yaml
#### Test Case 1: User Registration Happy Path
- **Scenario**: New user signs up for account
- **Preconditions**:
  - User has valid email address
  - User is not already registered
- **Steps**:
  1. User navigates to registration page
  2. User enters email, password, and name
  3. User clicks "Sign Up" button
  4. System sends verification email
  5. User clicks verification link
  6. System activates account
- **Expected Outcome**: User has active account and can log in
```

**Validation Checks:**
- Are all steps defined in the specification?
- Are error cases covered (invalid email, weak password)?
- Is the flow complete (no dead ends)?

### Logic Validation Tests

**Purpose**: Validate business rules and calculations

**Example Test Case:**
```yaml
#### Test Case 1: Discount Calculation
- **Scenario**: Calculate order total with multiple discount rules
- **Preconditions**:
  - Order contains 3 items ($10, $20, $30)
  - User has 10% loyalty discount
  - Current promotion: 15% off orders >$50
- **Steps**:
  1. Calculate subtotal: $60
  2. Apply loyalty discount: $60 * 0.9 = $54
  3. Check promotion eligibility: $54 > $50 ✓
  4. Apply promotion: $54 * 0.85 = $45.90
- **Expected Outcome**: Final total is $45.90
```

**Validation Checks:**
- Are discount stacking rules clear?
- Is calculation order specified?
- Are edge cases handled (e.g., both discounts reduce below threshold)?

### Consistency Check Tests

**Purpose**: Find contradictions across specification sections

**Example Test Case:**
```yaml
#### Test Case 1: User Role Permissions Consistency
- **Scenario**: Verify user role definitions are consistent across sections
- **Preconditions**: None
- **Steps**:
  1. Extract "Admin" role permissions from Section 3.1
  2. Extract "Admin" role capabilities from Section 5.4
  3. Compare lists
- **Expected Outcome**: All capabilities in 5.4 are covered by permissions in 3.1
```

**Validation Checks:**
- Do different sections contradict each other?
- Are terms used consistently?
- Are cross-references valid?

### Completeness Check Tests

**Purpose**: Find gaps and missing requirements

**Example Test Case:**
```yaml
#### Test Case 1: Error Handling Coverage
- **Scenario**: Verify all API endpoints specify error responses
- **Preconditions**: None
- **Steps**:
  1. List all API endpoints from Section 4
  2. For each endpoint, check if error responses are specified
  3. Identify endpoints missing error specs
- **Expected Outcome**: All endpoints have error response documentation
```

**Validation Checks:**
- Are all requirements covered?
- Are edge cases specified?
- Are error scenarios defined?

## Workflow

### 1. Test Creation (Manual or Automated)

**Manual:**
1. User creates `planning/tests/spec-test-NNN.md`
2. User defines test cases based on specification sections
3. User runs `/test-specification spec-test-NNN`

**Automated (via /test-specification command):**
1. User runs `/test-specification`
2. Agent reads `planning/specification.md`
3. Agent generates test files for each major section
4. User reviews and approves test suite

### 2. Test Execution

1. Agent reads test file
2. Agent reads referenced specification sections
3. Agent executes each test case
4. Agent fills in "Actual Outcome" and "Pass/Fail"
5. Agent identifies issues
6. Agent generates tasks for issues

### 3. Task Generation

For each issue found:
```json
{
  "id": "task-XXX",
  "title": "Fix: [Issue Title]",
  "description": "[Issue Description]\n\nLocation: [Spec Section]\nSeverity: [Severity]\n\nSuggested Fix: [Fix]",
  "status": "pending",
  "difficulty": [1-10 based on severity],
  "priority": "critical | high | medium | low",
  "related_phases": ["phase-N"],
  "related_decisions": ["decision-N"],
  "validation": {
    "criteria": ["Re-run spec-test-NNN and verify it passes"],
    "completed": false
  }
}
```

### 4. Specification Refinement

1. User completes tasks (fixes specification)
2. User re-runs tests
3. Tests pass → specification is validated
4. Tests fail → repeat refinement

### 5. Iteration

- Tests can be re-run multiple times
- Test files updated with latest results
- Test suite evolves as specification evolves

## Standard Test Output Format

```yaml
# Specification Test: User Registration Flow

## Test Metadata
- **Test ID**: spec-test-001
- **Created**: 2025-12-15
- **Specification Section**: Section 3.2 (User Authentication)
- **Test Type**: user_flow
- **Status**: failed
- **Assigned Agent**: specification-architect

## Test Definition

### Objective
Validate that the user registration flow is complete, consistent, and handles all error cases.

### Scope
- Section 3.2.1: Registration form
- Section 3.2.2: Email verification
- Section 3.2.3: Account activation

### Test Cases

#### Test Case 1: Happy Path Registration
- **Scenario**: New user successfully registers and verifies email
- **Preconditions**:
  - User has valid email address (user@example.com)
  - Email is not already registered
- **Steps**:
  1. User navigates to /register
  2. User enters email, password (min 8 chars), and name
  3. User clicks "Sign Up"
  4. System sends verification email to user@example.com
  5. User receives email within 5 minutes
  6. User clicks verification link in email
  7. System activates account and redirects to dashboard
- **Expected Outcome**: User has active account with status="verified"
- **Actual Outcome**: Steps 1-7 are defined in specification
- **Pass/Fail**: pass

#### Test Case 2: Duplicate Email Registration
- **Scenario**: User tries to register with already-used email
- **Preconditions**:
  - Email user@example.com is already registered
- **Steps**:
  1. User navigates to /register
  2. User enters email user@example.com
  3. User clicks "Sign Up"
- **Expected Outcome**: System shows error "Email already registered"
- **Actual Outcome**: Specification does not mention this error case
- **Pass/Fail**: fail
- **Notes**: Section 3.2.1 only covers happy path

#### Test Case 3: Weak Password Rejection
- **Scenario**: User tries to register with weak password
- **Preconditions**: None
- **Steps**:
  1. User enters password "123"
  2. User clicks "Sign Up"
- **Expected Outcome**: System shows error "Password must be at least 8 characters"
- **Actual Outcome**: Specification mentions 8-char minimum but doesn't specify error message
- **Pass/Fail**: needs_review
- **Notes**: Should we specify exact error messages?

## Validation Logic

### Validation Rules
1. All user actions must have corresponding system responses
2. All error cases must be explicitly handled
3. Success criteria must be measurable
4. Flow must not have dead ends

### Agent Prompt
Read Section 3.2 and trace through each test case. For each step, verify that the specification defines:
1. What the user does
2. What the system does in response
3. What happens if the action fails
Flag any steps where the specification is silent or ambiguous.

## Test Results

### Execution Date
2025-12-15 14:30

### Overall Result
failed (1 pass, 1 fail, 1 needs_review)

### Issues Found

#### Issue 1: Missing Duplicate Email Error Handling
- **Severity**: major
- **Location**: specification.md Section 3.2.1
- **Description**: Specification does not define behavior when user attempts to register with an email that's already in the system.
- **Impact**: Implementation team won't know what error to show or how to handle this case. Could lead to poor UX or security issues (email enumeration).
- **Suggested Fix**: Add subsection "3.2.1.2 Duplicate Email Handling" specifying:
  - System checks if email exists before creating account
  - If exists, show error "This email is already registered. Try logging in or reset your password."
  - Do not reveal whether email exists (to prevent enumeration attacks)
- **Generated Task**: task-101

#### Issue 2: Unclear Error Message Specification
- **Severity**: minor
- **Location**: specification.md Section 3.2.1
- **Description**: Password length requirement is mentioned (8 chars) but exact error message wording is not specified.
- **Impact**: Inconsistent error messages across the application. Minor UX inconsistency.
- **Suggested Fix**: Add appendix "Error Message Standards" with all error messages specified exactly, or add note that exact wording is left to implementation team.
- **Generated Task**: task-102

### Passed Validations
- Happy path registration flow is complete and well-defined
- Email verification process is clear
- Account activation steps are specified

## Generated Tasks

### Task Summary
Total tasks generated: 2

### Task List
- **task-101**: Add duplicate email error handling to registration spec (Priority: high)
- **task-102**: Clarify error message specification approach (Priority: medium)

## Recommendations
1. Consider creating a comprehensive error handling appendix
2. Add test cases for password strength validation (uppercase, numbers, symbols?)
3. Specify timeout for verification email (currently says "within 5 minutes" but not in spec)

## Next Steps
1. Complete task-101 and task-102
2. Re-run spec-test-001 to verify fixes
3. Consider creating spec-test-002 for password reset flow (similar structure)
```

## Agent Integration

### Specification Architect Agent

**Capabilities:**
- Read specification sections
- Identify logical inconsistencies
- Trace user flows
- Generate test cases
- Create refinement tasks

**Inputs:**
- `planning/specification.md`
- Test file (`planning/tests/spec-test-NNN.md`)
- Context from `planning/.claude/context/phases.md` and `decisions.md`

**Outputs:**
- Test results (filled into test file)
- Issues found (in test file)
- Generated tasks (in `planning/.claude/tasks/`)

## Examples

### Example: Consistency Check Test

```yaml
# Specification Test: Phase Input/Output Consistency

## Test Metadata
- **Test ID**: spec-test-005
- **Created**: 2025-12-20
- **Specification Section**: Section 2 (Architecture), Section 4 (Data Flow)
- **Test Type**: consistency_check
- **Status**: passed
- **Assigned Agent**: specification-architect

## Test Definition

### Objective
Verify that data outputs from each phase match the inputs expected by the next phase.

### Scope
- Section 2.1: Phase 1 outputs
- Section 2.2: Phase 2 inputs and outputs
- Section 2.3: Phase 3 inputs

### Test Cases

#### Test Case 1: Phase 1 → Phase 2 Data Consistency
- **Scenario**: Phase 1 output matches Phase 2 input requirements
- **Preconditions**: None
- **Steps**:
  1. Extract Phase 1 outputs from Section 2.1: "Normalized data in staging.users table with fields: id, email, name, created_at"
  2. Extract Phase 2 inputs from Section 2.2: "User data from staging schema"
  3. Compare: Does "staging.users table" match "User data from staging schema"?
- **Expected Outcome**: Phase 1 output satisfies Phase 2 input
- **Actual Outcome**: Match confirmed. Phase 2 explicitly references staging.users table in Section 4.2.
- **Pass/Fail**: pass

#### Test Case 2: Phase 2 → Phase 3 Data Consistency
- **Scenario**: Phase 2 output matches Phase 3 input requirements
- **Preconditions**: None
- **Steps**:
  1. Extract Phase 2 outputs from Section 2.2: "Analytics-ready dataset in production.user_metrics table"
  2. Extract Phase 3 inputs from Section 2.3: "User metrics data"
  3. Compare: Does "production.user_metrics table" match "User metrics data"?
- **Expected Outcome**: Phase 2 output satisfies Phase 3 input
- **Actual Outcome**: Match confirmed.
- **Pass/Fail**: pass

## Test Results

### Execution Date
2025-12-20 10:15

### Overall Result
passed

### Issues Found
None

### Passed Validations
- Phase 1 → Phase 2 data flow is consistent
- Phase 2 → Phase 3 data flow is consistent
- All phase inputs have corresponding outputs from previous phases

## Generated Tasks

### Task Summary
Total tasks generated: 0

## Recommendations
None - specification is consistent on phase data flow.

## Next Steps
Proceed with implementation. Consider creating similar tests for API contracts between phases.
```

## Troubleshooting

### Problem: Test cases are too detailed and take forever to create
**Solution**: Focus on high-risk areas. Don't test everything - test critical flows and complex logic.

### Problem: Agent finds too many minor issues
**Solution**: Adjust severity threshold. Only generate tasks for major/critical issues.

### Problem: Specification keeps changing, tests are always failing
**Solution**: This is expected during early planning. Run tests less frequently or mark tests as "needs_review" until spec stabilizes.

### Problem: Unclear if a test case passed or failed
**Solution**: Use "needs_review" status and manually evaluate. Refine the test case for clarity.

### Problem: Test results are ambiguous
**Solution**: Make expected outcomes more specific and measurable. Use concrete values instead of vague descriptions.
