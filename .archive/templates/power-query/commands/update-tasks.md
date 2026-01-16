# Command: Update Tasks

## Purpose
Validate task structure, ensure tasks are still relevant, and flag any inconsistencies between task JSON files and task-overview.md. This is the main command for checking system health.

## Context Required
- `.claude/tasks/*.json` (all task files)
- `.claude/tasks/task-overview.md`
- `.claude/context/validation-rules.md`
- `.claude/reference/difficulty-guide.md`

## Process

1. **Read all task files** using @.claude/tasks/*.json and @.claude/tasks/task-overview.md

2. **Validate structure and rules** for each task:

   **A. Structural Validation**
   - All task files are valid JSON
   - All required fields present (id, title, description, difficulty, status)
   - Task IDs are sequential (no gaps) and match filenames
   - Status values are legal ("Pending", "In Progress", "Blocked", "Broken Down", "Finished")
   - Difficulty scoring is appropriate per difficulty-guide.md (1-10)
   - Dates are in YYYY-MM-DD format

   **B. Parent-Child Relationship Validation**
   - "Broken Down" tasks have at least one subtask in `subtasks` array
   - Parents list valid subtask IDs
   - Subtasks have valid `parent_task` reference
   - No orphaned subtasks (parent doesn't list them)
   - No nested subtasks (subtasks cannot have subtasks)
   - Subtasks have difficulty ≤6

   **C. Dependency Validation**
   - Dependencies reference existing task IDs
   - No circular dependencies
   - No self-dependencies
   - Dependencies form valid DAG (acyclic)

3. **Check consistency** between JSON files and task-overview.md:
   - Are all tasks from JSON files present in overview?
   - Do statuses match between JSON and overview?
   - Are difficulty scores consistent?
   - Does overview correctly show subtask progress for "Broken Down" tasks?

4. **Assess relevance:**
   - Are "In Progress" tasks actually being worked on (have start_date)?
   - Are "Blocked" tasks listing specific blockers?
   - Are finished tasks marked with completion dates?
   - Do "Broken Down" tasks have all their subtasks created?
   - Flag stale tasks:
     - Created >30 days ago and still "Pending"
     - Status "In Progress" >7 days with no updates
     - Description mentions deprecated approaches

5. **Validate parent-child relationships:**
   - All subtasks listed in parent's `subtasks` array exist
   - All subtasks with `parent_task` reference a valid parent
   - Parent tasks with difficulty ≥7 and status "Pending" should be flagged for breakdown
   - **Auto-fix common issues:**
     - **Issue 1**: Parent has subtasks but status is "Pending" → Set status to "Broken Down"
     - **Issue 2**: All subtasks "Finished" but parent still "Broken Down" → Auto-complete parent, set completion_date
     - **Issue 3**: Task status "Finished" but no completion_date → Use current date
     - **Issue 4**: Orphaned subtasks → Add subtask to parent's subtasks array
     - **Issue 5**: Invalid dependencies → Remove invalid dependency
   - **Flag for manual review:**
     - Circular dependencies (cannot auto-fix)
     - High-difficulty tasks (≥7) in "In Progress" without breakdown
     - Potentially outdated tasks

6. **Update if needed:**
   - Save all auto-fixed tasks back to their JSON files
   - If JSON files are correct but overview is outdated: automatically run sync-tasks
   - If JSON files need manual updates: flag them and suggest corrections
   - Identify optimization opportunities:
     - Tasks with no dependencies that could run in parallel
     - Critical path tasks to prioritize
     - Long-blocked tasks

7. **Report findings:**
   - Generate detailed validation report with:
     - Auto-fixed issues (with counts)
     - Manual review required (with specific recommendations)
     - Stale tasks identified
     - Optimization suggestions
     - Next actions to take
   - List any validation errors or inconsistencies found
   - Confirm if system is in sync

## Output Location

**Console Report:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Validation Status:** [PASS / ISSUES FOUND]

## Auto-Fixed Issues: [Count]

✅ Fixed parent status for Task 5 (Pending → Broken Down)
✅ Auto-completed parent Task 8 (all subtasks done)
✅ Added completion_date to Task 12
✅ Removed invalid dependency: Task 7 → Task 99 (doesn't exist)

## Manual Review Required: [Count]

⚠️ Task 15: Circular dependency detected
⚠️ Task 20: High difficulty (9) still pending - needs breakdown

## Stale Tasks: [Count]

⏱️ Task 18: In progress for 10 days with no activity
⏱️ Task 22: Pending for 45 days, possibly outdated

## Optimization Suggestions: [Count]

💡 Tasks 7,8 could run in parallel
💡 Critical path identified: 1→3→5→6
💡 Task 10 should be broken down (difficulty 8)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Next Actions

1. Review manual issues and fix as needed
2. Address stale tasks (complete or archive)
3. Consider optimization suggestions
4. Run: @.claude/commands/sync-tasks.md to update overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Modified Files:**
- `.claude/tasks/task-*.json` (any auto-fixed tasks)
- `.claude/tasks/task-overview.md` (via automatic sync-tasks run)

**Created Files:**
- `.claude/tasks/_validation-report.md` (detailed validation log)

## When to Run

**Run periodically:**
- Before starting major work session
- After manually editing task files
- Weekly for long projects
- When task-overview.md seems incorrect

**Run after:**
- Manually creating tasks
- Manually editing task dependencies
- Git pull (if collaborating)

## Validation Rules Reference

### Parent Task Rules
1. Status must be "Broken Down" if has subtasks
2. Cannot have status "In Progress" or "Finished" if subtasks incomplete
3. Auto-completes when all subtasks "Finished"
4. Hours = sum of subtask hours

### Subtask Rules
1. Must reference valid parent
2. Parent must list subtask in its subtasks array
3. Difficulty must be ≤6
4. Cannot have their own subtasks (flat hierarchy)

### Dependency Rules
1. Must form valid DAG (no cycles)
2. Cannot depend on self
3. Cannot depend on non-existent tasks
4. Cannot depend on "Broken Down" parents (depend on subtasks instead)

### Status Transitions
**Valid transitions:**
- Pending → In Progress → Finished
- Pending → Broken Down → Finished (auto)
- Pending → Blocked → In Progress → Finished
- Any → Cancelled (manual)

**Invalid transitions:**
- Finished → Pending (cannot un-finish)
- Broken Down → In Progress (work on subtasks instead)

## Notes

- **Phase 1 Template**: Enhanced version with comprehensive auto-fix and optimization features
- **Safe to run frequently**: Only fixes clear issues, non-destructive
- **Always backs up**: Before modifying task files
- **Manual review required**: For complex issues like circular dependencies
- **Idempotent**: Safe to run multiple times
- **Automatic sync**: Runs sync-tasks.md automatically after fixes
- Use this before manual `sync-tasks.md` runs for best results
