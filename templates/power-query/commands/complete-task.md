# Command: Complete Task (Phase 1)

## Purpose
Execute a specific task with full context loading and automatic status tracking.

## Usage
```
@.claude/commands/complete-task.md [task_id]
```

## Prerequisites
- Phase 0 complete
- Task exists in `.claude/tasks/task-[id].json`
- Task status is "Pending" (not "Finished", "In Progress", or "Broken Down")

## Process

### 1. Load and Validate Task
Read `.claude/tasks/task-[id].json`:

**Validation Checks:**
- Task exists
- Task status is "Pending"
- If task has dependencies, check all dependencies are "Finished"
- If task is parent (has subtasks), status should be "Broken Down" → cannot work on it
- If task difficulty ≥7, suggest breakdown first

**If validation fails:**
```
❌ Cannot work on Task [id]

Reason: [Specific issue]

[Suggested action based on issue]
```

### 2. Load Context Files

**Always Load (Core Context):**
1. `.claude/context/glossary.md` - Variable definitions and naming rules
2. `.claude/context/assumptions.md` - All interpretation decisions
3. `.claude/context/llm-pitfalls.md` - Implementation checklist
4. `.claude/context/power-query.md` - M code conventions
5. `.claude/context/naming.md` - Naming rules
6. `.claude/context/error-handling.md` - Error patterns

**Task-Specific Context:**
7. `.claude/reference/data-contracts.md` - Find schema for this query
8. `.claude/reference/query-manifest.md` - Find query description
9. `.claude/reference/dependency-graph.md` - Check dependencies and impact

**If Query Implementation Task:**
10. Load any dependent query .m files from `power-query/`
11. Review calculation method docs referenced in task notes

### 3. Update Task Status
Set task status to "In Progress":

```json
{
  "status": "In Progress",
  "start_date": "[current date]"
}
```

### 4. Present Task Summary
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting Task [id]: [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Description:** [Task description]
**Difficulty:** [Score]/10
**Dependencies:** [List or "None"]

**Loaded Context:**
✅ Glossary: [N] terms available
✅ Assumptions: [N] decisions available
✅ LLM Pitfalls: Checklist loaded
✅ Data Contract: [QueryName] schema loaded
✅ Dependent Queries: [List any loaded]

**Implementation Plan:**
[Claude generates plan based on task description and context]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5. Execute Task

**For Query Implementation Tasks:**

#### A. Review Requirements
- Check data contract for expected input/output schema
- Review query manifest for transformation logic
- Check assumptions for any relevant interpretation decisions
- Verify variable names in glossary

#### B. Check LLM Pitfalls Checklist
Before writing code, verify:
- [ ] All ambiguities addressed in assumptions.md
- [ ] Formula broken into explicit steps
- [ ] Units documented for every value
- [ ] Dependencies mapped
- [ ] Edge cases defined
- [ ] Nulls handled explicitly
- [ ] No silent error handling
- [ ] Variable names from glossary

#### C. Implement Query
Create or update .m file in `power-query/`:

**Code Structure:**
```m
// Query: [QueryName]
// Purpose: [From query manifest]
// Dependencies: [List]
// Generated: [Date]
// Task: [task_id]

// SCHEMA INPUT
// [List expected columns with types and units from data contract]

// SCHEMA OUTPUT  
// [List output columns with types and units from data contract]

let
    // Step 1: [Description]
    // Context: [Reference to assumption/formula if applicable]
    Source = [implementation],
    
    // Step 2: [Description]
    // Unit: [if applicable]
    StepName = [implementation],
    
    // Step 3: [Description]
    // Validation: [explain check]
    ValidationStep = [implementation],
    
    // Error handling
    // NOTE: No try/otherwise - let errors surface
    
    // Final output
    Output = StepName
in
    Output
```

**Code Standards:**
- Use PascalCase for step variables
- snake_case for column names (from glossary)
- Explicit type conversions
- Comments for every transformation
- NO Table.Buffer unless explicitly needed
- NO try/otherwise without justification
- Units in comments where applicable

#### D. Validate Implementation
Run mental validation:
1. Does output match data contract schema?
2. Are all variables from glossary?
3. Are units consistent?
4. Are nulls handled per assumptions?
5. Is error handling appropriate?
6. Are all steps commented?

#### E. Document in Code
Add header comment block:
```m
// VALIDATION CHECKLIST
// [x] Output schema matches data-contracts.md
// [x] Variable names from glossary.md
// [x] Units documented
// [x] Assumptions referenced: #5, #12
// [x] Dependencies verified
// [x] Edge cases handled
```

### 6. Extension Auto-Sync
After saving .m file:
- Extension automatically syncs to Excel (if watch mode active)
- Backup created before sync
- User can verify in Excel if needed

### 7. Schema Validation
Run static validation:
- Parse .m file output
- Compare against data contract
- Report any discrepancies

```
Schema Validation: [QueryName]

Expected (from data-contracts.md):
✅ RecycledContentShare: decimal, non-null
✅ TotalEmissions: decimal, non-null
⚠️ ComplianceFlag: text, non-null (not found in output)

Result: 1 issue found
```

If issues found, fix before completing.

### 8. Complete Task
Update task file:

```json
{
  "status": "Finished",
  "completion_date": "[current date]",
  "hours_spent": "[estimate based on difficulty]",
  "notes": "Implemented [QueryName] query. Schema validated. [Any additional notes]"
}
```

**If parent task exists:**
Check if all sibling subtasks are finished.
If yes, auto-complete parent task.

### 9. Update Task Overview
Run sync-tasks command to update `task-overview.md`.

### 10. Final Summary
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task [id] Complete: [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Completed:**
- Implemented: power-query/[QueryName].m
- Schema: ✅ Validated
- Auto-sync: ✅ Updated in Excel
- Task status: Finished

**Changes Made:**
[Summary of implementation]

**Next Tasks Available:**
[List tasks that are now unblocked, if any]

**Suggested Next Action:**
@.claude/commands/complete-task.md [next_task_id]

OR

Review the implementation in Excel before continuing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Git commit suggested:
```
git add power-query/[QueryName].m .claude/tasks/task-[id].json
git commit -m "Task [id]: Implement [QueryName] query"
```
```

## Error Handling

### Task Not Found
```
❌ Task [id] not found

Available tasks: [List pending task IDs]
Check: @.claude/tasks/task-overview.md
```

### Task Has Unfinished Dependencies
```
❌ Cannot start Task [id]: Dependencies not complete

Unfinished dependencies:
- Task [dep_id1]: [Title] - Status: [Status]
- Task [dep_id2]: [Title] - Status: [Status]

Complete these tasks first, or remove dependencies if incorrect.
```

### Task Is "Broken Down"
```
❌ Cannot work on Task [id]: Status is "Broken Down"

This task has been split into subtasks. Work on subtasks instead:
- Task [sub_id1]: [Title]
- Task [sub_id2]: [Title]
- Task [sub_id3]: [Title]

Subtasks progress: [X]/[Total] complete

Parent task will auto-complete when all subtasks finish.
```

### Task Difficulty Too High
```
⚠️ Task [id] has difficulty [score] (≥7)

High-difficulty tasks should be broken down before starting.

Suggested: Run @.claude/commands/breakdown.md [id] first

This will split the task into manageable subtasks (difficulty ≤6).

Continue anyway? [Warn but allow]
```

### Schema Validation Fails
```
⚠️ Schema validation found issues:

Expected columns missing:
- [ColumnName]: [type]

Unexpected columns found:
- [ColumnName]: [type]

Please review and fix before completing task.
```

### Query File Already Exists
```
ℹ️ File power-query/[QueryName].m already exists

Actions:
A) Overwrite with new implementation
B) Edit existing file
C) Create backup before modifying

Select: [A/B/C]
```

## Special Cases

### First Task of Project
```
🎉 Starting first task!

This is where the rubber meets the road. All the Phase 0 work
(glossary, assumptions, contracts) now pays off.

Claude has complete context and will implement exactly per specs.
Watch mode will keep Excel in sync.

Let's build! 🚀
```

### Last Task
```
🎉 Final task!

After this completes, all planned queries will be implemented.

Consider:
- Full testing with real data (outside Claude's view)
- Documentation review
- Performance testing
- Git tag for v1.0
```

### Parent Task Auto-Complete
```
✅ Task [id] complete

🎉 This was the last subtask of Task [parent_id]!

Parent task "[ParentTitle]" is now automatically marked as Finished.

All subtasks complete:
- Task [sub1]: ✅
- Task [sub2]: ✅
- Task [sub3]: ✅

Great work on completing a complex task!
```

## Output Files
- `.claude/tasks/task-[id].json` - Updated status
- `power-query/[QueryName].m` - Created/modified query
- `.claude/tasks/task-overview.md` - Updated (via sync-tasks)

## Notes

- **Always use this command** to work on tasks - don't manually update status
- Claude has FULL context - no need to explain basics from glossary/assumptions
- Schema validation is automatic
- Git commits should reference task ID
- Watch mode syncs automatically - no manual copy/paste needed
- High-difficulty tasks (≥7) should be broken down first
- Parent tasks cannot be worked on directly - work on subtasks
