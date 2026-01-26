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
| owner | String | claude (default), human, or both - see Owner Values below |
| created_date | String | YYYY-MM-DD format |
| updated_date | String | YYYY-MM-DD format |
| completion_date | String | YYYY-MM-DD format, set when Finished |
| dependencies | Array | Task IDs that must finish first |
| subtasks | Array | Task IDs (only when Broken Down) |
| parent_task | String | Parent task ID if this is a subtask |
| files_affected | Array | File paths this task will modify |
| notes | String | Context, warnings, or completion notes |

## Owner Values

The `owner` field determines who is responsible and where tasks appear in the dashboard:

| Value | Emoji | Dashboard Section | When to Use |
|-------|-------|-------------------|-------------|
| `claude` | 🤖 | Claude Status | Tasks Claude can do autonomously (default) |
| `human` | ❗ | Your Actions | Requires human action (config, decisions, external) |
| `both` | 👥 | Both sections | Collaborative work (appears in BOTH dashboard sections) |

### Examples by Owner

**`claude`** (default - omit field if this):
- Write code, implement features
- Create tests, documentation
- Refactor, fix bugs
- Research and analysis

**`human`**:
- Configure API keys, secrets
- Make business decisions
- External actions (deploy, purchase, contact)
- Review and approve

**`both`**:
- Design work (human provides direction, Claude implements)
- Content requiring human judgment (Claude drafts, human refines)

## Status Rules

1. Only work on tasks with status "Pending" or "In Progress"
2. Never work directly on "Broken Down" tasks - work on subtasks
3. "Broken Down" tasks auto-complete when all subtasks are "Finished"
4. Document blockers when setting status to "Blocked"

## Task Archiving

For large projects (100+ tasks), finished tasks can be archived.

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
