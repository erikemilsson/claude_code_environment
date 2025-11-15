# Command: Complete Task

## Purpose
Begin working on a task with proper status tracking. This is the standard way to start any task work.

## Context Required
- Specific task JSON file (e.g., `.claude/tasks/task-X.json`)
- `.claude/tasks/task-overview.md`
- `.claude/context/validation-rules.md`
- Any context files relevant to the task

## Process
1. **Load task details:**
   - Read the specified task JSON file
   - Read task-overview.md to check dependencies and current state
   - **Check if status is "Broken Down":**
     * If yes, halt with message: "❌ Task {id} has been broken down into subtasks {list}. Please work on the individual subtasks instead. Use '@.claude/commands/complete-task.md {subtask_id}' to start a subtask."
   - Verify all dependencies are marked "Finished"

2. **Confirm with user:**
   - Display task title, description, and estimated hours
   - Show any blockers or dependencies
   - If task has `parent_task`, show parent context
   - Ask: "Ready to start work on Task X: [title]? (yes/no)"
   - Wait for user confirmation before proceeding

3. **Update status to "In Progress":**
   - Update task JSON file:
     * `"status": "In Progress"`
     * `"updated_date"` to current date (YYYY-MM-DD format)
     * If not already set, add `"actual_hours": 0`

4. **Sync overview:**
   - Run @.claude/commands/sync-tasks.md to update task-overview.md

5. **Begin work:**
   - Load any standards or context files mentioned in `files_affected`
   - Perform the task work
   - Track any issues or notes

6. **Update upon completion:**
   - Update task JSON file:
     * `"status": "Finished"`
     * `"updated_date"` to completion date
     * `"actual_hours"` with time spent
     * Add any relevant notes to `"notes"` field

   - **Check for parent task auto-completion:**
     * Read task's `parent_task` field
     * If parent_task exists:
       - Load parent task JSON file
       - If parent status == "Broken Down":
         * Get all task IDs from parent's `subtasks` array
         * Load each subtask JSON and check status
         * If ALL subtasks are "Finished":
           - Update parent task JSON:
             * `"status": "Finished"`
             * `"updated_date"` to current date
             * Add to `"notes"`: "Auto-completed: all subtasks finished on {date}"
           - Report to user: "🎉 Completing this subtask also completed parent Task #{parent_id}: {parent_title}!"

7. **Final sync and feedback:**
   - Run @.claude/commands/sync-tasks.md again
   - Provide completion summary:
     * What was accomplished
     * Any blockers encountered
     * Estimated vs actual hours
     * Files created/modified
     * If parent was auto-completed, mention it
     * Suggested next task (lowest difficulty with no dependencies)

## Output Location
- Updated task JSON file in `.claude/tasks/`
- Possibly updated parent task JSON file (if auto-completion triggered)
- Updated `.claude/tasks/task-overview.md` (via sync-tasks)
- Console feedback on task progress and completion
- Any work products in their appropriate project locations

## Example: Parent Auto-Completion

User: @.claude/commands/complete-task.md 17

[Task work happens...]

✅ Task #17 "Add error handling" completed!

- Estimated: 3 hours
- Actual: 2.5 hours
- Files modified: src/etl/error_handler.py, tests/test_errors.py

🎉 Completing this subtask also completed parent Task #12: "Build emissions data ETL pipeline"! All 5 subtasks (13-17) are now finished.

Suggested next task: Task #18 "Create dashboard mockups" (difficulty: 4)
