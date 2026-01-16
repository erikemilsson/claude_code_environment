# Update Tasks

Check task system health and fix inconsistencies.

## Usage
```
/update-tasks
```

## Checks

1. **Structure**: All tasks have required fields (id, title, status)
2. **Relationships**:
   - Subtasks reference valid parents
   - Parents list all their subtasks
3. **Status consistency**:
   - "Broken Down" tasks have subtasks
   - No orphaned subtasks
4. **Staleness**:
   - "In Progress" tasks that haven't been touched
   - "Blocked" tasks without notes explaining why

## Fixes

- Auto-complete parents when all subtasks are finished
- Flag tasks that need attention
- Run sync-tasks to update overview

## When to Run
- Start of work session
- When something seems off
- After manual task file edits
