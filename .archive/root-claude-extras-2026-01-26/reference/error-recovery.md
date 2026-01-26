# Error Recovery Patterns for Claude 4

## Core Philosophy

**Fail gracefully, recover automatically, escalate transparently**

1. **Anticipate failures** - Common errors should have pre-planned responses
2. **Automatic recovery** - Try to fix issues without user intervention
3. **Clear escalation** - When automation fails, provide actionable guidance
4. **Learn from failures** - Document patterns for future prevention

## Common Failure Scenarios & Recovery Strategies

### 1. File Operation Errors

#### File Not Found
```
ERROR: File not found at path/to/file.txt

RECOVERY SEQUENCE:
1. Check for typos in path (case sensitivity)
2. Search for similar filenames using Glob
3. Check if file was moved/renamed recently
4. Offer to create file if appropriate
5. Ask user for correct path

CONFIDENCE THRESHOLDS:
- >90% match found → Auto-correct and proceed
- 70-90% match → Confirm with user
- <70% match → Full clarification needed
```

**Implementation Pattern**:
```python
# Attempt 1: Direct read
try:
    content = Read("path/to/file.txt")
except FileNotFoundError:
    # Attempt 2: Search for similar
    similar = Glob("**/file.txt")
    if similar and confidence(similar[0]) > 0.9:
        content = Read(similar[0])
        log("Auto-corrected path to: " + similar[0])
    else:
        # Attempt 3: User clarification
        ask_user("File not found. Possible matches: ...")
```

#### Permission Denied
```
ERROR: Permission denied for file operation

RECOVERY:
1. Check if file is locked by another process
2. Verify correct permissions needed
3. Try alternative approach (copy instead of move)
4. Escalate to user with specific fix instructions
```

#### File Already Exists
```
ERROR: File already exists at target path

RECOVERY:
1. Read existing file to check if identical
2. If different, create backup with timestamp
3. Offer merge options if appropriate
4. Create numbered alternative (file_2.txt)
```

### 2. Bash Command Failures

#### Command Not Found
```
ERROR: Command 'xyz' not found

RECOVERY:
1. Check for common alternatives (python → python3)
2. Verify if package needs installation
3. Check PATH environment
4. Provide installation instructions
```

**Recovery Matrix**:
| Command | Alternative | Install Command |
|---------|------------|-----------------|
| python | python3, py | apt-get install python3 |
| node | nodejs | npm install -g node |
| code | code-insiders, codium | Download from website |

#### Command Timeout
```
ERROR: Command exceeded timeout limit

RECOVERY:
1. Check if partial output available
2. Retry with increased timeout
3. Break into smaller operations
4. Run in background if appropriate
```

**Timeout Strategy**:
```javascript
const timeoutLevels = [
    { duration: 30000, action: "standard" },
    { duration: 120000, action: "retry_extended" },
    { duration: 300000, action: "background_execution" },
    { duration: 600000, action: "user_intervention" }
];
```

#### Non-Zero Exit Code
```
ERROR: Command failed with exit code 1

RECOVERY:
1. Parse error output for specific issue
2. Apply known fixes for common errors
3. Retry with modified parameters
4. Provide detailed error context to user
```

### 3. Template Detection Ambiguity

#### Multiple Templates Match
```
AMBIGUITY: Both 'research' and 'data-engineering' templates match

RECOVERY:
1. Calculate confidence scores for each
2. Look for disambiguation signals
3. If still ambiguous (diff <20%), ask user
4. Document decision for pattern learning
```

**Disambiguation Framework**:
```
IF confidence_diff < 20%:
    ask_one_question(most_discriminating_factor)
ELIF confidence_diff < 40%:
    proceed_with_highest_but_note_alternative
ELSE:
    auto_select_highest_confidence
```

#### No Template Matches
```
AMBIGUITY: No clear template detected

RECOVERY:
1. Use base template as fallback
2. Extract any domain hints from spec
3. Offer template selection menu
4. Create custom hybrid if needed
```

### 4. Assumption Validation Failures

#### Critical Assumption Invalid
```
ERROR: Assumed Python 3.9+ but found Python 3.7

RECOVERY:
1. Check if upgrade possible
2. Adapt code for older version
3. Find alternative approach
4. Document compatibility requirements
```

**Assumption Recovery Table**:
| Assumption | Validation | Recovery | Fallback |
|------------|------------|----------|----------|
| Python 3.9+ | version check | Request upgrade | Use 3.7 compatible code |
| Git installed | which git | Provide install guide | Use file-based tracking |
| Internet access | ping test | Work offline | Cache required resources |
| Write permissions | test write | Request permissions | Use temp directory |

#### Confidence Degradation
```
WARNING: Confidence dropped below threshold during execution

RECOVERY:
1. Checkpoint current state
2. Re-validate assumptions
3. Adjust approach if needed
4. Create recovery point for rollback
```

### 5. Context Loss Recovery

#### Mid-Task Context Reset
```
ERROR: Context lost during long-running task

RECOVERY:
1. Check for checkpoint files
2. Read task status JSON
3. Scan recent file modifications
4. Reconstruct state from artifacts
5. Resume from last known good state
```

**Checkpoint Pattern**:
```json
{
  "checkpoint_id": "task_78_step_3",
  "timestamp": "2025-12-16T10:30:00Z",
  "completed_steps": ["read_spec", "analyze", "template_selected"],
  "next_step": "generate_files",
  "state": {
    "template": "power-query",
    "confidence": 0.92,
    "files_created": []
  }
}
```

#### State Validation Failure
```
ERROR: Current state doesn't match expected

RECOVERY:
1. Compare actual vs expected state
2. Identify divergence point
3. Determine if safe to continue
4. Rollback if necessary
5. Document state mismatch
```

### 6. Data Validation Errors

#### Schema Mismatch
```
ERROR: Data doesn't match expected schema

RECOVERY:
1. Attempt automatic type conversion
2. Handle missing fields with defaults
3. Validate partial data if possible
4. Request user input for critical fields
```

#### Corrupted Data
```
ERROR: Data file appears corrupted

RECOVERY:
1. Check for backup versions
2. Attempt partial recovery
3. Validate what can be salvaged
4. Reconstruct from other sources
5. Start fresh with user confirmation
```

## Retry Strategies

### Exponential Backoff
```javascript
async function retryWithBackoff(operation, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await operation();
        } catch (error) {
            if (attempt === maxRetries) throw error;

            const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
            log(`Attempt ${attempt} failed, retrying in ${delay}ms`);
            await sleep(delay);
        }
    }
}
```

### Circuit Breaker Pattern
```javascript
class CircuitBreaker {
    constructor(threshold = 5, timeout = 60000) {
        this.failures = 0;
        this.threshold = threshold;
        this.timeout = timeout;
        this.state = 'closed';
        this.nextAttempt = Date.now();
    }

    async execute(operation) {
        if (this.state === 'open') {
            if (Date.now() < this.nextAttempt) {
                throw new Error('Circuit breaker is open');
            }
            this.state = 'half-open';
        }

        try {
            const result = await operation();
            this.onSuccess();
            return result;
        } catch (error) {
            this.onFailure();
            throw error;
        }
    }

    onSuccess() {
        this.failures = 0;
        this.state = 'closed';
    }

    onFailure() {
        this.failures++;
        if (this.failures >= this.threshold) {
            this.state = 'open';
            this.nextAttempt = Date.now() + this.timeout;
        }
    }
}
```

## Error Escalation Framework

### Level 1: Silent Recovery
- Auto-correct obvious issues
- Apply known fixes
- Log for analysis
- Continue execution

### Level 2: Notification & Continue
- Inform user of issue and fix
- Show what was corrected
- Continue with task
- Note in completion summary

### Level 3: User Confirmation
- Stop before critical operation
- Explain issue and proposed fix
- Get explicit approval
- Provide alternatives

### Level 4: Full Stop
- Critical failure detected
- Cannot proceed safely
- Provide detailed diagnostics
- Offer manual recovery steps

## Recovery Confidence Thresholds

| Confidence | Action | Example |
|------------|--------|---------|
| >95% | Auto-fix silently | Fix typo in filepath |
| 85-95% | Auto-fix with notification | Change python to python3 |
| 70-85% | Confirm before proceeding | Select similar filename |
| 50-70% | Provide options | Choose between templates |
| <50% | Full user guidance | Unknown error, need help |

## Error Pattern Documentation

### Template for New Patterns
```markdown
### [Error Type]

**Symptoms**:
- What user sees
- Error messages
- Failed operations

**Root Causes**:
- Common trigger 1
- Common trigger 2

**Recovery Strategy**:
1. First attempt
2. Second attempt
3. Escalation

**Prevention**:
- Proactive check
- Validation step
- User guidance

**Success Rate**: X% auto-recovery
**Added**: [Date]
**Last Updated**: [Date]
```

## Proactive Error Prevention

### Pre-Execution Validation
```python
def validate_before_execution():
    checks = [
        ("Python installed", check_python),
        ("Git available", check_git),
        ("Write permissions", check_permissions),
        ("Required packages", check_dependencies),
        ("Sufficient disk space", check_disk_space)
    ]

    failures = []
    for name, check in checks:
        if not check():
            failures.append(name)

    if failures:
        handle_validation_failures(failures)
    return len(failures) == 0
```

### Health Checks
- Pre-task environment validation
- Mid-task state verification
- Post-task result validation
- Continuous assumption checking

## Learning from Failures

### Error Metrics to Track
1. **Frequency**: How often does this error occur?
2. **Recovery Rate**: What percentage auto-recover?
3. **Time to Resolution**: How long to fix?
4. **User Impact**: Does it block progress?
5. **Pattern Evolution**: Is it increasing/decreasing?

### Continuous Improvement Process
1. Log all errors with context
2. Analyze patterns weekly
3. Update recovery strategies
4. Add new patterns to documentation
5. Improve preemptive checks
6. Share learnings across projects

## Quick Reference Card

| Error | First Try | Second Try | Escalate |
|-------|-----------|------------|----------|
| File not found | Search similar | Check recent moves | Ask user |
| Permission denied | Check locks | Try alternatives | Request access |
| Command not found | Check aliases | Provide install | Manual guide |
| Timeout | Increase limit | Background run | Break apart |
| Template ambiguous | Score confidence | Single question | User choice |
| Data corrupt | Check backups | Partial recovery | Start fresh |
| Context lost | Load checkpoint | Reconstruct state | Restart task |

## Implementation Priority

1. **High Priority** (implement first):
   - File not found recovery
   - Command failures
   - Template detection
   - Context checkpointing

2. **Medium Priority**:
   - Data validation
   - Permission issues
   - Assumption validation
   - State recovery

3. **Low Priority**:
   - Advanced retry patterns
   - Learning systems
   - Metric tracking
   - Pattern evolution