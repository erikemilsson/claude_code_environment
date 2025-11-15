# Sync Tasks Command

## Purpose
Update `task-overview.md` to reflect current state of all task JSON files.

## Process

1. **Scan all task files** in `.claude/tasks/`
2. **Extract key information**: ID, title, status, difficulty, parent/subtasks
3. **Generate markdown table** with columns: ID, Title, Status, Difficulty, Dependencies, Subtasks
4. **Calculate statistics**: Total tasks, by status, by difficulty
5. **Write to** `.claude/tasks/task-overview.md`

## Output Location
`.claude/tasks/task-overview.md`

## When to Use
- After creating/updating any task file
- Before starting work session (to see current state)
- After completing tasks
- When task relationships change
