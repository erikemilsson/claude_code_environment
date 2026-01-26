# Restore Task

Move a task from archive back to active tasks.

## Usage

```
/restore-task {id}
```

## Process

1. Find task in `.claude/tasks/archive/`
2. Move task file back to `.claude/tasks/`
3. Restore subtasks if this is a parent task
4. Update `archive-index.json`
5. Run `/sync-tasks` to update overview

## When to Use

- Task needs rework or follow-up
- Active task has dependency on archived task
- Reopening a feature for modifications
- Reference needed during related work

## Example

```bash
# Restore a single task
/restore-task 42

# Restore a parent task (subtasks come with it)
/restore-task 78
```

## Notes

- Parent tasks restore with all their subtasks
- Restored tasks keep their original completion status
- You may want to change status back to "In Progress" if reworking

## Script Usage

```bash
python scripts/task-manager.py restore --task-id 42
```
