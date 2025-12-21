<!-- Type: Direct Execution -->

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
   - All required fields present and valid
   - Status values are legal ("Pending", "In Progress", "Blocked", "Broken Down", "Finished")
   - Difficulty scoring is appropriate per difficulty-guide.md
   - Dates are in YYYY-MM-DD format
   - Dependencies reference existing task IDs and there are no circular dependencies
   - "Broken Down" tasks have at least one subtask in `subtasks` array
   - Subtasks have valid `parent_task` reference
3. **Check consistency** between JSON files and task-overview.md:
   - Are all tasks from JSON files present in overview?
   - Do statuses match between JSON and overview?
   - Are difficulty scores consistent?
   - Does overview correctly show subtask progress for "Broken Down" tasks?
4. **Assess relevance:**
   - Are "In Progress" tasks actually being worked on?
   - Are "Blocked" tasks listing specific blockers?
   - Are finished tasks marked with completion dates?
   - Do "Broken Down" tasks have all their subtasks created?
5. **Validate parent-child relationships:**
   - All subtasks listed in parent's `subtasks` array exist
   - All subtasks with `parent_task` reference a valid parent
   - Parent tasks with difficulty ≥7 and status "Pending" should be flagged for breakdown
6. **Update if needed:**
   - If JSON files are correct but overview is outdated: run sync-tasks
   - If JSON files need updates: update them first, then run sync-tasks
   - Flag any tasks that may be outdated or irrelevant
7. **Report findings:**
   - List any validation errors or inconsistencies found
   - Suggest corrections
   - Confirm if system is in sync

## Output Location
- Console report of findings
- Updated task JSON files (if corrections needed)
- Updated `.claude/tasks/task-overview.md` (via sync-tasks if needed)
