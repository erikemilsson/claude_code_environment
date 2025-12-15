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
3. **Update belief tracking fields**:
   - Review confidence score, adjust if needed based on new information
   - Document any new assumptions discovered
   - Update momentum phase from "pending" to "ignition"
   - Set momentum velocity to initial value (10-20)
4. **Update status** to "In Progress"
5. **Show task details** including confidence and assumptions
6. **Perform the work**

### Finishing a Task
1. **Complete all work** described in task
2. **Validate assumptions**:
   - Review each assumption in the task
   - Mark as "validated" or "invalidated" based on actual experience
   - Add validation_method and validated_date
   - Update overall validation_status (validated/invalidated/partial)
3. **Update belief tracking**:
   - **Confidence**: Adjust based on actual vs expected difficulty
     - Increase if easier than expected (+10-20)
     - Decrease if harder than expected (-10-20)
   - **Momentum**: Update phase and velocity
     - If completed quickly: phase="cruising", velocity=70-80
     - If struggled: phase="coasting", velocity=30-50
     - Calculate velocity based on time taken vs estimate
   - **Decision rationale**: Document key decisions made
     - Why specific approaches were chosen
     - Trade-offs considered
     - Alternative solutions rejected and why
4. **Document any issues encountered**:
   - If something didn't go as planned, explicitly state what happened
   - Document any fixes or workarounds applied during completion
   - Create new tasks for unexpected issues that need follow-up
   - Be transparent about scope changes or deviations from original plan
5. **Update status** to "Finished"
6. **Add completion notes** with:
   - What was actually done
   - Any fixes or adjustments made
   - New tasks created (if applicable)
   - Links to relevant files or commits
   - Assumption validation results
   - Final confidence score
7. **Check for parent task**:
   - If exists, check if all sibling tasks are finished
   - If yes, automatically update parent to "Finished"
   - Update parent progress indicator
   - Transfer momentum to parent (average of subtask velocities)
8. **Run sync-tasks** to update overview

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

## Belief Tracking Integration

### Momentum Phase Transitions
When updating momentum phase during task work:

| Current Phase | Next Phase If... | Velocity Range |
|--------------|------------------|----------------|
| pending | Starting work | ignition (10-20) |
| ignition | Making progress | building (20-50) |
| building | Steady progress | cruising (50-80) |
| cruising | Slowing down | coasting (30-60) |
| coasting | Major slowdown | stalling (10-30) |
| stalling | No progress | stopped (0) |

### Confidence Adjustments
Adjust confidence based on discoveries during task execution:

- **Increase confidence** when:
  - Requirements clearer than expected (+10)
  - Solution simpler than anticipated (+15)
  - Good documentation found (+10)
  - Existing patterns apply (+10)

- **Decrease confidence** when:
  - Hidden complexity discovered (-15)
  - Dependencies not documented (-10)
  - Integration issues found (-20)
  - Performance problems emerge (-15)

### Assumption Validation Process
1. List all assumptions from task
2. For each assumption:
   - Test if still valid
   - Document how validated
   - Update status and date
3. Calculate overall validation_status:
   - All validated → "validated"
   - All invalidated → "invalidated"
   - Mix → "partial"
   - None tested → "pending"

### Decision Rationale Examples

**Good rationale:**
"Chose PostgreSQL over MongoDB because:
1. Strong consistency requirements for financial data
2. Complex relational queries needed
3. Team expertise in SQL
Trade-off: Less flexible schema evolution"

**Poor rationale:**
"Used PostgreSQL because it's better"
