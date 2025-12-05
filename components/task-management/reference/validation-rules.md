# Task Validation Rules

## Required Fields
Every task JSON file must include:
- `id` (string, unique)
- `title` (string, non-empty)
- `description` (string)
- `difficulty` (integer, 1-10)
- `status` (string, from valid statuses)
- `created_date` (string, YYYY-MM-DD format)
- `dependencies` (array of task IDs or empty)
- `subtasks` (array of task IDs or empty)
- `parent_task` (string task ID or null)
- `breakdown_history` (string YYYY-MM-DD format or null)

## Valid Status Values
- **Pending**: Task is defined but not started
- **In Progress**: Task is actively being worked on
- **Blocked**: Task cannot proceed (must have specific blockers listed)
- **Broken Down**: Task has been decomposed into subtasks; completion depends on subtask progress
- **Finished**: Task is complete

## Status-Specific Rules

### "Broken Down" Status
- MUST have at least one subtask in the `subtasks` array
- CANNOT be manually moved to "Finished" (only automatic)
- CANNOT be worked on directly (must work on subtasks)
- Original `difficulty` is preserved for reference
- Automatically transitions to "Finished" when all subtasks are "Finished"
- MUST have `breakdown_history` timestamp set

### Subtask Rules
- If `parent_task` is not null, task is a subtask
- Parent task referenced in `parent_task` must exist
- Parent task must have this subtask in its `subtasks` array
- Subtasks should have difficulty ≤6

## Legal Status Transitions
- Pending → In Progress (when work begins)
- Pending → Blocked (if blockers discovered before starting)
- Pending → **Broken Down** (when using breakdown.md command)
- In Progress → Finished (when work completes successfully)
- In Progress → Blocked (if blockers encountered during work)
- In Progress → **Broken Down** (if complexity discovered mid-work)
- Blocked → In Progress (when blockers are resolved)
- Blocked → Pending (if need to reset blocked task)
- **Broken Down → Finished** (automatic only, when all subtasks done)

## Illegal Transitions
- Finished → any other status (completed tasks don't regress)
- Direct Pending → Finished (must go through In Progress, unless parent is Broken Down)
- **Broken Down → In Progress** (cannot resume work on broken down task)
- **Manual Broken Down → Finished** (only automatic transition allowed)

## Automatic Status Updates
- When using complete-task.md: Status automatically changes Pending → In Progress → Finished
- When completing a subtask: Check if parent should auto-complete
- When using breakdown.md: Parent status automatically changes to "Broken Down"
- When using update-tasks.md: Status inconsistencies are flagged but not auto-corrected
- When using sync-tasks.md: Status is read from JSON and displayed in overview (no changes to JSON)

## Dependency Rules
- Tasks with unfinished dependencies should stay "Pending"
- Task cannot depend on itself
- No circular dependencies (A→B→C→A)
- All dependency IDs must reference existing tasks
- Subtasks can depend on other subtasks from the same parent

## Difficulty Rules
- Tasks with difficulty ≥7 should be broken down using breakdown.md
- Subtasks should each have difficulty ≤6
- Difficulty should match criteria in difficulty-guide.md
- Parent task's original difficulty is preserved even after breakdown

## Parent-Child Relationship Rules
- If task has `parent_task` set, it must be listed in parent's `subtasks` array
- If task has entries in `subtasks` array, those tasks must have `parent_task` pointing back
- A task cannot be both a parent and a subtask (no nesting beyond one level)
- All subtasks of a "Broken Down" parent must exist as valid task files

## ATEF Optional Fields (Backward Compatible)

These fields are optional and only used when ATEF features are enabled.

### Validation Field Structure
- **Type**: Object (optional)
- **Purpose**: Track validation gate results
- **Properties**:
  - `pre_gate_passed` (boolean): Whether pre-execution gate passed
  - `post_gate_passed` (boolean): Whether post-execution gate passed
  - `warnings` (array of strings): Warnings from validation gates
  - `gate_results` (array of objects): Full gate result objects for audit trail
- **Rules**:
  - If `validation` exists, recommend including at least one of: `pre_gate_passed`, `post_gate_passed`
  - `gate_results` should conform to gate-result.schema.json if present
  - Can be added by complete-task.md when validation gates enabled

### Patterns Field Structure
- **Type**: Object (optional)
- **Purpose**: Track which pattern was applied during task execution
- **Properties**:
  - `pattern_id` (string): Pattern file name (e.g., "power-query-bronze.pattern.md")
  - `applied_at` (string, ISO 8601 date-time): When pattern was applied
  - `parameters` (object): Parameters passed to pattern (key-value pairs)
- **Rules**:
  - If `patterns` exists, `pattern_id` should be required
  - `pattern_id` should reference a valid pattern file in pattern library
  - `applied_at` should be ISO 8601 format timestamp
  - Can be added by apply-pattern.md command

### Checkpoints Field Structure
- **Type**: Array of strings (optional)
- **Purpose**: Track checkpoints created during task execution
- **Item Format**: `chk-{task_id}-{sequence}` (e.g., "chk-42-1", "chk-42-2")
- **Rules**:
  - Each checkpoint ID must match pattern `^chk-[0-9]+-[0-9]+$`
  - Checkpoint IDs should reference valid checkpoint metadata in `.claude/checkpoints/`
  - Array should be ordered chronologically (earliest first)
  - Can be appended by create-checkpoint.md command

### Errors Encountered Field Structure
- **Type**: Array of strings (optional)
- **Purpose**: Track errors that occurred during task execution
- **Item Format**: `ERR-{CATEGORY}-{NUMBER}` (e.g., "ERR-PQ-001", "ERR-DAX-002")
- **Rules**:
  - Each error ID must match pattern `^ERR-[A-Z]+-[0-9]+$`
  - Error IDs should reference valid errors in error catalog (common-errors.json)
  - Can be appended by log-error.md command
  - Helps track which errors occurred for learning purposes

## ATEF Cross-Field Validation Rules

### Validation and Status
- If `validation.post_gate_passed` is `false`, status should not be "Finished" (gate failure suggests incomplete work)
- If status is "Finished", recommend `validation.post_gate_passed` is `true` (successful completion)

### Checkpoints and Status
- Checkpoints typically created when status is "In Progress" or transitioning to "In Progress"
- If `checkpoints` array is non-empty, task has used checkpoint system for safety

### Errors and Checkpoints
- If `errors_encountered` is non-empty, there should likely be checkpoints (errors often require rollback)
- Presence of errors may explain extended `actual_hours` or task complexity

### Patterns and Files Affected
- If `patterns.pattern_id` is set, the pattern's expected output files should align with `files_affected`
- Pattern parameters should be consistent with task description and files

### Optional vs. Required
- All ATEF fields are **optional** (tasks without these fields are still valid)
- Older task files without ATEF fields remain fully compatible
- Commands should check for field existence before reading ATEF data
