# Command: Breakdown High-Difficulty Tasks (Phase 1)

## Purpose
Split tasks with difficulty ≥7 into smaller, manageable subtasks to reduce LLM error risk. Automatically transitions parent task to "Broken Down" status and establishes completion dependency chain.

## Context Required
- `.claude/tasks/*.json` (all task files)
- `.claude/context/validation-rules.md`
- `.claude/reference/difficulty-guide-pq.md`
- `.claude/context/glossary.md` (for PQ terminology)
- `.claude/reference/data-contracts.md` (if query task)
- `.claude/reference/query-manifest.md` (if query task)

## Process

### 1. Identify Breakdown Candidate
- Accept task ID as parameter: `@breakdown.md <task_id>`
- Read the specified task JSON file
- **Validate eligibility:**
  - Task difficulty MUST be ≥7
  - Task status MUST be "Pending" or "In Progress"
  - Task MUST NOT already have status "Broken Down" or "Finished"
  - If invalid, halt with clear error message

### 2. Analyze and Plan Breakdown
- Review task description, requirements, and `files_affected`
- **Analyze Power Query complexity dimensions:**
  - Query dependency depth
  - Formula complexity (M language operators, custom functions)
  - Error surface (null handling, type conversions, edge cases)
  - Regulatory precision requirements
  - Performance considerations (folding, buffering, caching)
- Identify logical components that can be separated
- Design subtasks following these rules:
  - Each subtask difficulty MUST be ≤6
  - Subtasks MUST cover all original requirements
  - Subtasks SHOULD be independently testable
  - Create natural dependency order if needed
- **Apply PQ breakdown patterns:**
  - **Pipeline Stages**: Input validation → Core transformation → Error handling → Output validation
  - **Formula Implementation**: Extract inputs → Implement formula steps → Add conversions → Handle edge cases → Add validation
  - **Integration Tasks**: Dependency setup → Query A → Query B → Integration logic → End-to-end testing
- Confirm breakdown plan with user before proceeding

### 3. Create Subtask Files
For each planned subtask:
- Generate new task ID (next sequential number)
- Create JSON file: `.claude/tasks/task-{new_id}.json`
- Set required fields:
  ```json
  {
    "id": "{new_id}",
    "title": "{subtask_title}",
    "description": "{detailed_description}",
    "difficulty": {1-6},
    "status": "Pending",
    "created_date": "{YYYY-MM-DD}",
    "updated_date": "{YYYY-MM-DD}",
    "parent_task": "{original_task_id}",
    "dependencies": [{other_subtask_ids_if_needed}],
    "subtasks": [],
    "notes": "Created from breakdown of Task {original_task_id}. Context: {relevant files/sections}"
  }
  ```

### 4. Update Parent Task to "Broken Down"

This is the CRITICAL step that solves the state ambiguity problem:

- Update original task JSON file:
  ```json
  {
    "status": "Broken Down",
    "updated_date": "{current_date}",
    "breakdown_history": "{current_date}",
    "subtasks": ["{subtask_1_id}", "{subtask_2_id}", ...],
    "notes": "{original_notes}\n\n[{date}] Task broken down into {N} subtasks: #{ids}. Parent task will auto-complete when all subtasks finish."
  }
  ```

### 5. Sync and Report
- Run `@.claude/commands/sync-tasks.md` to update overview
- Provide breakdown summary:
  - Original task ID and title
  - Number of subtasks created
  - List of subtask IDs with titles and difficulties
  - Confirmation that parent is now "Broken Down"
  - Next recommended action (start first subtask)

## Automatic Completion Logic

**IMPORTANT:** The following logic should be checked by `complete-task.md` whenever marking a subtask as "Finished":

```
When marking subtask as "Finished":
1. Read subtask's `parent_task` field
2. If parent_task exists:
   a. Load parent task JSON
   b. If parent status == "Broken Down":
      - Check ALL tasks in parent's `subtasks` array
      - If ALL subtasks have status "Finished":
        * Update parent status to "Finished"
        * Set parent updated_date to current date
        * Add note: "Auto-completed: all subtasks finished"
        * Report to user: "✅ Parent Task #{id} automatically completed!"
```

## Example Breakdown

**Input Task:**
```json
{
  "id": "5",
  "title": "Implement Gold_Calculate_CFF query",
  "difficulty": 8,
  "status": "Pending",
  "description": "Build Power Query to calculate Corporate Fossil Fuel percentage with regulatory precision"
}
```

**After Breakdown:**

**Parent Task (task-5.json):**
```json
{
  "id": "5",
  "title": "Implement Gold_Calculate_CFF query",
  "difficulty": 8,
  "status": "Broken Down",
  "breakdown_history": "2024-01-15",
  "subtasks": ["12", "13", "14", "15", "16"],
  "notes": "[2024-01-15] Task broken down into 5 subtasks: #12-16. Parent will auto-complete when all subtasks finish."
}
```

**Created Subtasks:**
- Task 12: "Extract and validate CFF input parameters" (difficulty: 4, parent: "5")
- Task 13: "Implement core CFF formula calculation" (difficulty: 5, parent: "5")
- Task 14: "Add error handling for null/missing values" (difficulty: 4, parent: "5")
- Task 15: "Implement edge case handling (zero denominators, negative values)" (difficulty: 3, parent: "5")
- Task 16: "Add compliance flag logic and precision rounding" (difficulty: 4, parent: "5")

## Output Location
- New task JSON files in `.claude/tasks/` (one per subtask)
- Updated parent task JSON file (status → "Broken Down")
- Updated `.claude/tasks/task-overview.md` (via sync-tasks)
- Console report of breakdown results

## Error Handling
- If task already "Broken Down": "Task #{id} has already been broken down into subtasks #{list}. Use update-tasks.md to modify existing subtasks."
- If task difficulty <7: "Task #{id} has difficulty {X} which is below the breakdown threshold (7). Breakdown not needed."
- If task "Finished": "Cannot break down completed task #{id}."

## Power Query Breakdown Guidelines

### Subtask Difficulty Scoring
- Target: 3-6 range (sweet spot for LLM execution with Power Query)
- Never create subtasks with difficulty >6
- If subtask would be >6, break it down further
- Consider PQ-specific complexity dimensions when scoring:
  - Query dependency depth
  - Formula complexity (M language operators, custom functions)
  - Error surface (null handling, type conversions)
  - Regulatory precision requirements
  - Performance considerations (folding, buffering)

### Subtask Scope
Each subtask should be:
- **Atomic**: One clear deliverable
- **Testable**: Can verify completion independently
- **Sequential**: Clear order of execution
- **Context-light**: Doesn't require extensive context from other tasks

### Common Power Query Breakdown Patterns

**Pattern A: Pipeline Stages**
For data transformation tasks:
1. Input validation (check source structure, required columns)
2. Core transformation (main M formula implementation)
3. Error handling (null checks, type validation)
4. Output validation (verify schema, data quality)

**Pattern B: Formula Implementation**
For calculation tasks:
1. Extract/validate inputs (read parameters, validate types)
2. Implement formula steps 1-N (break complex formulas into stages)
3. Add unit conversions (normalize units, apply multipliers)
4. Add edge case handling (zero denominators, negative values, nulls)
5. Add validation checks (regulatory precision, compliance flags)

**Pattern C: Integration Tasks**
For multi-query orchestration:
1. Dependency setup (ensure upstream queries exist)
2. Query A implementation (first dependent query)
3. Query B implementation (second dependent query)
4. Integration logic (merge/join operations)
5. End-to-end testing (validate complete pipeline)

### Dependency Management
- Keep dependency chains SHORT (max 2-3 levels)
- Prefer parallel subtasks over sequential when possible
- First subtask typically inherits parent's dependencies
- Later subtasks depend on earlier siblings
- Document query reference dependencies in notes

## Quality Checks

Before finalizing breakdown:
- [ ] All subtasks have difficulty ≤6
- [ ] All subtasks have clear descriptions
- [ ] Dependencies form valid DAG (no cycles)
- [ ] Execution order is logical
- [ ] Each subtask is independently completable
- [ ] Total effort roughly matches original task
- [ ] M language complexity is distributed evenly
- [ ] Query folding considerations are documented
- [ ] Error handling strategy is clear across subtasks

## Notes

- Breakdown creates ONE LEVEL of hierarchy only (no nested subtasks)
- Parent tasks track progress in task-overview.md
- Maximum subtasks per parent: ~8 (keep manageable)
- Sequential numbering: No gaps in task IDs
- Breaking down is permanent (cannot un-break)
- See `.claude/reference/breakdown-workflow.md` for detailed workflow
- Subtasks should reference parent in notes and include relevant file context
