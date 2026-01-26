# Archive Tasks

Move completed tasks to archive to reduce token usage in large projects.

## Usage

```
/archive-tasks [--days N] [--threshold N] [--dry-run]
```

## Process

1. Determine which tasks to archive based on mode (time-based or count-based)
2. Verify no active tasks depend on them
3. Move task files to `.claude/tasks/archive/`
4. Update `archive-index.json` with lightweight summaries
5. Run `/sync-tasks` to update overview

## Options

- `--days N`: Archive tasks finished more than N days ago (default: 7)
- `--threshold N`: Archive oldest finished tasks until active count <= N (count-based mode)
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
Archives oldest finished tasks until active task count is <= 100. Useful for:
- Keeping context window manageable
- Projects that grow faster than the 7-day window clears
- Maintaining consistent performance regardless of project velocity

**Selection order for count-based:**
1. Finished tasks sorted by completion_date (oldest first)
2. Subtasks follow their parent task
3. Tasks with active dependents are skipped

## When to Use

- When task count exceeds ~100 and most are finished
- Before starting a new project phase
- When `/sync-tasks` feels slow
- When context window fills with historical task data
- For fast-moving projects where 7-day window isn't enough (use `--threshold`)
- When `/health-check` warns about high task count

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
    {"id": "1", "title": "Setup project", "completion_date": "2026-01-10", "difficulty": 3, "owner": "claude"}
  ]
}
```

## Example

```bash
# See what would be archived (time-based, default 7 days)
/archive-tasks --dry-run

# Archive tasks finished more than 14 days ago
/archive-tasks --days 14

# Archive with default settings (7 days)
/archive-tasks

# Keep active task count under 100 (count-based)
/archive-tasks --threshold 100

# Preview count-based archiving
/archive-tasks --threshold 100 --dry-run

# Aggressive cleanup for large projects
/archive-tasks --threshold 50
```

## Combining Options

Options can be combined for fine-grained control:

```bash
# Archive tasks older than 3 days, but only if count > 80
/archive-tasks --days 3 --threshold 80
```

When both `--days` and `--threshold` are specified:
1. First filters to tasks finished > N days ago
2. Then archives oldest until count <= threshold

## Restoring Tasks

If you need a task back:
```
/restore-task {id}
```

## Script Usage

```bash
python scripts/task-manager.py archive --days 7
python scripts/task-manager.py archive --threshold 100
python scripts/task-manager.py archive --dry-run
```
