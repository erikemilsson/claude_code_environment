<!-- Type: Direct Execution -->
<!-- Parameterized: Uses $ARGUMENTS for file path -->

# Review File Command

## Purpose
Review a specific file for issues including security vulnerabilities, performance problems, code style violations, and bugs.

## Usage
```
/review-file <file-path>
```

## Arguments
- `$ARGUMENTS` - Path to the file to review (required)

## Process

### 1. Read the Target File
```markdown
READ file at $ARGUMENTS
IF file not found:
  REPORT: "File not found: $ARGUMENTS"
  STOP
```

### 2. Perform Comprehensive Review

**Security Analysis:**
```markdown
CHECK FOR:
□ SQL injection vulnerabilities
□ XSS vulnerabilities
□ Command injection
□ Path traversal
□ Hardcoded credentials
□ Insecure cryptography
□ CSRF vulnerabilities
□ Sensitive data exposure
```

**Performance Analysis:**
```markdown
CHECK FOR:
□ N+1 query patterns
□ Unnecessary loops
□ Memory leaks
□ Blocking operations
□ Missing caching opportunities
□ Inefficient algorithms
□ Large bundle/import issues
```

**Code Quality Analysis:**
```markdown
CHECK FOR:
□ Unused variables/imports
□ Dead code
□ Complex functions (high cyclomatic complexity)
□ Missing error handling
□ Inconsistent naming
□ Magic numbers/strings
□ Code duplication
```

**Bug Detection:**
```markdown
CHECK FOR:
□ Off-by-one errors
□ Null/undefined handling
□ Race conditions
□ Resource cleanup
□ Edge case handling
□ Type mismatches
```

### 3. Generate Report

**Output Format:**
```markdown
# File Review: $ARGUMENTS

## Summary
[Quick overview of file purpose and overall quality]

## Critical Issues (Fix Immediately)
[Security vulnerabilities, bugs that cause failures]

## High Priority Issues
[Performance problems, significant code quality issues]

## Medium Priority Issues
[Code style, minor performance concerns]

## Low Priority Issues
[Suggestions, minor improvements]

## Positive Observations
[Good patterns, well-implemented sections]

## Recommendations
[Actionable next steps]
```

## Example Usage

```markdown
User: /review-file src/auth/login.js

Claude: "# File Review: src/auth/login.js

## Summary
Authentication login handler. 245 lines. Handles user credential
validation and session creation.

## Critical Issues (Fix Immediately)
1. **SQL Injection** (line 45)
   ```javascript
   query(`SELECT * FROM users WHERE email = '${email}'`)
   ```
   Fix: Use parameterized queries

2. **Hardcoded Secret** (line 12)
   ```javascript
   const JWT_SECRET = 'mysecretkey123'
   ```
   Fix: Use environment variable

## High Priority Issues
1. **Missing Rate Limiting** (line 30-50)
   Login endpoint has no rate limiting, vulnerable to brute force.

## Medium Priority Issues
1. **No Input Validation** (line 35)
   Email format not validated before database query.

## Positive Observations
- Good separation of concerns
- Clear function naming
- Proper async/await usage

## Recommendations
1. Fix critical SQL injection immediately
2. Move secrets to environment variables
3. Add rate limiting middleware
4. Implement input validation"
```

## Integration with Workflows

**With TDD:**
```markdown
1. Run /review-file
2. Create tests for identified issues
3. Fix issues with TDD approach
4. Re-run /review-file to verify
```

**With Task System:**
```markdown
1. Run /review-file
2. Create tasks for each issue category
3. Use /complete-task for each fix
4. Run /review-file again to verify
```

## Related Commands

- `/explore-plan-code-commit` - Full workflow for addressing issues
- `/tdd-cycle` - Test-driven approach to fixing issues
- `/complete-task` - Task-based issue resolution
