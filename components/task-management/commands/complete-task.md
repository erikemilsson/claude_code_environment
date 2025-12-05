# Command: Complete Task (Enhanced with ATEF)

## Purpose
Begin working on a task with proper status tracking, validation gates, checkpoints, and error prevention. This is the standard way to start any task work.

## Context Required
- Specific task JSON file (e.g., `.claude/tasks/task-X.json`)
- `.claude/tasks/task-overview.md`
- `.claude/context/validation-rules.md`
- `components/validation-gates/gates/pre-execution.md` (for validation)
- `components/validation-gates/gates/post-execution.md` (for validation)
- `components/checkpoint-system/commands/create-checkpoint.md` (optional)
- Any context files relevant to the task

## Process
1. **Load task details:**
   - Read the specified task JSON file
   - Read task-overview.md to check dependencies and current state
   - **Check if status is "Broken Down":**
     * If yes, halt with message: "❌ Task {id} has been broken down into subtasks {list}. Please work on the individual subtasks instead. Use '@.claude/commands/complete-task.md {subtask_id}' to start a subtask."

2. **Run Pre-Execution Validation Gate:** (ATEF Enhancement)
   - Execute validation checks from `components/validation-gates/gates/pre-execution.md`
   - Checks performed:
     * Status Check (must be "Pending" or "In Progress", not "Broken Down" or "Finished")
     * Dependency Check (all dependencies must be "Finished")
     * Difficulty Check (if difficulty >= 7, must be broken down first)
     * Context Check (verify files in files_affected exist, warn if missing)
     * Pattern Check (search pattern library for applicable patterns)
   - **If validation FAILS (blocking failures exist):**
     * Display blocking failures with remediations
     * HALT execution with message: "Pre-execution validation failed. Resolve issues before proceeding."
     * Do NOT proceed to next steps
   - **If validation PASSES with warnings:**
     * Display warnings but allow user to continue
   - **If patterns found:**
     * Display: "Pattern available: {pattern_name}. Consider using."
     * Optionally ask: "Apply pattern {pattern_name}? [Y/N]"
   - Store gate result in task metadata (optional `validation` field)

3. **Confirm with user:**
   - Display task title, description, and estimated hours
   - Show any blockers or dependencies
   - If task has `parent_task`, show parent context
   - Include gate warnings in display (if any)
   - If pattern suggested: "A pattern is available for this task type. Use it? [Y/N]"
   - Ask: "Ready to start work on Task X: [title]? (yes/no)"
   - Wait for user confirmation before proceeding

4. **Create Checkpoint (before changes):** (ATEF Enhancement)
   - **If checkpoint system available:**
     * Call `components/checkpoint-system/commands/create-checkpoint.md`
     * Capture files listed in task's `files_affected` array
     * Generate checkpoint ID: `chk-{task_id}-{sequence}` (e.g., `chk-22-001`)
     * Save checkpoint metadata and file backups to `.claude/checkpoints/`
     * Add checkpoint ID to task's optional `checkpoints` array
     * Display: "Checkpoint {id} created. Rollback available if needed."
   - **If checkpoint system not available:** Skip this step

5. **Update status to "In Progress":**
   - Update task JSON file:
     * `"status": "In Progress"`
     * `"updated_date"` to current date (YYYY-MM-DD format)
     * If not already set, add `"actual_hours": 0`

6. **Sync overview:**
   - Run @.claude/commands/sync-tasks.md to update task-overview.md

7. **Begin work:**
   - If pattern was selected in step 3, load and follow pattern
   - Load any standards or context files mentioned in `files_affected`
   - Perform the task work
   - Track any issues or notes
   - Periodically offer to create mid-execution checkpoints for long tasks (optional)

8. **Run Post-Execution Validation Gate:** (ATEF Enhancement)
   - Execute validation checks from `components/validation-gates/gates/post-execution.md`
   - Checks performed:
     * Files Modified Check (verify files in files_affected were modified)
     * Notes Check (verify notes were added)
     * Time Tracking Check (suggest updating actual_hours if needed)
     * Parent Completion Check (auto-complete parent if all siblings finished)
     * Error Pattern Check (warn about common errors for this task type)
   - **Display results:**
     * Warnings: Show but don't block
     * Info: Display suggestions
     * Auto-actions: Confirm what was automated (e.g., parent completion)
   - **If blocking failures (rare):**
     * Offer rollback option: "Rollback to checkpoint {id}? [Y/N]"
   - Store gate result in task metadata (optional `validation` field)

9. **Update upon completion:**
   - Update task JSON file:
     * `"status": "Finished"`
     * `"updated_date"` to completion date
     * `"actual_hours"` with time spent
     * Add any relevant notes to `"notes"` field
     * If pattern was used, add to optional `patterns` field: `{"pattern_id": "pattern-xxx", "applied_at": "YYYY-MM-DD"}`
     * If validation gates ran, add results to optional `validation` field

   - **Note:** Parent task auto-completion is now handled by post-execution gate (step 8)
   - If post-execution gate auto-completed parent:
     * Parent task JSON already updated by gate
     * Display: "🎉 Completing this subtask also completed parent Task #{parent_id}: {parent_title}!"

10. **Final sync and feedback:**
   - Run @.claude/commands/sync-tasks.md again
   - Provide completion summary:
     * What was accomplished
     * Any blockers encountered
     * Estimated vs actual hours
     * Files created/modified
     * **Gate results summary (ATEF):**
       - "Validation caught {N} issues before they became problems" (if warnings/info shown)
       - Checkpoint info: "Checkpoint {id} available for reference"
       - Pattern info: "Applied pattern {pattern_id}" (if pattern used)
     * If parent was auto-completed, mention it
     * Suggested next task (lowest difficulty with no dependencies)

## Output Location
- Updated task JSON file in `.claude/tasks/`
- Possibly updated parent task JSON file (if auto-completion triggered by post-execution gate)
- Updated `.claude/tasks/task-overview.md` (via sync-tasks)
- Checkpoint files in `.claude/checkpoints/chk-{task_id}-{sequence}/` (if checkpoint system available)
- Console feedback on task progress and completion
- Any work products in their appropriate project locations

## Example: ATEF-Enhanced Task Completion with Parent Auto-Completion

User: @.claude/commands/complete-task.md 17

[Step 1: Load task]
Loaded task #17: "Add error handling"

[Step 2: Pre-execution validation]
✓ Pre-execution validation PASSED
ℹ Suggestions:
  - Pattern available: pattern-code-error-handling. Consider using.

[Step 3: Confirm]
Ready to start work on Task 17: "Add error handling"? (yes/no)
> yes

[Step 4: Checkpoint]
✓ Checkpoint chk-17-001 created. Rollback available if needed.

[Step 5-7: Status update, sync, and work...]

[Step 8: Post-execution validation]
✓ Post-execution validation PASSED
⚡ Auto-actions:
  - Parent task 12 auto-completed (all subtasks finished)

[Step 9-10: Completion]
✅ Task #17 "Add error handling" completed!

- Estimated: 3 hours
- Actual: 2.5 hours
- Files modified: src/etl/error_handler.py, tests/test_errors.py

ATEF Summary:
  - Checkpoint chk-17-001 available for reference
  - Pre-execution gate: Pattern suggested
  - Post-execution gate: Parent auto-completed

🎉 Completing this subtask also completed parent Task #12: "Build emissions data ETL pipeline"! All 5 subtasks (13-17) are now finished.

Suggested next task: Task #18 "Create dashboard mockups" (difficulty: 4)
