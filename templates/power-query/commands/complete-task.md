# Command: Complete Task (Phase 1)

## Purpose
Begin working on a task with proper status tracking and full context loading. This is the standard way to start any task work in Power Query projects.

## Context Required
- Specific task JSON file (e.g., `.claude/tasks/task-[id].json`)
- `.claude/tasks/task-overview.md`
- `.claude/context/validation-rules.md`
- **Power Query core context:**
  - `.claude/context/glossary.md` - Variable definitions and naming rules
  - `.claude/context/assumptions.md` - All interpretation decisions
  - `.claude/context/llm-pitfalls.md` - Implementation checklist
  - `.claude/context/power-query.md` - M code conventions
  - `.claude/context/naming.md` - Naming rules
  - `.claude/context/error-handling.md` - Error patterns
- **Task-specific context:**
  - `.claude/reference/data-contracts.md` - Schema definitions
  - `.claude/reference/query-manifest.md` - Query descriptions
  - `.claude/reference/dependency-graph.md` - Dependencies and impact
- Any other context files relevant to the task

## Process

### 1. Load task details:
   - Read the specified task JSON file
   - Read task-overview.md to check dependencies and current state
   - **Check if status is "Broken Down":**
     * If yes, halt with message: "❌ Task {id} has been broken down into subtasks {list}. Please work on the individual subtasks instead. Use '@.claude/commands/complete-task.md {subtask_id}' to start a subtask."
   - Verify all dependencies are marked "Finished"
   - If task difficulty ≥7, warn user and suggest breakdown first (but allow to continue if user confirms)

### 2. Load Power Query context files:

   **Core Context (Always Load):**
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

### 3. Confirm with user:
   - Display task title, description, and estimated hours
   - Show any blockers or dependencies
   - If task has `parent_task`, show parent context
   - Display loaded context summary:
     ```
     **Loaded Context:**
     ✅ Glossary: [N] terms available
     ✅ Assumptions: [N] decisions available
     ✅ LLM Pitfalls: Checklist loaded
     ✅ Data Contract: [QueryName] schema loaded
     ✅ Dependent Queries: [List any loaded]
     ```
   - Ask: "Ready to start work on Task X: [title]? (yes/no)"
   - Wait for user confirmation before proceeding

### 4. Update status to "In Progress":
   - Update task JSON file:
     * `"status": "In Progress"`
     * `"updated_date"` to current date (YYYY-MM-DD format)
     * If not already set, add `"actual_hours": 0`

### 5. Sync overview:
   - Run @.claude/commands/sync-tasks.md to update task-overview.md

### 6. Begin work:
   - Load any standards or context files mentioned in `files_affected`
   - Perform the task work
   - Track any issues or notes

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
   Add validation checklist to query header:
   ```m
   // VALIDATION CHECKLIST
   // [x] Output schema matches data-contracts.md
   // [x] Variable names from glossary.md
   // [x] Units documented
   // [x] Assumptions referenced: #5, #12
   // [x] Dependencies verified
   // [x] Edge cases handled
   ```

   #### F. Extension Auto-Sync
   After saving .m file:
   - Extension automatically syncs to Excel (if watch mode active)
   - Backup created before sync
   - User can verify in Excel if needed

   #### G. Schema Validation
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

   If issues found, fix before completing task.

### 7. Finishing a Task - Update upon completion:
   - Update task JSON file:
     * `"status": "Finished"`
     * `"updated_date"` to completion date (YYYY-MM-DD format)
     * `"actual_hours"` with time spent
     * Add relevant notes to `"notes"` field including:
       - What was accomplished (e.g., "Implemented [QueryName] query")
       - Schema validation status
       - Any deviations from the original plan
       - Fixes or workarounds applied
       - Files created/modified
       - Any blockers encountered
       - References to assumptions or decisions made

   - **Check for parent task auto-completion:**
     * Read task's `parent_task` field
     * If parent_task exists:
       - Load parent task JSON file
       - If parent status == "Broken Down":
         * Get all task IDs from parent's `subtasks` array
         * Load each subtask JSON and check status
         * If ALL subtasks are "Finished":
           - Update parent task JSON:
             * `"status": "Finished"`
             * `"updated_date"` to current date
             * Add to `"notes"`: "Auto-completed: all subtasks finished on {date}"
           - Report to user: "🎉 Completing this subtask also completed parent Task #{parent_id}: {parent_title}!"

### 8. Final sync and feedback:
   - Run @.claude/commands/sync-tasks.md again
   - Provide completion summary:
     ```
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ✅ Task #{id} Complete: {title}
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

     **Completed:**
     - Implemented: power-query/[QueryName].m
     - Schema: ✅ Validated
     - Auto-sync: ✅ Updated in Excel

     **Summary:**
     {What was accomplished}

     **Time:**
     - Estimated: {estimated_hours} hours
     - Actual: {actual_hours} hours

     **Files:**
     {Files created/modified}

     **Blockers encountered:** {Any blockers or "None"}

     {If parent was auto-completed, mention it}

     **Next Tasks Available:**
     {List tasks that are now unblocked, if any}

     **Suggested next task:** Task #{next_id} "{title}" (difficulty: {score})

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

     Git commit suggested:
     ```
     git add power-query/[QueryName].m .claude/tasks/task-{id}.json
     git commit -m "Task {id}: Implement [QueryName] query"
     ```
     ```

## Output Location
- Updated task JSON file in `.claude/tasks/`
- Possibly updated parent task JSON file (if auto-completion triggered)
- Updated `.claude/tasks/task-overview.md` (via sync-tasks)
- Console feedback on task progress and completion
- Power Query .m file in `power-query/` directory
- Any work products in their appropriate project locations

## Example: Parent Auto-Completion

User: @.claude/commands/complete-task.md 17

[Task work happens... implementing RecycledContentShare calculation query]

```
✅ Task #17 "Implement RecycledContentShare calculation" completed!

- Estimated: 3 hours
- Actual: 2.5 hours
- Files created: power-query/RecycledContentShare.m
- Schema: ✅ Validated against data-contracts.md
- Auto-sync: ✅ Synced to Excel

🎉 Completing this subtask also completed parent Task #12: "Build emissions calculations module"! All 5 subtasks (13-17) are now finished.

Suggested next task: Task #18 "Implement ComplianceFlag query" (difficulty: 4)
```

## Special Cases

### First Task of Project
```
🎉 Starting first task!

This is where the rubber meets the road. All the Phase 0 work
(glossary, assumptions, contracts) now pays off.

Claude has complete context and will implement exactly per specs.
Watch mode will keep Excel in sync.

Let's build!
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
✅ Task {id} complete

🎉 This was the last subtask of Task {parent_id}!

Parent task "{ParentTitle}" is now automatically marked as Finished.

All subtasks complete:
- Task {sub1}: ✅
- Task {sub2}: ✅
- Task {sub3}: ✅

Great work on completing a complex task!
```

### Task Not Found
```
❌ Task {id} not found

Available tasks: {List pending task IDs}
Check: @.claude/tasks/task-overview.md
```

### Task Has Unfinished Dependencies
```
❌ Cannot start Task {id}: Dependencies not complete

Unfinished dependencies:
- Task {dep_id1}: {Title} - Status: {Status}
- Task {dep_id2}: {Title} - Status: {Status}

Complete these tasks first, or remove dependencies if incorrect.
```

### Task Is "Broken Down"
```
❌ Cannot work on Task {id}: Status is "Broken Down"

This task has been split into subtasks. Work on subtasks instead:
- Task {sub_id1}: {Title}
- Task {sub_id2}: {Title}
- Task {sub_id3}: {Title}

Subtasks progress: {X}/{Total} complete

Parent task will auto-complete when all subtasks finish.
```

### Task Difficulty Too High
```
⚠️ Task {id} has difficulty {score} (≥7)

High-difficulty tasks should be broken down before starting.

Suggested: Run @.claude/commands/breakdown.md {id} first

This will split the task into manageable subtasks (difficulty ≤6).

Continue anyway? [Warn but allow]
```

### Schema Validation Fails
```
⚠️ Schema validation found issues:

Expected columns missing:
- {ColumnName}: {type}

Unexpected columns found:
- {ColumnName}: {type}

Please review and fix before completing task.
```

### Query File Already Exists
```
ℹ️ File power-query/{QueryName}.m already exists

Actions:
A) Overwrite with new implementation
B) Edit existing file
C) Create backup before modifying

Select: [A/B/C]
```

## Notes

- **Always use this command** to work on tasks - don't manually update status
- Claude has FULL context from Phase 0 - no need to explain basics from glossary/assumptions
- Schema validation is automatic and compares against data-contracts.md
- Git commits should reference task ID for traceability
- Watch mode syncs automatically - no manual copy/paste needed
- High-difficulty tasks (≥7) should be broken down first for better success rate
- Parent tasks cannot be worked on directly - work on subtasks instead
- Parent tasks auto-complete when all subtasks are finished
- Transparency in notes is critical - document deviations, fixes, and workarounds
