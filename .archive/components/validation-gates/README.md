# Validation Gates Component

## Overview

The Validation Gates component provides systematic pre- and post-execution validation for tasks, catching errors before they propagate and automating quality checks. This is a core part of the Air-Tight Execution Framework (ATEF).

## Purpose

**Catch errors BEFORE they become problems.** Every task execution passes through validation gates that:
- Verify preconditions before starting work
- Check postconditions after completing work
- Automate parent task completion
- Suggest error prevention based on historical patterns

## Component Structure

```
components/validation-gates/
├── README.md                      # This file
├── gates/
│   ├── pre-execution.md           # Checks before starting task
│   ├── post-execution.md          # Checks after completing task
│   └── checkpoint-gate.md         # Verifies checkpoint creation (future)
├── schemas/
│   └── gate-result.schema.json    # Validation result format
└── commands/
    └── run-gate.md                # Execute specific gate
```

## Gate Types

### Pre-Execution Gate
**Purpose:** Verify task is ready for execution

**Checks:**
1. **Status Check** (BLOCKING) - Task must be "Pending" or "In Progress"
2. **Dependency Check** (BLOCKING) - All dependencies must be "Finished"
3. **Difficulty Check** (BLOCKING) - Tasks with difficulty >= 7 must be broken down first
4. **Context Check** (WARNING) - Files in files_affected should exist
5. **Pattern Check** (INFO) - Suggest applicable patterns from pattern library

**Integration:** Called by `complete-task.md` after loading task, before status change

### Post-Execution Gate
**Purpose:** Verify task completed correctly and handle automation

**Checks:**
1. **Files Modified Check** (WARNING) - Verify files_affected were touched
2. **Notes Check** (WARNING) - Ensure documentation was added
3. **Time Tracking Check** (INFO) - Suggest updating actual_hours
4. **Parent Completion Check** (AUTO) - Auto-complete parent if all siblings finished
5. **Error Pattern Check** (INFO) - Warn about common errors for this task type

**Integration:** Called by `complete-task.md` after work done, before marking "Finished"

## Gate Result Format

All gates return a structured result conforming to `schemas/gate-result.schema.json`:

```json
{
  "gate": "pre-execution|post-execution|checkpoint",
  "task_id": "string",
  "passed": boolean,
  "blocking_failures": [
    {
      "check": "string",
      "message": "string",
      "remediation": "string"
    }
  ],
  "warnings": ["string"],
  "info": ["string"],
  "auto_actions": ["string"],
  "timestamp": "YYYY-MM-DD HH:MM:SS"
}
```

### Result Levels
- **Blocking Failures**: Critical issues that HALT task execution
- **Warnings**: Issues that should be reviewed but don't block
- **Info**: Suggestions and informational messages
- **Auto-actions**: Automated actions taken by the gate (e.g., parent completion)

## Integration with Task Management

### Enhanced complete-task.md Workflow

1. Load task details
2. **→ Run Pre-Execution Gate** ← VALIDATION
3. Confirm with user (includes gate warnings)
4. Create checkpoint (if available)
5. Update status to "In Progress"
6. Sync overview
7. Begin work
8. **→ Run Post-Execution Gate** ← VALIDATION
9. Update upon completion (includes gate results)
10. Final sync and feedback

### Task JSON Schema Extension

Tasks can optionally store gate results:

```json
{
  "id": "15",
  "title": "...",
  "validation": {
    "pre_gate_passed": true,
    "post_gate_passed": true,
    "warnings": ["File not found warning"]
  }
}
```

## Usage Examples

### Passing Pre-Execution Gate
```
✓ Pre-execution validation PASSED

ℹ Suggestions:
  - Pattern available: pattern-microsoft-pq-bronze
```

### Failing Pre-Execution Gate
```
✗ Pre-execution validation FAILED

🛑 Blocking Issues:
  [Dependency Check] Cannot start task 25: dependency 23 not finished
  → Remediation: Complete dependency task 23 first

Task execution halted. Resolve blocking issues before proceeding.
```

### Post-Execution with Parent Auto-Completion
```
✓ Post-execution validation PASSED

⚡ Auto-actions:
  - Parent task 12 auto-completed (all subtasks finished)
```

## Parent Task Auto-Completion

The post-execution gate automates parent task completion:

**Process:**
1. Detect task has `parent_task` field
2. Load parent and all sibling tasks
3. Check if ALL siblings are "Finished"
4. If yes:
   - Update parent status to "Finished"
   - Update parent updated_date
   - Add completion note to parent
   - Log auto-action

**Example:**
```
Task 12 (parent, status: "Broken Down")
├── Task 13 (Finished)
├── Task 14 (Finished)
└── Task 15 (In Progress → Finished)  ← Triggers parent completion

Result: Task 12 automatically becomes "Finished"
```

## Dependencies

### Required
- Task management component (`components/task-management/`)
- Task JSON schema with task files

### Optional (for enhanced functionality)
- Pattern library component (for pattern suggestions)
- Error catalog component (for error pattern warnings)
- Checkpoint system component (referenced in workflow)

## Design Principles

1. **Non-blocking by default**: Only critical issues (blocking_failures) halt execution
2. **Informative**: Warnings and info guide without interrupting
3. **Automated**: Auto-actions reduce manual work (e.g., parent completion)
4. **Extensible**: Easy to add new checks to gates
5. **Optional**: Can be disabled if ATEF not needed for simple projects

## Version History

- **v1.0.0** (2025-12-05): Initial release as part of ATEF
  - Pre-execution gate with 5 checks
  - Post-execution gate with 5 checks
  - Automated parent task completion
  - Gate result schema
  - Integration with complete-task.md

## See Also

- `components/task-management/` - Core task system
- `components/pattern-library/` - Reusable execution patterns
- `components/checkpoint-system/` - State snapshots and rollback
- `components/error-catalog/` - Error learning and prevention
