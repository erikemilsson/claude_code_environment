# Task Breakdown Workflow Guide

## When to Break Down Tasks

**Mandatory breakdown:**
- Any task with difficulty ≥7

**Optional breakdown:**
- Tasks estimated >8 hours
- Tasks with unclear requirements (break down for clarity)
- Tasks discovered to be complex during "In Progress"

## The "Broken Down" Status

### What It Means
When a task is marked "Broken Down", it becomes a **container** or **epic**:
- It is NOT a unit of work itself
- It CANNOT be worked on directly
- It tracks progress through its subtasks
- It auto-completes when all subtasks finish

### What You Can Do
- ✅ View its progress in task-overview.md
- ✅ Add notes for context
- ✅ Review its subtasks
- ❌ Cannot change status manually to "Finished"
- ❌ Cannot use complete-task.md on it
- ❌ Cannot add time tracking (track time on subtasks instead)

### Visual Indicators
In task-overview.md, Broken Down tasks show:
- 🔵 icon
- Progress: "Broken Down (X/Y done)"
- Subtasks indented with ↳ symbol
- Links to all subtasks

## Subtask Rules

### Subtask Creation
- Each subtask gets sequential ID (next available number)
- Each subtask has `parent_task` field pointing to original
- Subtasks inherit context but have own difficulty scores (≤6)
- Subtasks can have dependencies on other subtasks
- Subtasks start with status "Pending"

### Subtask Completion
When you finish the LAST subtask:
1. You mark subtask as "Finished" (normal process via complete-task.md)
2. System detects parent is "Broken Down"
3. System checks all sibling subtasks
4. If all siblings "Finished" → parent auto-completes to "Finished"
5. You receive notification: "🎉 Parent Task #{id} automatically completed!"

## Example Workflow

### Initial State
Task 7: "Implement Azure SQL integration" (difficulty: 8, status: Pending)

### Step 1: Break Down
**User:** @.claude/commands/breakdown.md 7

**Claude analyzes the task and proposes:**

I'll break down Task 7 into 4 subtasks:

1. Create connection manager (difficulty: 4)
   - Handle connection pooling
   - Manage credentials securely

2. Build bulk insert module (difficulty: 6)
   - Implement batch processing
   - Handle data type mapping

3. Add retry logic (difficulty: 4)
   - Exponential backoff
   - Error classification

4. Write integration tests (difficulty: 3)
   - Test connection handling
   - Test bulk operations

Proceed with breakdown? (yes/no)

### After Breakdown
Task 7: "Implement Azure SQL integration"
  - Status: Broken Down 🔵
  - Difficulty: 8 (original preserved)
  - Subtasks: 15, 16, 17, 18
  - Progress shown in overview: "Broken Down (0/4 done)"

Task 15: "Create connection manager" (difficulty: 4, status: Pending, parent: 7)
Task 16: "Build bulk insert module" (difficulty: 6, status: Pending, parent: 7)
Task 17: "Add retry logic" (difficulty: 4, status: Pending, parent: 7, depends on: 15, 16)
Task 18: "Write integration tests" (difficulty: 3, status: Pending, parent: 7, depends on: 15, 16, 17)

### Step 2: Work on Subtasks
User: @.claude/commands/complete-task.md 15  # Start first subtask

**Claude:**
Progress updates:
Task 7: "Broken Down (1/4 done)" after completing Task 15
Task 7: "Broken Down (2/4 done)" after completing Task 16
Task 7: "Broken Down (3/4 done)" after completing Task 17

### Step 3: Complete Last Subtask
@.claude/commands/complete-task.md 18  # Finish last subtask

# Output includes:
✅ Task #18 "Write integration tests" completed!
- Estimated: 2 hours
- Actual: 2.5 hours

🎉 Completing this subtask also completed parent Task #7: "Implement Azure SQL integration"!
All 4 subtasks (15-18) are now finished.

Suggested next task: Task #19 "Configure ETL scheduling" (difficulty: 5)

### Final State
Task 7: Status changed from "Broken Down" to "Finished" (automatic)
  - All subtasks (15-18): Status = "Finished"
  - Notes updated: "Auto-completed: all subtasks finished on 2024-01-16"
  - Total actual hours: Sum of all subtask hours (11 hours)

## Benefits of This Approach

1. **No Ambiguity**: Clear distinction between work items (subtasks) and containers (broken down parents)
2. **Accurate Progress**: Easy to see "3 out of 4 subtasks done = 75%" in task-overview.md
3. **Prevents Errors**: Cannot accidentally complete parent with unfinished work
4. **Self-Managing**: Automatic completion reduces manual overhead and prevents inconsistencies
5. **Better Planning**: Difficulty scores reflect actual work complexity per subtask
6. **Lower Risk**: Each subtask has difficulty ≤6, reducing LLM error probability
7. **Clear Dependencies**: Subtask dependencies make work sequence explicit

## Common Questions

**Q: Can I break down a task that's already "In Progress"?**
A: Yes! If you discover complexity mid-work, you can break it down. The parent will transition to "Broken Down" and you'll work on the subtasks instead.

**Q: What if I want to undo a breakdown?**
A: You cannot directly undo. However, you can mark all subtasks as "Finished" individually (if the work is done), or delete the subtasks and reset the parent to "Pending" (if you made a mistake).

**Q: Can subtasks be broken down further?**
A: No. The system only supports one level of hierarchy (parent → subtasks). If a subtask seems too complex, increase its difficulty score but keep it ≤6. If it's genuinely >6, consider redesigning the parent's breakdown.

**Q: How do I track time for a "Broken Down" task?**
A: Don't track time on the parent. Track actual_hours on each subtask. The parent's total effort is the sum of all subtask hours.

**Q: What happens if I try to use complete-task.md on a "Broken Down" task?**
A: The command will halt with an error: "❌ Task {id} has been broken down into subtasks {list}. Please work on the individual subtasks instead."
