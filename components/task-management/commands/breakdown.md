# Command: Breakdown High-Difficulty Tasks

## Purpose
Split tasks with difficulty ≥7 into smaller, manageable subtasks to reduce LLM error risk. Automatically transitions parent task to "Broken Down" status and establishes completion dependency chain.

## Context Required
- `.claude/tasks/*.json` (all task files)
- `.claude/context/validation-rules.md`
- `.claude/reference/difficulty-guide.md`

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
- Identify logical components that can be separated
- Design subtasks following these rules:
  - Each subtask difficulty MUST be ≤6
  - Subtasks MUST cover all original requirements
  - Subtasks SHOULD be independently testable
  - Create natural dependency order if needed

### 2.5. Suggest Relevant Patterns (ATEF Enhancement)
**If pattern library exists:**
- Call `find-pattern.md` for the parent task
- Review suggested patterns that match task description
- For each subtask being created:
  - Check if pattern matches subtask description
  - Note applicable patterns in subtask planning
  - Include pattern recommendation in subtask notes

**Example pattern suggestions:**
```
Parent task: "Create Silver layer for sales data"
Pattern found: power-query-silver.pattern.md

Subtasks with pattern suggestions:
- Subtask 1: "Load Bronze layer" → power-query-silver.pattern.md (step 1)
- Subtask 2: "Clean and standardize columns" → power-query-silver.pattern.md (steps 2-4)
- Subtask 3: "Add validation timestamp" → power-query-silver.pattern.md (step 6)
```

**Display to user:**
```
⚡ Pattern Suggestions:
  Main pattern: power-query-silver.pattern.md matches parent task

  Subtask recommendations:
  - Task 13: Consider power-query-silver.pattern.md for Bronze loading
  - Task 14: Consider power-query-silver.pattern.md for transformations
  - Task 15: Consider power-query-silver.pattern.md for metadata
```

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
    "notes": "Created from breakdown of Task {original_task_id}"
  }
  ```
- **ATEF Enhancement**: If pattern suggested for this subtask, add to notes:
  ```
  "notes": "Created from breakdown of Task {original_task_id}. Suggested pattern: {pattern_id}"
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
  "id": "12",
  "title": "Build emissions data ETL pipeline",
  "difficulty": 8,
  "status": "Pending"
}
```

**After Breakdown:**

**Parent Task (task-12.json):**
```json
{
  "id": "12",
  "title": "Build emissions data ETL pipeline",
  "difficulty": 8,
  "status": "Broken Down",
  "breakdown_history": "2024-01-15",
  "subtasks": ["13", "14", "15", "16", "17"],
  "notes": "[2024-01-15] Task broken down into 5 subtasks: #13-17. Parent will auto-complete when all subtasks finish."
}
```

**Created Subtasks:**
- Task 13: "Design pipeline architecture" (difficulty: 4, parent: "12")
- Task 14: "Build API connectors for emissions data sources" (difficulty: 5, parent: "12")
- Task 15: "Implement data transformation with Polars" (difficulty: 6, parent: "12")
- Task 16: "Create Azure SQL loader" (difficulty: 5, parent: "12")
- Task 17: "Add error handling and logging" (difficulty: 4, parent: "12")

## Output Location
- New task JSON files in `.claude/tasks/` (one per subtask)
- Updated parent task JSON file (status → "Broken Down")
- Updated `.claude/tasks/task-overview.md` (via sync-tasks)
- Console report of breakdown results

## Error Handling
- If task already "Broken Down": "Task #{id} has already been broken down into subtasks #{list}. Use update-tasks.md to modify existing subtasks."
- If task difficulty <7: "Task #{id} has difficulty {X} which is below the breakdown threshold (7). Breakdown not needed."
- If task "Finished": "Cannot break down completed task #{id}."
