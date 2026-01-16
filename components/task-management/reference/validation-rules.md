# Task Validation Rules

## Required Fields
- `id` - Unique identifier
- `title` - What needs doing
- `status` - Current state

## Valid Statuses
- **Pending** - Not started
- **In Progress** - Working on it
- **Blocked** - Can't proceed (explain why in notes)
- **Broken Down** - Split into subtasks
- **Finished** - Done

## Status Rules

### Broken Down
- Must have subtasks
- Cannot work on directly
- Auto-completes when all subtasks finish

### Subtasks
- Must have `parent_task` pointing to parent
- Parent must list subtask in `subtasks` array

## Valid Transitions
```
Pending → In Progress → Finished
Pending → Broken Down → Finished (auto)
Pending → Blocked → In Progress
In Progress → Blocked → In Progress
```

## Invalid Transitions
- Finished → anything (done is done)
- Broken Down → In Progress (work on subtasks instead)
- Manual Broken Down → Finished (only auto-completes)

## Dependency Rules
- All dependencies must be Finished before starting
- No circular dependencies
- Dependencies must reference existing tasks
