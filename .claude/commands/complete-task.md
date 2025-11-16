# Complete Task Command

## Purpose
Start and finish tasks with proper status tracking.

## Context Required
- Task ID to work on
- Understanding of task requirements

## Process

### Starting a Task
1. **Read task file** `.claude/tasks/task-{id}.json`
2. **Validate task is workable**:
   - Status must be "Pending" or "In Progress"
   - Cannot be "Broken Down" (work on subtasks instead)
   - Check dependencies are met
3. **Update status** to "In Progress"
4. **Show task details** to confirm understanding
5. **Perform the work**

### Finishing a Task
1. **Complete all work** described in task
2. **Document any issues encountered**:
   - If something didn't go as planned, explicitly state what happened
   - Document any fixes or workarounds applied during completion
   - Create new tasks for unexpected issues that need follow-up
   - Be transparent about scope changes or deviations from original plan
3. **Update status** to "Finished"
4. **Add completion notes** with:
   - What was actually done
   - Any fixes or adjustments made
   - New tasks created (if applicable)
   - Links to relevant files or commits
5. **Check for parent task**:
   - If exists, check if all sibling tasks are finished
   - If yes, automatically update parent to "Finished"
   - Update parent progress indicator
6. **Run sync-tasks** to update overview

## Output Location
- Updated task JSON file
- Updated task-overview.md (via sync-tasks)
- Parent task JSON if applicable

## Critical Rules
- Never mark "Broken Down" tasks as complete (they auto-complete when subtasks finish)
- Always check parent task status when completing subtasks
- Add notes about what was actually done
- **Transparency Requirements**:
  - If implementation deviated from original plan, document why
  - If bugs were fixed during completion, note what was broken
  - If workarounds were needed, explain what didn't work as expected
  - If new tasks were created, reference them in notes
  - Never silently fix issues - always document changes made
