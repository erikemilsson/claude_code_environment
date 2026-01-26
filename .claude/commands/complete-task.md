# Complete Task

Start and finish a task with status tracking.

## Usage
```
/complete-task {id}
```

## Process

### Starting
1. Read `.claude/tasks/task-{id}.json`
2. Verify task is workable:
   - Status must be "Pending" or "In Progress" (not "Broken Down" or "Finished")
   - Dependencies must all be "Finished"
3. Set status to "In Progress"
4. Set `updated_date` to today (YYYY-MM-DD)
5. Do the work

### Finishing
1. **Check work**: Review all changes made for this task
   - Look for bugs, edge cases, inefficiencies
   - If issues found, fix them before proceeding
2. Update status to "Finished"
3. Set `completion_date` to today (YYYY-MM-DD)
4. Set `updated_date` to today (YYYY-MM-DD)
5. Add completion notes (what was done, any follow-ups needed)
6. Check parent auto-completion:
   ```
   IF parent_task exists:
     IF all sibling subtasks are "Finished":
       Set parent status to "Finished"
   ```
7. Run `/sync-tasks` to update overview

## Example

**Task file before:**
```json
{
  "id": "3",
  "title": "Add user validation",
  "status": "Pending",
  "difficulty": 4
}
```

**Task file after:**
```json
{
  "id": "3",
  "title": "Add user validation",
  "status": "Finished",
  "difficulty": 4,
  "updated_date": "2026-01-26",
  "completion_date": "2026-01-26",
  "notes": "Added email format and password strength checks in auth.py"
}
```

## Rules
- Never work on "Broken Down" tasks directly - work on their subtasks
- Parent tasks auto-complete when all subtasks finish
- Always add notes about what was actually done
