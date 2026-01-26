# Sync Tasks

Update task-overview.md from task JSON files.

## Usage
```
/sync-tasks
```

## Process

1. Read all `.claude/tasks/task-*.json` files (active tasks only)
2. Calculate statistics by owner and status
3. Generate owner-grouped sections for pending tasks
4. Generate full task list table
5. Add archive summary if tasks have been archived
6. Write to `.claude/tasks/task-overview.md`

## Output Format

```markdown
# Task Overview

<!-- Auto-generated. Do not edit manually. Run /sync-tasks to update. -->
Generated: {date}

## Quick Stats

- **Total**: 15 (8 remaining)
- **Claude**: 5 pending | **Human**: 2 pending | **Both**: 1 pending

## Human Tasks - Ready Now

| ID | Title | Difficulty |
|----|-------|------------|
| 23 | Configure dashboard | 4 |

## Human Tasks - Waiting on Claude

| ID | Title | Blocked By |
|----|-------|------------|
| 67 | Deploy to prod | Task 66 (API endpoint) |

## Claude Tasks - Ready Now

| ID | Title | Difficulty |
|----|-------|------------|
| 44 | Build API endpoint | 5 |

## Full Task List

| ID | Title | Status | Difficulty | Owner |
|----|-------|--------|------------|-------|
| 1 | Setup project | Finished | 3 | claude |
| 2 | Build API | In Progress | 5 | claude |

Summary: 3/7 complete
```

## Owner Field

Tasks can have an `owner` field:
- `claude` - Claude will do this task (default when not specified)
- `human` - Requires human action
- `both` - Collaborative task

## Ready vs Blocked Logic

**Ready Now**: Task is `Pending` AND all dependencies are `Finished`

**Waiting/Blocked**: Task is `Pending` AND has unfinished dependencies

## When to Run
- After completing any task
- After breaking down a task
- When starting a work session
- After archiving tasks
