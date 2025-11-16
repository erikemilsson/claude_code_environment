# Update Progress Command

## Purpose
Log project progress, document changes, track status, and update project documentation with photos and notes.

## Context Required
- Current task status from `.claude/tasks/`
- Budget tracker from `.claude/context/budget-tracker.md`
- Timeline/schedule information
- Photos of progress (if available)

## Process

1. **Gather Information**
   - Review which tasks were completed
   - Identify tasks currently in progress
   - Note any issues or blockers encountered
   - Collect photos taken during work
   - Check if any costs were incurred
   - Assess timeline impact

2. **Document Completion**
   - Update task status (mark completed tasks as "Finished")
   - Add completion notes to task files
   - Include any lessons learned or observations

3. **Log Issues (if any)**
   - Create issue entry in `.claude/context/progress-log.md`
   - Document problem, impact, and resolution
   - Add photos of issues if relevant
   - Create new tasks if needed to address issues

4. **Update Budget (if applicable)**
   - If costs were incurred, update budget tracker
   - Record actual costs vs estimates
   - Calculate and note variances
   - Update remaining budget

5. **Update Timeline (if needed)**
   - If delays or acceleration occurred, adjust task dates
   - Recalculate completion estimate
   - Note buffer time used
   - Update milestone dates if affected

6. **Organize Photos**
   - Save photos to appropriate folder (before/progress/issues/after)
   - Use naming convention: `YYYY-MM-DD-description.jpg`
   - Reference photos in progress log

7. **Create Progress Entry**
   - Add update to `.claude/context/progress-log.md`
   - Include date, tasks completed, issues, budget/timeline impact
   - Reference photos
   - Note next steps

8. **Sync Tasks**
   - Run `/sync-tasks` to update task-overview.md
   - Ensure all changes are reflected in overview

9. **Communicate (if needed)**
   - Share update with stakeholders if appropriate
   - Notify vendors if coordination needed
   - Update any external trackers

## Output Location
- `.claude/context/progress-log.md` - Append new progress entry
- `.claude/tasks/task-*.json` - Update relevant task files
- `.claude/tasks/task-overview.md` - Auto-generated via sync-tasks
- `.claude/context/budget-tracker.md` - Update if costs incurred
- `photos/progress/` - Save photos with date-stamped names

## Example Usage

```
/update-progress

User provides:
> Completed demolition of old bathroom. Found water damage behind tub
> that needs repair (approx 2 sq ft). Took photos. Contractor quotes
> $800 for repair. Will delay tile work by 2 days.

Claude updates:
1. Marks demo tasks as complete
2. Logs issue (water damage) with impact
3. Creates new task for water damage repair
4. Updates budget (+$800 from contingency)
5. Adjusts timeline (+2 days delay)
6. Adds progress entry with photo references
7. Syncs task overview
```

## Template for Progress Entry

```markdown
## Progress Update - [Date]

### Tasks Completed
- [Task ID/Name] - [Brief description]

### Tasks In Progress
- [Task ID/Name] - [Status, % if known]

### Issues/Blockers
- [Description]
  - Impact: [Timeline/Budget/Quality]
  - Resolution: [How addressed]

### Budget Impact
- [Description]: +/- $[Amount]
- Total spent: $[Amount]
- Remaining: $[Amount]

### Timeline Impact
- [Description]: +/- [Days]
- New completion estimate: [Date]

### Photos
- [Photos folder path or specific files]

### Next Steps
- [What's happening next]
- [Any decisions needed]
```
