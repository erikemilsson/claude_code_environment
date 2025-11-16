# Hierarchical Task Breakdown Workflow

## Purpose
Explains the hierarchical task management system for handling complex tasks.

---

## Core Concept

**Problem:** Complex tasks (difficulty ≥7) are too risky for direct LLM execution.

**Solution:** Break them into subtasks (difficulty ≤6) before starting work.

**Result:** Parent task status becomes "Broken Down", work happens on subtasks, parent auto-completes.

---

## Task Hierarchy

### One-Level Hierarchy Only

```
Task 5: Implement Gold_Calculate_CFF (difficulty 8) [Broken Down]
├─ Task 12: Extract inputs (difficulty 4) [Pending]
├─ Task 13: Core formula (difficulty 5) [Pending]
├─ Task 14: Error handling (difficulty 4) [Pending]
└─ Task 15: Validation (difficulty 3) [Pending]
```

**No nesting allowed:**
```
Task 5 [Broken Down]
├─ Task 12 [Broken Down]  ← ❌ NOT ALLOWED
│  ├─ Task 20
│  └─ Task 21
```

If subtask needs breakdown, create new top-level task instead.

---

## Workflow Steps

### 1. Identify High-Difficulty Task

When planning or reviewing tasks:
- Check task difficulty
- If difficulty ≥7, flag for breakdown
- task-overview.md marks these with 🔴

```markdown
| ID | Title | Difficulty | Status |
|----|-------|------------|--------|
| 5 | Implement Gold_Calculate_CFF | 8 | Pending 🔴
```

### 2. Run Breakdown Command

```
@.claude/commands/breakdown.md 5
```

Claude analyzes the task and creates 4-6 subtasks (difficulty 3-5 each).

### 3. Parent Task Updated

```json
{
  "id": "5",
  "status": "Broken Down",
  "breakdown_date": "2024-01-15",
  "subtasks": ["12", "13", "14", "15"]
}
```

**Status "Broken Down" means:**
- Cannot work on this task directly
- Work on subtasks instead
- Will auto-complete when all subtasks done

### 4. Subtasks Created

```json
{
  "id": "12",
  "title": "Extract and validate CFF inputs",
  "difficulty": 4,
  "status": "Pending",
  "parent_task": "5",
  "dependencies": ["3", "4"]
}
```

Each subtask:
- References parent task
- Has manageable difficulty
- Has clear dependencies
- Can be completed independently

### 5. Work on Subtasks

Execute subtasks in order:

```
@.claude/commands/complete-task.md 12
```

After completion:
- Task 12: Status → "Finished"
- Parent Task 5: Still "Broken Down (1/4 done)" 🔵

### 6. Parent Auto-Completion

When the LAST subtask finishes:
- Parent status: "Broken Down" → "Finished"
- Parent completion_date: Set to last subtask completion
- Parent hours_spent: Sum of all subtask hours
- **No manual action needed**

---

## Status Indicators

### In task-overview.md

**Pending high-difficulty task:**
```
| 5 | Implement Gold_Calculate_CFF | 8 | Pending 🔴
```
🔴 = Needs breakdown before starting

**Parent with subtasks in progress:**
```
| 5 | Implement Gold_Calculate_CFF | 8 | Broken Down 🔵 (2/4 done)
| ↳ 12 | Extract inputs | 4 | Finished ✅
| ↳ 13 | Core formula | 5 | Finished ✅
| ↳ 14 | Error handling | 4 | In Progress ⏳
| ↳ 15 | Validation | 3 | Pending
```
🔵 = Broken down parent (shows progress)
↳ = Subtask (indented under parent)

---

## Rules and Constraints

### Must Follow

1. **Only break down difficulty ≥7** (or 6 if very uncertain)
2. **Subtasks must be ≤6 difficulty** (sweet spot: 3-5)
3. **One level only** - no nested breakdowns
4. **Cannot work on "Broken Down" parents** - work on subtasks
5. **Parents auto-complete** - don't manually set to "Finished"

### Best Practices

1. **Break down early** - before starting work, not mid-task
2. **Clear subtask scope** - each should have one deliverable
3. **Sequential dependencies** - establish clear execution order
4. **Shallow dependency chains** - max 2-3 levels deep
5. **Document context** - each subtask references relevant files

---

## Breakdown Strategies

### Strategy A: Pipeline Stages
For data transformation tasks:
1. Input validation (diff 3)
2. Core transformation (diff 5)
3. Error handling (diff 4)
4. Output validation (diff 3)

### Strategy B: Formula Steps
For calculation tasks:
1. Extract/validate inputs (diff 4)
2. Implement formula part 1 (diff 5)
3. Implement formula part 2 (diff 5)
4. Add edge case handling (diff 3)
5. Validation (diff 3)

### Strategy C: Component-Based
For integration tasks:
1. Component A setup (diff 4)
2. Component B setup (diff 4)
3. Integration logic (diff 5)
4. Testing (diff 4)

Choose strategy based on task nature.

---

## Common Scenarios

### Scenario 1: All Subtasks Done, Parent Still "Broken Down"

**This is a bug. Run:**
```
@.claude/commands/update-tasks.md
```

This will detect the issue and auto-complete the parent.

### Scenario 2: Want to Work on Parent Task Directly

**Cannot do this. Must work on subtasks.**

If parent is "Broken Down", you must:
1. Work on available subtasks
2. Complete all subtasks
3. Parent auto-completes

### Scenario 3: Subtask Turns Out to be Complex (>6)

**Do NOT break down subtasks.**

Instead:
1. Complete the subtask as best you can
2. Create a NEW top-level task for the complex part
3. Mark original subtask done
4. Add new task to project

### Scenario 4: Want to Add More Subtasks to Parent

**After breakdown, cannot add more subtasks.**

If you discover more work:
1. Create new top-level tasks
2. Link them via dependencies
3. Don't try to modify broken-down parent

---

## Benefits of This System

### For LLMs
- Manageable task complexity
- Clear scope per task
- Reduced error rate
- Better context understanding

### For Users
- Predictable progress tracking
- Clear completion criteria
- Easy to resume work
- Better estimation

### For Projects
- Reduced risk
- Better decomposition
- Clear dependencies
- Audit trail of decisions

---

## Anti-Patterns to Avoid

### ❌ Don't: Break down easy tasks
```
Task 3 (difficulty 4) → Don't break down, just complete it
```

### ❌ Don't: Create subtasks >6 difficulty
```
Task 5 broken down into:
├─ Subtask 12 (difficulty 7) ← Too hard! Break down further
```

### ❌ Don't: Nest subtasks
```
Task 5
├─ Task 12
│  ├─ Task 20 ← Not allowed!
```

### ❌ Don't: Manually complete parent
```
Task 5: "Broken Down" → "Finished" ← Let it auto-complete!
```

### ❌ Don't: Work on "Broken Down" task
```
@.claude/commands/complete-task.md 5 ← Error! Work on subtasks
```

---

## Task Lifecycle

```
Created → Pending → [Breakdown] → Broken Down → [Subtasks finish] → Finished
                ↓
            In Progress → Finished
```

**Key Transitions:**
- Pending → Broken Down: Via `breakdown.md` command
- Pending → In Progress: Via `complete-task.md` command
- Broken Down → Finished: Automatic (when last subtask finishes)
- In Progress → Finished: Via `complete-task.md` completion

---

## Troubleshooting

### Parent shows "(3/4 done)" but I can't find the 4th subtask

Check `task-overview.md` for the full subtask list under the parent.
One subtask might be "Blocked" or have dependencies.

### Subtask is finished but parent still shows same progress

Run:
```
@.claude/commands/sync-tasks.md
```

This regenerates task-overview.md with current status.

### Want to "un-break-down" a task

**Not possible.** Breakdown is permanent.

If you made a mistake:
1. Complete all subtasks quickly
2. Parent auto-completes
3. Create new task with correct scope

---

## Summary

**The Golden Rule:** Tasks ≥7 difficulty are broken down into subtasks ≤6 difficulty.

**The Automation:** Parents auto-complete when all subtasks finish.

**The Benefit:** Reduced complexity → reduced errors → faster completion.

---

**See Also:**
- `.claude/commands/breakdown.md` - Breakdown command
- `.claude/commands/complete-task.md` - Task execution
- `.claude/reference/difficulty-guide-pq.md` - Difficulty scoring
