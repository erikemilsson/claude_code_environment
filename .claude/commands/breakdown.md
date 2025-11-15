# Breakdown Task Command

## Purpose
Split high-difficulty tasks (≥7) into manageable subtasks (≤6 difficulty each).

## Context Required
- Task ID to break down
- Understanding of task scope and requirements

## Process

1. **Read task file** `.claude/tasks/task-{id}.json`
2. **Validate task needs breakdown**:
   - Difficulty ≥ 7, or
   - User requests breakdown regardless of difficulty
3. **Analyze task** into logical subtasks
4. **Create subtask files**:
   - Each subtask difficulty ≤ 6
   - Clear, actionable descriptions
   - Proper dependency chains
   - Set `parent_task` field to original task ID
5. **Update parent task**:
   - Set status to "Broken Down"
   - Add subtask IDs to `subtasks` array
   - Add progress note: "Broken Down (0/X done)"
6. **Run sync-tasks** to update overview

## Output Location
- New task files: `.claude/tasks/task-{new-id}.json` for each subtask
- Updated parent task file
- Updated task-overview.md

## Critical Rules
- Parent task becomes a container (cannot be worked on directly)
- All subtasks must have difficulty ≤ 6
- Subtasks should be independently completable when dependencies allow
- Parent auto-completes when last subtask finishes
