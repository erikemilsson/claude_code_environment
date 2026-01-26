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
4. Do the work

### Finishing
1. **Check work**: Review all changes made for this task
   - Look for bugs, edge cases, inefficiencies, inconsistencies
   - If issues found, fix them before proceeding
2. Update status to "Finished"
3. Add completion notes (what was done, any follow-ups needed)
4. Check parent auto-completion:
   ```
   IF parent_task exists:
     IF all sibling subtasks are "Finished":
       Set parent status to "Finished"
   ```
5. Run sync-tasks to update overview

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
  "notes": "Added email format and password strength checks in auth.py"
}
```

## Rules
- Never work on "Broken Down" tasks directly - work on their subtasks
- Parent tasks auto-complete when all subtasks finish
- Always add notes about what was actually done
