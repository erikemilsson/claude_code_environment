# Task Schema

## Minimal Task

```json
{
  "id": "1",
  "title": "Brief description",
  "status": "Pending",
  "difficulty": 3
}
```

## Full Task

```json
{
  "id": "1",
  "title": "Brief description",
  "description": "Detailed explanation of what needs to be done",
  "status": "Pending",
  "difficulty": 3,
  "created_date": "2025-01-15",
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "files_affected": [],
  "notes": ""
}
```

## Field Definitions

### id (required)
- Type: String
- Format: Number for top-level tasks ("1", "2"), underscore notation for subtasks ("1_1", "1_2")

### title (required)
- Type: String
- Brief description of what needs to be done

### status (required)
- Type: String
- Values:
  - `Pending` - Not started
  - `In Progress` - Currently working on
  - `Blocked` - Cannot proceed (document blocker in notes)
  - `Broken Down` - Split into subtasks
  - `Finished` - Complete

### difficulty (required)
- Type: Number (1-10)
- See difficulty-guide.md for detailed examples

### description (optional)
- Type: String
- Detailed explanation when title isn't enough

### created_date (optional)
- Type: String (YYYY-MM-DD)
- When the task was created

### dependencies (optional)
- Type: Array of task ID strings
- Tasks that must finish before this one can start

### subtasks (optional)
- Type: Array of task ID strings
- Only used when status is "Broken Down"

### parent_task (optional)
- Type: String or null
- References parent task if this is a subtask

### files_affected (optional)
- Type: Array of file paths
- What files this task will create or modify

### notes (optional)
- Type: String
- Additional context, warnings, or completion notes

## Status Rules

1. Only work on tasks with status "Pending" or "In Progress"
2. Never work directly on "Broken Down" tasks - work on subtasks
3. "Broken Down" tasks auto-complete when all subtasks are "Finished"
4. Document blockers when setting status to "Blocked"

## Task Archiving

For large projects (100+ tasks), finished tasks can be archived to reduce token usage.

### Archive Directory Structure

```
.claude/tasks/
├── task-*.json           # Active tasks
├── task-overview.md      # Active task overview
└── archive/
    ├── task-*.json       # Archived task files (full data)
    └── archive-index.json # Lightweight summary
```

### Archive Index Format

```json
{
  "archived_at": "2026-01-21",
  "count": 50,
  "tasks": [
    {"id": "1", "title": "Setup project", "completion_date": "2026-01-10", "difficulty": 3}
  ]
}
```

### Archiving Rules

1. **Eligibility**: Status = "Finished" AND completion_date > 7 days ago
2. **Subtasks follow parents**: When parent is archived, all subtasks go with it
3. **Dependencies honored**: Tasks with active dependents are not archived
4. **Reversible**: Use `/restore-task` to bring tasks back

### Commands

- `/archive-tasks` - Move old finished tasks to archive
- `/archive-tasks --dry-run` - Preview what would be archived
- `/restore-task {id}` - Restore a task from archive

### Token Savings

| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| 250 tasks (150 finished) | ~75K tokens | ~30K tokens | 60% |
