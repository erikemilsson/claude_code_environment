# Archive Tasks

Move completed tasks to archive to reduce token usage in large projects.

## Usage

```
/archive-tasks [--days N] [--dry-run]
```

## Process

1. Find finished tasks completed more than N days ago (default: 7)
2. Verify no active tasks depend on them
3. Move task files to `.claude/tasks/archive/`
4. Update `archive-index.json` with lightweight summaries
5. Run `/sync-tasks` to update overview

## Options

- `--days N`: Archive tasks finished more than N days ago (default: 7)
- `--dry-run`: Show what would be archived without doing it

## When to Use

- When task count exceeds ~100 and most are finished
- Before starting a new project phase
- When `/sync-tasks` feels slow
- When context window fills with historical task data

## What Gets Archived

- **Parent tasks**: Moved with all their subtasks
- **Subtasks**: Follow their parent task
- **Dependencies**: Tasks with active dependents are skipped

## Archive Structure

```
.claude/tasks/archive/
├── task-1.json           # Full task data (preserved)
├── task-2.json
├── task-2_1.json         # Subtasks follow parent
├── task-2_2.json
└── archive-index.json    # Lightweight summary
```

## Archive Index

Only stores ~50 tokens per task:
```json
{
  "archived_at": "2026-01-21",
  "count": 150,
  "tasks": [
    {"id": "1", "title": "Setup project", "completion_date": "2026-01-10", "difficulty": 3}
  ]
}
```

## Example

```bash
# See what would be archived
/archive-tasks --dry-run

# Archive tasks finished more than 14 days ago
/archive-tasks --days 14

# Archive with default settings (7 days)
/archive-tasks
```

## Restoring Tasks

If you need a task back:
```
/restore-task {id}
```

## Script Usage

```bash
python scripts/task-manager.py archive --days 7
python scripts/task-manager.py archive --dry-run
```
