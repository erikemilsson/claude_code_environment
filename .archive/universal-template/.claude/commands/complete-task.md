# Command: complete-task

## Purpose
Start or finish a task with proper status tracking and validation.

## Usage
```
/complete-task task-042 start   # Mark task as in_progress
/complete-task task-042 finish  # Mark task as finished
```

## Context Required
- Task ID to work on
- Understanding of task requirements from task JSON file

## Process

### Starting a Task

1. **Read task file** `.claude/tasks/task-{id}.json`
2. **Validate task readiness**:
   - Status must be "pending" (or "blocked" if blockers resolved)
   - Not "broken_down" (work on subtasks instead)
   - Not already "finished"
   - Check dependencies are met
3. **Update task file**:
   - Set `status: "in_progress"`
   - Update `updated` field to today's date
4. **Display task details** to user
5. **Begin work** on the task

### Finishing a Task

1. **Validate completion**:
   - All requirements from description addressed
   - Quality standards met
   - No obvious issues
   - Acceptance criteria satisfied
2. **Update task file**:
   - Set `status: "finished"`
   - Update `updated` field
   - Set `validation.completed: true` if all criteria met
   - Add notes about what was done
3. **Check parent task**:
   - If `parent_task` is not null, read parent
   - Read all sibling tasks
   - If ALL siblings have `status: "finished"`:
     - Set parent `status: "finished"`
     - Add note to parent: "Auto-completed (all subtasks finished)"
4. **Run /sync-tasks** to update task-overview.md

## Output Location
- Updated task JSON file(s)
- Updated task-overview.md (via /sync-tasks)

## Critical Rules

**ALWAYS:**
- Check parent task status when completing subtasks
- Add notes about what was actually done
- Run /sync-tasks after finishing any task

**NEVER:**
- Mark "broken_down" tasks as complete (they auto-complete when subtasks finish)
- Skip validation criteria
- Work on multiple tasks simultaneously (one task in_progress at a time)

## Example

```
User: /complete-task task-025 start

Claude: Starting task-025...

Task: Add user profile page
Status: pending → in_progress
Difficulty: 5
Priority: medium

Requirements:
- Display current user info from API
- Form for editing name and email
- Image upload for avatar
- Save changes via PUT /api/users/:id

Beginning work...

[Work continues]

User: /complete-task task-025 finish

Claude: Validating task-025 completion...

✓ All requirements addressed
✓ Profile page renders at /profile
✓ User data loads correctly
✓ Form validation works
✓ Save functionality tested

Marking task-025 as finished...

✓ Task updated
✓ No parent task to check

Running /sync-tasks...

✓ Task overview updated

Task-025 complete! Review task-overview.md for next steps.
```
