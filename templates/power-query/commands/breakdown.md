# Command: Breakdown Task (Phase 1)

## Purpose
Split high-difficulty tasks (≥7) into manageable subtasks (≤6 difficulty each).

## Usage
```
@.claude/commands/breakdown.md [task_id]
```

## Prerequisites
- Task exists and has difficulty ≥7
- Task status is "Pending" (not started yet)
- Task is not already broken down

## Process

### 1. Load Task
Read `.claude/tasks/task-[id].json`:

**Validation:**
- Task difficulty is ≥7
- Task status is "Pending"
- Task does not already have subtasks

If task difficulty <7:
```
ℹ️ Task [id] has difficulty [score] (<7)

Breakdown is only recommended for tasks with difficulty ≥7.
This task can be completed directly with @.claude/commands/complete-task.md [id]
```

### 2. Load Context for Task Analysis
- `.claude/context/glossary.md`
- `.claude/reference/data-contracts.md` (if query task)
- `.claude/reference/query-manifest.md` (if query task)
- `.claude/reference/difficulty-guide-pq.md`

### 3. Analyze Task Complexity
Identify complexity dimensions:
- Query dependency depth
- Formula complexity
- Error surface
- Regulatory precision requirements
- Performance considerations

### 4. Generate Subtask Breakdown

**Breakdown Strategy:**

**For difficulty 7-8:**
Create 4-6 subtasks, each difficulty 3-5:

Example for "Implement Gold_Calculate_CFF" (difficulty 8):
1. Extract and validate input data (difficulty 4)
2. Implement core CFF formula (difficulty 5)
3. Add error handling and validation (difficulty 4)
4. Implement edge case handling (difficulty 3)
5. Add compliance flag logic (difficulty 4)

**For difficulty 9-10:**
Create 5-8 subtasks, each difficulty 3-6:

Include additional subtasks for:
- Ambiguity documentation
- Unit testing setup
- Dependency mapping
- Performance validation

### 5. Create Subtask Files

For each subtask, create new task file `.claude/tasks/task-[new_id].json`:

```json
{
  "id": "[next_sequential_id]",
  "title": "[Subtask title]",
  "description": "[Detailed description with context]",
  "difficulty": [3-6],
  "status": "Pending",
  "created_date": "[current date]",
  "dependencies": ["[parent_id_or_sibling_id]"],
  "subtasks": [],
  "parent_task": "[parent_id]",
  "notes": "Subtask of: [parent_title]. Context: [relevant files/sections]"
}
```

**Subtask Numbering:**
- Use next sequential task IDs
- Do NOT nest subtasks (flat hierarchy only)

**Dependencies:**
- First subtask may depend on parent's dependencies
- Subsequent subtasks depend on previous subtask(s)
- Establish clear execution order

### 6. Update Parent Task

Modify parent task status:

```json
{
  "status": "Broken Down",
  "breakdown_date": "[current date]",
  "subtasks": ["[sub_id_1]", "[sub_id_2]", "[sub_id_3]", ...],
  "notes": "Split into [N] subtasks. Work on subtasks, not parent."
}
```

**Important:** Parent task status is now "Broken Down" and cannot be worked on directly.

### 7. Update Task Overview

Present breakdown summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task [id] Broken Down
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Parent Task:** [Title] (difficulty [score])
**Status:** Broken Down → Work on subtasks instead

**Created Subtasks:**

1. Task [sub_id_1]: [Title] (difficulty [score])
   - Dependencies: [List]
   - Ready to start: [Yes/No]

2. Task [sub_id_2]: [Title] (difficulty [score])
   - Dependencies: Task [sub_id_1]
   - Ready to start: After subtask 1

3. Task [sub_id_3]: [Title] (difficulty [score])
   - Dependencies: Task [sub_id_2]
   - Ready to start: After subtask 2

[... continue for all subtasks]

**Execution Order:**
[sub_id_1] → [sub_id_2] → [sub_id_3] → ... → Parent auto-completes

**Next Action:**
@.claude/commands/complete-task.md [first_ready_subtask_id]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: Parent task will automatically complete when all subtasks finish.
```

### 8. Update Task Overview File

Run sync-tasks to update `.claude/tasks/task-overview.md` with new structure:

```markdown
## Pending Tasks

| ID | Title | Difficulty | Dependencies | Status |
|----|-------|------------|--------------|--------|
| 5 | Implement Gold_Calculate_CFF | 8 | 3,4 | Broken Down 🔵 (0/5 done) |
| ↳ 12 | Extract and validate CFF inputs | 4 | 3,4 | Pending |
| ↳ 13 | Implement core CFF formula | 5 | 12 | Pending |
| ↳ 14 | Add error handling | 4 | 13 | Pending |
| ↳ 15 | Implement edge case handling | 3 | 13 | Pending |
| ↳ 16 | Add compliance flag logic | 4 | 14,15 | Pending |
```

## Breakdown Guidelines

### Subtask Difficulty
- Target: 3-6 range (sweet spot for LLM execution)
- Never create subtasks with difficulty >6
- If subtask would be >6, break it down further

### Subtask Scope
Each subtask should be:
- **Atomic**: One clear deliverable
- **Testable**: Can verify completion independently
- **Sequential**: Clear order of execution
- **Context-light**: Doesn't require extensive context from other tasks

### Common Breakdown Patterns

**Pattern A: Pipeline Stages**
For data transformation tasks:
1. Input validation
2. Core transformation
3. Error handling
4. Output validation

**Pattern B: Formula Implementation**
For calculation tasks:
1. Extract/validate inputs
2. Implement formula steps 1-N
3. Add unit conversions
4. Add edge case handling
5. Add validation checks

**Pattern C: Integration Tasks**
For multi-query orchestration:
1. Dependency setup
2. Query A implementation
3. Query B implementation
4. Integration logic
5. End-to-end testing

### Dependency Management
- Keep dependency chains SHORT (max 2-3 levels)
- Prefer parallel subtasks over sequential when possible
- First subtask typically has parent's dependencies
- Later subtasks depend on earlier siblings

## Quality Checks

Before finalizing breakdown:
- [ ] All subtasks have difficulty ≤6
- [ ] All subtasks have clear descriptions
- [ ] Dependencies form valid DAG (no cycles)
- [ ] Execution order is logical
- [ ] Each subtask is independently completable
- [ ] Total effort roughly matches original task

## Error Handling

### Task Already Broken Down
```
⚠️ Task [id] is already broken down

Subtasks:
- Task [sub_id_1]: [Title] - Status: [Status]
- Task [sub_id_2]: [Title] - Status: [Status]
...

Cannot break down again. Work on subtasks or create new tasks.
```

### Task In Progress or Finished
```
❌ Cannot break down Task [id]: Status is [Status]

Breakdown is only possible for Pending tasks.
If task needs restructuring, create new tasks manually.
```

### Task Difficulty Too Low
```
ℹ️ Task [id] has difficulty [score] (<7)

Breakdown is typically only needed for high-difficulty tasks (≥7).

This task can likely be completed directly:
@.claude/commands/complete-task.md [id]

Break down anyway? [Allow but warn]
```

## Output Files
- `.claude/tasks/task-[parent_id].json` - Updated with "Broken Down" status
- `.claude/tasks/task-[sub_id_1].json` - New subtask
- `.claude/tasks/task-[sub_id_2].json` - New subtask
- ... (one file per subtask)
- `.claude/tasks/task-overview.md` - Updated hierarchy

## Auto-Completion Behavior

**Parent Task Auto-Completion:**
When the LAST subtask is marked "Finished", the parent task automatically:
1. Status changes: "Broken Down" → "Finished"
2. Completion date set to last subtask completion date
3. Hours spent = sum of all subtask hours
4. No manual intervention needed

**Do NOT:**
- Manually set parent to "Finished"
- Work on parent directly
- Try to complete parent before all subtasks done

## Notes

- Breakdown creates ONE LEVEL of hierarchy only (no nested subtasks)
- Parent tasks track progress: "Broken Down (2/5 done)" 🔵
- Maximum subtasks per parent: ~8 (keep manageable)
- Sequential numbering: No gaps in task IDs
- Breaking down is permanent (cannot un-break)
- See `.claude/reference/breakdown-workflow.md` for detailed workflow
- Subtasks should reference parent in notes
