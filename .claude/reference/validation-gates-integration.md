# Validation Gates Integration Guide

*Created: 2025-12-17*

## Overview

Validation gates are MANDATORY checkpoints that ensure quality, safety, and correctness at critical decision points. This guide explains how validation gates integrate with the task workflow to prevent errors and ensure consistent execution.

## Core Principle

**Every critical decision must pass through explicit validation before proceeding**

Validation gates enforce:
1. **Pre-conditions** are met before starting work
2. **Invariants** hold during execution
3. **Post-conditions** verify completion
4. **Quality standards** meet acceptance criteria

## Gate Types

### 1. Pre-Execution Gates (GO/NO-GO)
Run BEFORE starting any task work to verify task is ready

### 2. Mid-Execution Gates (CONTINUE/ADJUST/ABORT)
Run DURING task execution at progress checkpoints

### 3. Post-Execution Gates (ACCEPT/REJECT)
Run AFTER task completion to verify quality and completeness

## Implementation

### Script Location
**Primary Tool**: `scripts/validation-gates.py`

### Available Gates
Defined in `.claude/reference/validation-gates.md`

## Integration with Complete-Task Workflow

### Starting a Task (Pre-Execution Gates)

When `complete-task.md` starts a task, it MUST run pre-execution gates:

```python
# 1. Load task
task = load_task(task_id)

# 2. Run validation gates
gates = ValidationGates()
can_proceed, results = gates.run_pre_execution_gates(task_id)

# 3. Check results
if not can_proceed:
    print("VALIDATION FAILED - Cannot start task")
    for result in results:
        if not result.passed and result.level == GateLevel.BLOCKING:
            print(f"❌ {result.check_name}: {result.message}")
    return  # STOP - do not proceed

# 4. Show warnings
for result in results:
    if not result.passed and result.level == GateLevel.WARNING:
        print(f"⚠️  {result.check_name}: {result.message}")

# 5. Proceed with task execution
update_task_status(task_id, "In Progress")
```

### Pre-Execution Gate Checks

1. **Task Status Valid**
   - Status is "Pending" or "In Progress"
   - NOT "Broken Down" (work on subtasks instead)
   - NOT "Finished" (already complete)
   - NOT "Blocked" (resolve blocker first)

2. **Dependencies Complete**
   - All tasks in `dependencies` array have status "Finished"
   - No circular dependencies
   - Dependency chain is valid

3. **Difficulty Breakdown Requirement**
   - If difficulty ≥ 7 AND status = "Pending":
     - BLOCKING: Must break down task first
     - Message: "Task difficulty 7+ must be broken down before execution"

4. **Parent Task Not Broken Down**
   - If parent task exists:
     - Parent status must NOT be "In Progress" or "Finished"
     - Parent should be "Broken Down"

5. **Required Files Accessible**
   - Files in `files_affected` are accessible (if they must exist)
   - Parent directories exist

6. **Confidence Threshold**
   - Confidence >= 50%
   - Warning if confidence < 70%

### During Execution (Mid-Execution Gates)

Gates run at checkpoints during task execution:

```python
# After every 3 steps or significant action
if current_step % 3 == 0:
    # Run mid-execution gates
    can_continue, results = gates.run_mid_execution_gates(task_id, current_state)

    if not can_continue:
        # Create checkpoint before stopping
        create_checkpoint(f"Stopped at step {current_step} - validation failed")

        # Report issues
        print("VALIDATION FAILED - Stopping execution")
        for result in results:
            if not result.passed:
                print(f"{result.level}: {result.message}")

        # Mark task as blocked
        update_task_status(task_id, "Blocked")
        add_blocker_note(task_id, "Mid-execution validation failed: " + str(results))
        return
```

### Mid-Execution Gate Checks

1. **Progress Checkpoint Gate** (Every 3 steps)
   - Current approach still valid
   - No unexpected blockers
   - Confidence hasn't dropped > 30%
   - Time estimate still reasonable
   - Context usage < 70%

2. **Assumption Validation Gate** (Before critical operations)
   - Each assumption explicitly tested
   - > 70% assumptions validated
   - No critical assumptions invalidated

3. **Resource Threshold Gate** (Context limits)
   - Context usage < 80%
   - Token budget sufficient
   - Memory available

### Completing a Task (Post-Execution Gates)

Before marking task as "Finished", run post-execution gates:

```python
# 1. Run post-execution gates
can_complete, results = gates.run_post_execution_gates(task_id)

# 2. Check results
if not can_complete:
    print("COMPLETION VALIDATION FAILED")
    for result in results:
        if not result.passed and result.level == GateLevel.BLOCKING:
            print(f"❌ {result.check_name}: {result.message}")

    # Keep task as "In Progress"
    add_completion_note(task_id, "Attempted completion but failed validation: " + str(results))
    return  # Do NOT mark as Finished

# 3. Show warnings
for result in results:
    if not result.passed and result.level == GateLevel.WARNING:
        print(f"⚠️  {result.check_name}: {result.message}")

# 4. Mark task as finished
update_task_status(task_id, "Finished")
add_completion_date(task_id)
add_completion_notes(task_id, completion_summary)
```

### Post-Execution Gate Checks

1. **Completion Notes Provided**
   - `completion_notes` field is not null/empty
   - Notes describe what was actually done

2. **Assumptions Validated**
   - All assumptions have status (validated/invalidated/pending)
   - Critical assumptions are not left pending
   - Validation methods documented

3. **Files Modified Verified**
   - Files in `files_affected` actually exist (if expected)
   - Changes are intentional

4. **Subtask Completion** (if parent task)
   - All subtasks have status "Finished"
   - Parent can auto-complete

5. **Quality Standards Met**
   - Documentation complete
   - Tests passing (if applicable)
   - No known bugs

## Integration with Breakdown Command

Before breaking down a task:

```python
# Run breakdown decision gate
gates = ValidationGates()
should_breakdown, results = gates.run_breakdown_decision_gate(task_id)

if not should_breakdown:
    print("Breakdown not recommended:")
    for result in results:
        print(f"- {result.message}")
    return

# Proceed with breakdown
create_checkpoint("Before breakdown of task " + task_id)
perform_breakdown(task_id)
```

### Breakdown Decision Gate Checks

1. **Difficulty Requirement**
   - Difficulty >= 7 OR explicit user request

2. **Decomposability**
   - Task can be broken into logical parts
   - Each subtask can be <= difficulty 6

3. **Dependency Chain Possible**
   - Clear dependencies between subtasks
   - No circular dependencies

## Integration with Environment Creation

Bootstrap/smart-bootstrap commands use environment creation gate:

```python
# Before generating environment
gates = ValidationGates()
can_create, results = gates.run_environment_creation_gate(spec_data, template_confidence)

if not can_create:
    print("Cannot create environment:")
    for result in results:
        if not result.passed:
            print(f"- {result.message}")
    return

# Proceed with environment generation
create_environment(spec_data, template)
```

### Environment Creation Gate Checks

1. **Specification Valid**
   - Specification successfully read
   - Required sections present

2. **Template Confidence**
   - Template confidence >= 85%
   - Clear template selection

3. **No Critical Unknowns**
   - All required information available
   - Configuration validated

4. **Target Directory Writable**
   - Destination directory accessible
   - Permissions sufficient

## Gate Configuration

### Gate Thresholds

Defined in `agent-config.json` → `validation_gates`:

```json
{
  "validation_gates": {
    "pre_execution": {
      "confidence_threshold": 50,
      "confidence_warning": 70
    },
    "mid_execution": {
      "progress_check_interval": 3,
      "confidence_drop_max": 30,
      "context_usage_max": 70
    },
    "post_execution": {
      "assumption_validation_min": 70,
      "require_completion_notes": true
    }
  }
}
```

### Customizing Gates

To modify gate behavior:

1. **Adjust thresholds**: Edit `agent-config.json`
2. **Add new checks**: Extend `validation-gates.py`
3. **Disable specific gates**: Set `enabled: false` in config

## Logging and Monitoring

### Gate Execution Log

All gate runs are logged to `.claude/validation-gates.log`:

```
2025-12-17T14:30:22 | PRE_EXEC | task-42 | PASS | All checks passed
2025-12-17T14:35:18 | MID_EXEC | task-42 | WARN | Confidence dropped 25%
2025-12-17T14:45:30 | POST_EXEC | task-42 | FAIL | Completion notes missing
```

### Viewing Gate History

```bash
# View recent gate results
tail -50 .claude/validation-gates.log

# Filter by gate type
grep "PRE_EXEC" .claude/validation-gates.log

# Find failures
grep "FAIL" .claude/validation-gates.log
```

### Gate Metrics

Track gate effectiveness:

```python
# From validation-gates.py
gates = ValidationGates()
metrics = gates.get_metrics()

print(f"Total gates run: {metrics['total']}")
print(f"Pass rate: {metrics['pass_rate']}%")
print(f"Blocking failures: {metrics['blocking_failures']}")
```

## Error Handling

### Gate Script Failures

If validation-gates.py fails:

```python
try:
    can_proceed, results = gates.run_pre_execution_gates(task_id)
except Exception as e:
    print(f"VALIDATION GATE ERROR: {e}")
    print("Proceeding WITHOUT validation (document in notes)")
    # Continue but add note about validation failure
    add_note(task_id, f"Validation gates failed to run: {e}")
```

### Handling Gate Failures

**Pre-Execution Gate Failure**:
1. DO NOT proceed with task
2. Fix issues identified by gates
3. Re-run gates before starting

**Mid-Execution Gate Failure**:
1. Create checkpoint immediately
2. Assess severity
3. If BLOCKING: Stop work, mark as Blocked
4. If WARNING: Adjust approach, continue with caution

**Post-Execution Gate Failure**:
1. DO NOT mark task as Finished
2. Address validation failures
3. Re-run completion when fixed

## Command-Line Interface

### Running Gates Manually

```bash
# Pre-execution gates
python3 scripts/validation-gates.py pre-exec task-42

# Mid-execution gates
python3 scripts/validation-gates.py mid-exec task-42 --current-step 6

# Post-execution gates
python3 scripts/validation-gates.py post-exec task-42

# Breakdown decision gate
python3 scripts/validation-gates.py breakdown task-42

# Environment creation gate
python3 scripts/validation-gates.py env-create --spec requirements.md --confidence 90
```

### Output Format

```
VALIDATION GATES: PRE-EXECUTION
Task: task-42 "Implement authentication system"

Running checks...

✓ Task status valid (Pending)
✓ Dependencies complete (1/1)
❌ Difficulty breakdown required
   → Task difficulty 8 must be broken down before execution
   → Use: /breakdown task-42
⚠️  Confidence below recommended threshold
   → Current: 65%, Recommended: 70%+
   → Consider gathering more information

RESULT: BLOCKED
Cannot proceed with execution until blocking issues resolved.
```

## Best Practices

### Always Run Gates

**DO**:
- Run pre-execution gates before every task start
- Run mid-execution gates at checkpoints
- Run post-execution gates before marking finished
- Log all gate results

**DON'T**:
- Skip gates "just this once"
- Ignore gate warnings without documenting why
- Proceed when BLOCKING gates fail
- Modify gates to "make them pass"

### Treat Gates as Hard Stops

BLOCKING gates must be fixed:
- Task difficulty 7+ not broken down → Break it down
- Dependencies incomplete → Wait for dependencies
- Critical assumptions invalidated → Revise approach
- Completion notes missing → Write notes

### Document Gate Overrides

If you must proceed despite gate warnings:

```json
{
  "completion_notes": "...",
  "gate_overrides": [
    {
      "gate": "confidence_threshold",
      "reason": "Proceeding with 65% confidence due to time constraints. Documented risks in assumptions.",
      "approved_by": "user",
      "date": "2025-12-17"
    }
  ]
}
```

## Performance Impact

### Gate Execution Time

| Gate Type | Typical Time | Notes |
|-----------|-------------|-------|
| Pre-execution | 10-30ms | Quick validation checks |
| Mid-execution | 20-50ms | Includes state analysis |
| Post-execution | 30-100ms | Most comprehensive |
| Breakdown decision | 15-40ms | Complexity analysis |

### Optimization

Gates are designed for minimal overhead:
- Fast file reads (no parsing unless needed)
- Cached dependency graphs
- Lazy evaluation of expensive checks
- Early exit on BLOCKING failures

## Troubleshooting

### Gate always failing?

Check the specific failure message:
```bash
python3 scripts/validation-gates.py pre-exec task-ID --verbose
```

### Gate configuration not working?

Verify `agent-config.json` syntax:
```bash
python3 -m json.tool .claude/agent-config.json
```

### Gates not running in commands?

Check command file integration:
```bash
grep "validation.*gate" .claude/commands/complete-task.md
```

## Related Documentation

- **Validation Gates Reference**: `.claude/reference/validation-gates.md` (gate definitions and criteria)
- **Validation Gates Script**: `scripts/validation-gates.py` (implementation)
- **Complete Task Command**: `.claude/commands/complete-task.md` (integration points)
- **Agent Config**: `.claude/agent-config.json` (gate configuration)
- **Error Recovery**: `.claude/reference/error-recovery.md` (handling gate failures)

## Summary

Validation gates provide:
- **Quality assurance** at critical decision points
- **Error prevention** through pre-validation
- **Consistency** across all task operations
- **Transparency** via logging and metrics

**Integration points**:
- `complete-task.md`: Pre/mid/post gates during task execution
- `breakdown.md`: Breakdown decision gate
- `smart-bootstrap.md`: Environment creation gate
- Manual: Run gates anytime via CLI

**Key principle**: Gates are not optional - they are mandatory quality checkpoints that prevent errors before they occur.
