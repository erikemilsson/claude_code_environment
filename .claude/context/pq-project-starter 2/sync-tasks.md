# Command: Sync Tasks (Phase 1)

## Purpose
Update `.claude/tasks/task-overview.md` to reflect current state of all task files.

## Usage
```
@.claude/commands/sync-tasks.md
```

## Prerequisites
- Tasks exist in `.claude/tasks/` directory
- Task files are valid JSON

## Process

### 1. Scan Task Directory
Read all `.claude/tasks/task-*.json` files (excluding `_phase-0-status.md`).

### 2. Parse Task Data
For each task file, extract:
- ID
- Title
- Description
- Difficulty
- Status
- Dependencies
- Subtasks (if parent)
- Parent task (if subtask)
- Created date
- Completion date
- Hours spent

### 3. Build Task Hierarchy
Identify parent-child relationships:
- Tasks with `parent_task: null` are top-level
- Tasks with `parent_task: [id]` are subtasks
- Tasks with `subtasks: [...]` are parents

### 4. Calculate Statistics

**Overall:**
- Total tasks
- Pending tasks
- In Progress tasks
- Finished tasks
- Broken Down tasks (parents)

**By Difficulty:**
- Tasks by difficulty level
- High-difficulty tasks needing breakdown (≥7)

**Progress:**
- Completion percentage
- Estimated hours remaining

### 5. Generate Task Overview

Create/update `.claude/tasks/task-overview.md`:

```markdown
# Task Overview

**Project:** [Project Name from CLAUDE.md]
**Last Updated:** [Current Date/Time]

---

## Summary

**Total Tasks:** [Count]
- ✅ Finished: [Count] ([Percentage]%)
- 🔵 Broken Down: [Count] (parent tasks)
- ⏳ In Progress: [Count]
- ⏸️ Pending: [Count]

**Progress:** [Finished]/[Total] tasks complete

**Estimated Hours Remaining:** [Sum of pending tasks based on difficulty]

---

## Pending Tasks

| ID | Title | Difficulty | Dependencies | Status | Notes |
|----|-------|------------|--------------|--------|-------|
| 1 | Implement Bronze_Source_EmissionFactors | 3 | None | Pending | |
| 2 | Implement Bronze_Source_InputTables | 3 | None | Pending | |
| 3 | Implement Silver_Clean_EmissionFactors | 5 | 1 | Pending | |
| 5 | Implement Gold_Calculate_CFF | 8 | 3,4 | Broken Down 🔵 (2/5 done) | |
| ↳ 12 | Extract and validate CFF inputs | 4 | 3,4 | Finished ✅ | |
| ↳ 13 | Implement core CFF formula | 5 | 12 | Finished ✅ | |
| ↳ 14 | Add error handling | 4 | 13 | In Progress ⏳ | |
| ↳ 15 | Implement edge cases | 3 | 13 | Pending | |
| ↳ 16 | Add compliance flags | 4 | 14,15 | Pending | |
| 6 | Implement Gold_Compliance_Report | 6 | 5 | Pending | Blocked |

---

## In Progress

| ID | Title | Started | Assigned To | Notes |
|----|-------|---------|-------------|-------|
| 14 | Add error handling | 2024-01-20 | Claude | Working on validation logic |

---

## Finished Tasks

| ID | Title | Difficulty | Completed | Hours |
|----|-------|------------|-----------|-------|
| 12 | Extract and validate CFF inputs | 4 | 2024-01-18 | 2.5 |
| 13 | Implement core CFF formula | 5 | 2024-01-19 | 3.0 |

---

## High-Difficulty Tasks (Need Breakdown)

| ID | Title | Difficulty |
|----|-------|------------|
| 8 | Implement full compliance pipeline | 9 | 🔴

**Note:** Tasks marked 🔴 should be broken down using `@.claude/commands/breakdown.md [id]` before starting.

---

## Blocked Tasks

| ID | Title | Blocked By | Reason |
|----|-------|------------|--------|
| 6 | Implement Gold_Compliance_Report | Task 5 | Waiting for parent task completion |

---

## Task Dependencies

```
1 (Bronze_Source_EmissionFactors) →
  3 (Silver_Clean_EmissionFactors) →
    5 (Gold_Calculate_CFF) [Broken Down] →
      12,13,14,15,16 (subtasks) →
    6 (Gold_Compliance_Report)

2 (Bronze_Source_InputTables) →
  4 (Silver_Validate_Inputs) →
    5 (Gold_Calculate_CFF)
```

---

## Next Actions

**Recommended Next Task:** Task 14 (already in progress)

**When Task 14 finishes:**
- Task 15 and 16 will become available
- After all subtasks done, Task 5 auto-completes
- Then Task 6 unblocks

**Available to Start Now:**
- Task 1: Implement Bronze_Source_EmissionFactors (no dependencies)
- Task 2: Implement Bronze_Source_InputTables (no dependencies)

---

**Commands:**
- Work on task: `@.claude/commands/complete-task.md [id]`
- Break down task: `@.claude/commands/breakdown.md [id]`
- Update this file: `@.claude/commands/sync-tasks.md`
```

### 6. Identify Issues

**Parent-Child Inconsistencies:**
- Parent lists subtask that doesn't exist
- Subtask references non-existent parent
- Parent status not "Broken Down" but has subtasks

**Dependency Issues:**
- Task depends on non-existent task
- Circular dependencies
- Task depends on "Pending" task but is marked "In Progress"

**Status Issues:**
- Parent is "Finished" but subtasks still "Pending"
- Task is "In Progress" with no start date
- Task is "Finished" with no completion date

Report any found issues:
```
⚠️ Task Integrity Issues Found:

1. Task 8: Lists subtask 25 which doesn't exist
2. Task 12: Parent task 5 is not marked "Broken Down"
3. Task 15: Depends on Task 14 which is still "Pending"

Run @.claude/commands/update-tasks.md to fix automatically.
```

### 7. Summary Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task Overview Synchronized
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Updated: .claude/tasks/task-overview.md

**Statistics:**
- Total Tasks: [Count]
- Finished: [Count] ([Percentage]%)
- In Progress: [Count]
- Pending: [Count]
- Broken Down (Parents): [Count]

**Progress:** [Progress bar visual]
███████████░░░░░░░░░ 55% complete

**Next Actions:**
- [Next recommended task or action]

**Issues:** [Count found, or "None"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Output Files
- `.claude/tasks/task-overview.md` - Regenerated from task files

## When to Run

**Automatically run by:**
- `complete-task.md` (after task completion)
- `breakdown.md` (after creating subtasks)

**Manually run when:**
- You want to see current project status
- After manually editing task files
- Before starting work session (sanity check)
- When task overview looks outdated

## Notes

- **Read-only of task files** - only updates overview.md
- **Safe to run frequently** - just regenerates overview
- **No validation** - use `update-tasks.md` for validation
- **Fast operation** - suitable for frequent use
- Overview is generated, don't manually edit it
- For fixing issues, use `update-tasks.md` instead
