# Sync Tasks Command

## Purpose
Update task-overview.md from all task JSON files.

## Context Required
- Task JSON files in `.claude/tasks/`

## Process
1. Read all task-*.json files
2. Generate markdown table with:
   - ID, Title, Difficulty, Status
   - Dependencies and subtasks
   - Tags and priority
3. Group by status
4. Calculate statistics
5. Write to task-overview.md

## Output Location
`.claude/tasks/task-overview.md`

## When to Run
- After completing any task
- After breakdown operation
- After creating new tasks
- When checking project status