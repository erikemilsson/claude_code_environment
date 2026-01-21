# Sync Tasks

Update task-overview.md from task JSON files.

## Usage
```
/sync-tasks
```

## Process

1. Read all `.claude/tasks/task-*.json` files (active tasks only)
2. Generate markdown table showing:
   - ID, Title, Status, Difficulty
   - Subtask progress for broken-down tasks
3. Add archive summary if tasks have been archived
4. Write to `.claude/tasks/task-overview.md`

## Output Format

```markdown
# Task Overview

| ID | Title | Status | Difficulty |
|----|-------|--------|------------|
| 1 | Setup project | Finished | 3 |
| 2 | Build API | Broken Down (2/4) | 8 |
| 2_1 | Design endpoints | Finished | 4 |
| 2_2 | Implement routes | Finished | 5 |
| 2_3 | Add validation | In Progress | 4 |
| 2_4 | Write tests | Pending | 4 |
| 3 | Deploy | Pending | 5 |

Summary: 3/7 complete

## Archived (50 tasks)
Last archived: 2026-01-21
```

## When to Run
- After completing any task
- After breaking down a task
- When starting a work session (to see current state)
- After archiving tasks

## Archive Integration

- Only reads active tasks (not archived ones)
- Shows archive summary at bottom if archive exists
- Use `/archive-tasks` to move old finished tasks to archive
- Use `/restore-task` to bring tasks back from archive
