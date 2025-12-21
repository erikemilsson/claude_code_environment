# Complete Task Command

## Purpose
Start and finish tasks with proper status tracking.

## Context Required
- Task ID to work on
- Understanding of task requirements

## Process

### Starting a Task
1. Read task file `.claude/tasks/task-{id}.json`
2. Validate task is workable (status must be "Pending" or "In Progress")
3. Update status to "In Progress"
4. Perform the work

### Finishing a Task
1. Complete all work described in task
2. Update status to "Finished"
3. Add completion notes
4. Check for parent task auto-completion
5. Run sync-tasks to update overview

## Output Location
- Updated task JSON file
- Updated task-overview.md (via sync-tasks)