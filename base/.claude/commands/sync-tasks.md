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
6. Trigger workflow diagram regeneration if task count > 20
7. Write to `.claude/tasks/task-overview.md`

## Output Format

```markdown
# Task Overview

<!-- Auto-generated. Do not edit manually. Run /sync-tasks to update. -->
Generated: {date}

## Quick Stats

- **Total**: 150 (50 remaining)
- **Claude**: 30 pending | **Human**: 15 pending | **Both**: 5 pending

## Human Tasks - Ready Now

| ID | Title | Difficulty |
|----|-------|------------|
| 23 | Configure dashboard | 4 |
| 45 | Review mockups | 3 |

## Human Tasks - Waiting on Claude

| ID | Title | Blocked By |
|----|-------|------------|
| 67 | Deploy to prod | Task 66 (API endpoint) |

## Claude Tasks - Ready Now

| ID | Title | Difficulty |
|----|-------|------------|
| 44 | Build API endpoint | 5 |
| 52 | Write tests | 4 |

## Claude Tasks - Blocked

| ID | Title | Blocked By |
|----|-------|------------|
| 78 | Integration | Task 45 (human review) |

## Collaborative Tasks (Both) - Ready Now

| ID | Title | Difficulty |
|----|-------|------------|
| 89 | Final review meeting | 3 |

## Collaborative Tasks (Both) - Blocked

| ID | Title | Blocked By |
|----|-------|------------|
| 92 | Integration testing | Task 78 (Integration) |

## Full Task List

| ID | Title | Status | Difficulty | Owner |
|----|-------|--------|------------|-------|
| 1 | Setup project | Finished | 3 | claude |
| 2 | Build API | Broken Down (2/4) | 8 | claude |
| 2_1 | Design endpoints | Finished | 4 | claude |
| 2_2 | Implement routes | Finished | 5 | claude |
| 2_3 | Add validation | In Progress | 4 | claude |
| 2_4 | Write tests | Pending | 4 | claude |
| 3 | Configure dashboard | Pending | 5 | human |

Summary: 3/7 complete

## Archived (50 tasks)
Last archived: 2026-01-21
```

## Owner Field

Tasks can have an `owner` field:
- `claude` - Claude will do this task (default when not specified)
- `human` - Requires human action
- `both` - Collaborative task

Tasks without an `owner` field default to `"claude"`.

## Ready vs Blocked Logic

**Ready Now**: Task is `Pending` AND all dependencies are `Finished`

**Waiting/Blocked**: Task is `Pending` AND has unfinished dependencies
- Shows which task(s) it's waiting on
- Cross-owner blocking is highlighted (Claude waiting on Human, or vice versa)

## Diagram Integration

When task count exceeds 20, sync-tasks automatically triggers workflow diagram regeneration:
1. Calls `/generate-workflow-diagram` logic
2. Updates `.claude/tasks/workflow-diagram.md`
3. This provides visual overview for large collaborative projects

To disable automatic diagram generation, create an empty `.claude/tasks/.no-auto-diagram` file.

## When to Run
- After completing any task
- After breaking down a task
- When starting a work session (to see current state)
- After archiving tasks
- After adding `owner` field to tasks

## Archive Integration

- Only reads active tasks (not archived ones)
- Shows archive summary at bottom if archive exists
- Use `/archive-tasks` to move old finished tasks to archive
- Use `/restore-task` to bring tasks back from archive

## "Plan My Day" Use Case

The owner-grouped format directly answers "What can I work on today?":

1. Look at **Human Tasks - Ready Now** for immediate human work
2. Look at **Human Tasks - Waiting on Claude** to see what Claude needs to unblock
3. The workflow diagram (if generated) shows the full dependency chain
