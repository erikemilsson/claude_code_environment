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
  "owner": "claude",
  "created_date": "2026-01-15",
  "updated_date": "2026-01-15",
  "completion_date": null,
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "files_affected": [],
  "notes": ""
}
```

## Field Definitions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| id | String | Number for top-level ("1"), underscore for subtasks ("1_1") |
| title | String | Brief description of what needs to be done |
| status | String | Pending, In Progress, Blocked, Broken Down, Finished |
| difficulty | Number | 1-10 scale (see shared-definitions.md) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| description | String | Detailed explanation when title isn't enough |
| owner | String | claude (default), human, or both |
| created_date | String | YYYY-MM-DD format |
| updated_date | String | YYYY-MM-DD format |
| completion_date | String | YYYY-MM-DD format, set when Finished |
| dependencies | Array | Task IDs that must finish first |
| subtasks | Array | Task IDs (only when Broken Down) |
| parent_task | String | Parent task ID if this is a subtask |
| files_affected | Array | File paths this task will modify |
| notes | String | Context, warnings, or completion notes |

## Status Rules

1. Only work on tasks with status "Pending" or "In Progress"
2. Never work directly on "Broken Down" tasks - work on subtasks
3. "Broken Down" tasks auto-complete when all subtasks are "Finished"
4. Document blockers when setting status to "Blocked"

## Task Archiving

For large projects (100+ tasks), finished tasks can be archived to reduce context size.

### Archive Structure

```
.claude/tasks/
├── task-*.json           # Active tasks
├── task-overview.md      # Auto-generated summary
└── archive/
    ├── task-*.json       # Archived task files
    └── archive-index.json # Lightweight summary
```

### Commands

- `/archive-tasks` - Move old finished tasks to archive
- `/restore-task {id}` - Restore a task from archive
