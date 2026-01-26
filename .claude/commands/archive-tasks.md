# Archive Tasks

Move completed tasks to archive to reduce token usage in large projects.

## Usage

```
/archive-tasks [--days N] [--threshold N] [--dry-run]
```

## Options

- `--days N`: Archive tasks finished more than N days ago (default: 7)
- `--threshold N`: Archive oldest finished tasks until active count <= N
- `--dry-run`: Show what would be archived without doing it

## Modes

### Time-Based (Default)
```
/archive-tasks --days 7
```
Archives all finished tasks completed more than 7 days ago.

### Count-Based
```
/archive-tasks --threshold 100
```
Archives oldest finished tasks until active task count is <= 100.

## Process

1. Determine which tasks to archive based on mode
2. Verify no active tasks depend on them
3. Move task files to `.claude/tasks/archive/`
4. Update `archive-index.json` with lightweight summaries
5. Run `/sync-tasks` to update overview

## Archive Structure

```
.claude/tasks/archive/
├── task-1.json           # Full task data (preserved)
├── task-2.json
└── archive-index.json    # Lightweight summary
```

## Archive Index

```json
{
  "archived_at": "2026-01-21",
  "count": 50,
  "tasks": [
    {"id": "1", "title": "Setup project", "completion_date": "2026-01-10", "difficulty": 3}
  ]
}
```

## When to Use

- When task count exceeds ~100 and most are finished
- Before starting a new project phase
- When context window fills with historical task data

## Example

```
# See what would be archived
/archive-tasks --dry-run

# Archive tasks finished more than 14 days ago
/archive-tasks --days 14

# Keep active task count under 100
/archive-tasks --threshold 100
```
