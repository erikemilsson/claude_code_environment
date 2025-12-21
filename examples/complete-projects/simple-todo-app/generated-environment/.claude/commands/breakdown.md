# Task Breakdown Command

## Purpose
Break down high-difficulty tasks (7+) into manageable subtasks.

## Context Required
- Task with difficulty >= 7
- Understanding of task scope

## Process
1. Read parent task file
2. Analyze complexity and identify logical components
3. Create subtask files with:
   - Difficulty 1-6
   - Clear dependencies
   - Parent task reference
4. Update parent task:
   - Status to "Broken Down"
   - Add subtask IDs
5. Run sync-tasks

## Output Location
- New subtask JSON files
- Updated parent task
- Updated task-overview.md

## Rules
- Each subtask difficulty <= 6
- Subtasks should be independently completable
- Parent auto-completes when all subtasks finish