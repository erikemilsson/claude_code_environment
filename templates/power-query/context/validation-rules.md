# Task Validation Rules

## Purpose
Defines validation rules for task structure and content used by `update-tasks.md` command.

---

## Required Task Fields

Every task JSON file must have:

```json
{
  "id": "string (sequential number)",
  "title": "string (descriptive)",
  "description": "string (detailed, non-empty)",
  "difficulty": "number (1-10)",
  "status": "string (valid status)",
  "created_date": "string (ISO date)",
  "dependencies": "array (of task IDs or empty)",
  "subtasks": "array (of task IDs or empty)",
  "parent_task": "string (task ID or null)",
  "notes": "string (can be empty)"
}
```

---

## Valid Status Values

- `"Pending"` - Not started, ready to work on
- `"In Progress"` - Currently being worked on
- `"Finished"` - Completed
- `"Broken Down"` - Split into subtasks (parent tasks only)
- `"Cancelled"` - No longer needed (rare)
- `"Blocked"` - Cannot start due to external blocker (rare)

---

## Status Rules

### Pending Tasks
- Can transition to: In Progress, Broken Down, Cancelled
- Must have: created_date
- Cannot have: start_date, completion_date

### In Progress Tasks
- Must have: start_date
- Cannot have: completion_date
- Should not stay in progress >7 days without update

### Finished Tasks
- Must have: completion_date, hours_spent
- Cannot transition to other states

### Broken Down Tasks
- Must have: non-empty subtasks array
- Must have: breakdown_date
- Cannot have: start_date
- Cannot be worked on directly (work on subtasks)

---

## Parent-Child Rules

### Parent Tasks
- If has subtasks: status MUST be "Broken Down"
- Cannot be "In Progress" or "Finished" manually
- Auto-completes when all subtasks are "Finished"
- hours_spent = sum of subtask hours_spent

### Subtasks
- Must reference parent via parent_task field
- Parent must list subtask in its subtasks array
- difficulty MUST be ≤6
- Cannot have their own subtasks (flat hierarchy only)

---

## Dependency Rules

- All dependency IDs must reference existing tasks
- Cannot depend on self
- Cannot create circular dependencies
- Cannot depend on "Broken Down" parents (depend on subtasks instead)
- Dependencies must form valid DAG (Directed Acyclic Graph)

---

## Difficulty Rules

- Must be integer 1-10
- Tasks with difficulty ≥7 should be broken down before starting
- Subtasks must have difficulty ≤6
- If difficulty doesn't match task complexity, flag for review

---

## Date Rules

- All dates in ISO format: YYYY-MM-DD
- created_date: Required for all tasks
- start_date: Required if status is "In Progress" or "Finished"
- completion_date: Required if status is "Finished"
- breakdown_date: Required if status is "Broken Down"

---

## Consistency Rules

### Task IDs
- Must be sequential: 1, 2, 3, 4... (no gaps)
- Must match filename: task-5.json has id: "5"
- String format: "1", "2", not 1, 2

### Dependencies Before Task
- A task cannot depend on a task with higher ID
- Exception: Subtasks can depend on later sibling subtasks

### Blocked Tasks
- If task status is "Blocked", must have blocker documented in notes
- Blocker should reference specific task ID or external factor

---

## Auto-Fix Rules

**update-tasks.md** can auto-fix these issues:

1. Parent has subtasks but status != "Broken Down"
   → Fix: Set status to "Broken Down"

2. All subtasks finished but parent still "Broken Down"
   → Fix: Set parent to "Finished", set completion_date

3. Subtask references parent, but parent doesn't list it
   → Fix: Add subtask to parent's subtasks array

4. Task finished but no completion_date
   → Fix: Set completion_date to current date

5. Invalid dependency (references non-existent task)
   → Fix: Remove invalid dependency

---

## Manual Review Required

**update-tasks.md** will FLAG but NOT auto-fix:

1. Circular dependencies
2. Task difficulty mismatch (e.g., diff 9 but status "In Progress")
3. Stale tasks (pending >30 days or in progress >7 days)
4. Subtask with difficulty >6
5. Contradictory status (e.g., finished task with pending dependencies)

---

## Task Quality Checks

### Title Quality
- Should be action-oriented: "Implement X", "Create Y", "Fix Z"
- Should be specific: Not "Work on queries" but "Implement Gold_Calculate_CFF query"
- Should be ≤100 characters

### Description Quality
- Should include enough context to start work
- Should reference relevant context files
- Should specify deliverables
- Should not be empty or generic

### Notes Quality
- Should document decisions, blockers, or important context
- Should reference related tasks if applicable
- Should include assumptions if any

---

## Validation Frequency

Run `update-tasks.md` validation:
- Before starting major work session
- After manually editing tasks
- Weekly for long projects
- Before git commits
- After git pull (if collaborating)

---

**See Also:**
- `.claude/commands/update-tasks.md` - Validation command
- `.claude/commands/complete-task.md` - Task execution
- `.claude/commands/breakdown.md` - Task breakdown
