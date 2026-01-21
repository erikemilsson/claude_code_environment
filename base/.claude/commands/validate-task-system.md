# Validate Task System

Comprehensive validation of task management system to detect and fix drift from standards.

## Usage
```
/validate-task-system
```

## Purpose

Over time, small changes compound and cause the task system to drift from standards. This command catches:
- Schema violations in task JSON files
- Inconsistencies between task files and task-overview.md
- Orphaned references (subtasks pointing to missing parents, or vice versa)
- Invalid status values or transitions
- ID collisions or format violations
- Missing required fields

## Validation Checks

### 1. Task JSON Schema Validation

**Required fields:**
| Field | Type | Valid Values |
|-------|------|--------------|
| `id` | string | Top-level: `"1"`, `"2"`, etc. Subtasks: `"1_1"`, `"1_2"`, etc. |
| `title` | string | Non-empty |
| `status` | string | `"Pending"`, `"In Progress"`, `"Blocked"`, `"Broken Down"`, `"Finished"` |
| `difficulty` | number | 1-10 |

**Optional fields:**
| Field | Type | Format |
|-------|------|--------|
| `description` | string | - |
| `created_date` | string | YYYY-MM-DD |
| `dependencies` | array | Task ID strings |
| `subtasks` | array | Task ID strings |
| `parent_task` | string/null | Parent task ID |
| `files_affected` | array | File paths |
| `notes` | string | - |

### 2. Relationship Integrity

**Parent-subtask consistency:**
- If task has `parent_task`, parent must exist and list this task in `subtasks`
- If task has `subtasks`, each subtask must exist and reference this task as `parent_task`
- `"Broken Down"` status requires non-empty `subtasks` array
- Subtasks should not have `"Broken Down"` as status (only top-level)

**Dependency validity:**
- All task IDs in `dependencies` array must exist
- No circular dependencies

### 3. ID Safety (Breakdown Protection)

When breaking down tasks, IDs must not collide:
- Subtask IDs use format `{parent_id}_{n}` (e.g., `5_1`, `5_2`, `5_3`)
- Check for ID uniqueness across all task files
- Verify no orphaned task files exist (file exists but ID not in any parent/overview)

### 4. Task Overview Consistency

**Expected format:**
```markdown
# Task Overview

| ID | Title | Status | Difficulty |
|----|-------|--------|------------|
| 1 | Task title | Status | N |
...

Summary: X/Y complete
```

**Checks:**
- Every task JSON has a corresponding row in overview
- Every row in overview has a corresponding task JSON
- Status, title, and difficulty match between JSON and overview
- Summary count is accurate

### 5. Status Rules

| Status | Rules |
|--------|-------|
| `Pending` | No special requirements |
| `In Progress` | Only ONE task should have this status at a time |
| `Blocked` | Should have `notes` explaining the blocker |
| `Broken Down` | Must have non-empty `subtasks` array; should not be worked on directly |
| `Finished` | If has subtasks, all subtasks must also be `Finished` |

### 6. Difficulty Range

- Must be integer 1-10
- Tasks with difficulty >= 7 should be `"Broken Down"` or have subtasks
- Subtasks should have difficulty <= 6

## Process

### Step 1: Scan All Tasks
```
READ all .claude/tasks/task-*.json files
READ .claude/tasks/task-overview.md
```

### Step 2: Run Validation Checks
```
FOR each task file:
  CHECK required fields exist and have correct types
  CHECK status is valid value
  CHECK difficulty is 1-10
  CHECK ID format matches expected pattern
  CHECK parent_task references exist (if set)
  CHECK subtasks all exist (if set)
  CHECK dependencies all exist (if set)

FOR task overview:
  CHECK each task JSON has matching row
  CHECK each row has matching task JSON
  CHECK values match (status, title, difficulty)
  CHECK summary count is correct

GLOBAL checks:
  CHECK only one task is "In Progress"
  CHECK no ID collisions
  CHECK no circular dependencies
  CHECK "Broken Down" tasks have subtasks
  CHECK high-difficulty tasks (>=7) are broken down
```

### Step 3: Report Issues
```
## Validation Report

### ✅ Passed Checks
- [X] All task files have required fields
- [X] All status values are valid
...

### ⚠️ Warnings
- Task 5: Difficulty 8 but not broken down
- Task 3: "In Progress" for >7 days without activity
...

### ❌ Errors (Requires Fix)
- Task 2_3: References parent_task "2" but parent has no subtasks array
- Task 7: Missing required field "status"
- task-overview.md: Task 4 shows "Pending" but JSON shows "Finished"
...
```

### Step 4: Offer Auto-Fixes

For each fixable issue, ask user:

```
❌ ISSUE: Task 4 status mismatch
   - Overview shows: "Pending"
   - JSON shows: "Finished"

   FIX OPTIONS:
   [1] Update overview to match JSON (run /sync-tasks)
   [2] Update JSON to match overview
   [3] Skip - I'll fix manually

   Which option? (1/2/3): _
```

## Auto-Fixable Issues

| Issue | Auto-Fix |
|-------|----------|
| Overview doesn't match JSON | Run /sync-tasks |
| Parent missing subtask in array | Add subtask ID to parent's subtasks array |
| Subtask missing parent_task field | Add parent_task field |
| "Broken Down" with empty subtasks | Change status to "Pending" |
| All subtasks Finished but parent not | Set parent status to "Finished" |
| Missing created_date | Add current date |
| Multiple "In Progress" tasks | Ask which to keep, set others to "Pending" |

## Non-Fixable Issues (Manual Required)

| Issue | Why Manual |
|-------|------------|
| Missing required field (id, title, status, difficulty) | Need human input for values |
| Invalid JSON syntax | Need to examine file |
| Circular dependencies | Need to understand intent |
| Duplicate task IDs | Need to decide which to keep |
| Unknown status value | Need to determine correct status |

## Reference

Schema definition: `.claude/reference/task-schema.md`
Difficulty guidelines: `.claude/reference/difficulty-guide.md`
Sync command: `.claude/commands/sync-tasks.md`
Breakdown rules: `.claude/commands/breakdown.md`

## When to Run

- Start of a work session
- After extensive task operations
- When something feels "off"
- Before major milestones or handoffs
- Periodically (weekly recommended)
