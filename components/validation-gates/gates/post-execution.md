# Post-Execution Validation Gate

## Purpose
Verify task completed correctly. Flags issues before marking finished and handles automatic parent task completion.

## Checks (in order)

### 1. Files Modified Check (WARNING)
- If `files_affected` specified, verify files were touched
- Check file modification timestamps against task start time
- **If WARN**: "Expected file {path} not modified during task"
- **Note**: Warns but doesn't block - file may have been intentionally skipped

### 2. Notes Check (WARNING)
- Task `notes` field should have content added
- Compare notes before task start vs after
- **If WARN**: "No notes added. Consider documenting what was done."
- **Recommendation**: Good practice to document changes, decisions, issues encountered

### 3. Time Tracking Check (INFO)
- If `estimated_hours` set but `actual_hours` not updated
- **If INFO**: "Consider updating actual_hours for better estimation in future"
- **Note**: Optional metadata for project planning

### 4. Parent Completion Check (AUTO)
- If task has `parent_task` field set:
  1. Load parent task JSON
  2. Check all sibling tasks (tasks with same parent_task)
  3. If ALL siblings have status "Finished":
     - Update parent status to "Finished"
     - Add auto-action: "Parent task {id} auto-completed"
     - Update parent's updated_date
- **Auto-action logged**: "Parent task {parent_id} auto-completed (all subtasks finished)"

### 5. Error Pattern Check (INFO)
- Check error catalog for this task type
- Match task description/type against error catalog keywords
- **If common errors exist**: "Review: {error_category} common in similar tasks. See error catalog entry {error_id}"
- **Note**: Helps prevent recurring issues

## Output Format

Returns a gate result object conforming to gate-result.schema.json:

```json
{
  "gate": "post-execution",
  "task_id": "string",
  "passed": boolean,
  "blocking_failures": [],
  "warnings": ["string"],
  "info": ["string"],
  "auto_actions": ["string"],
  "timestamp": "YYYY-MM-DD HH:MM:SS"
}
```

## Integration
- Called by `complete-task.md` after work done, before status = "Finished"
- Display any warnings and info to user
- Execute auto-actions automatically (e.g., parent completion)
- If blocking failures (rare at this stage): offer rollback option
- **Note**: Post-execution gate rarely blocks, mainly provides feedback and automation

## Example Results

### Passing Gate with Parent Auto-Completion
```json
{
  "gate": "post-execution",
  "task_id": "17",
  "passed": true,
  "blocking_failures": [],
  "warnings": [],
  "info": ["Consider updating actual_hours for better estimation in future"],
  "auto_actions": ["Parent task 12 auto-completed (all subtasks finished)"],
  "timestamp": "2025-12-05 11:45:30"
}
```

### Passing with Warnings
```json
{
  "gate": "post-execution",
  "task_id": "15",
  "passed": true,
  "blocking_failures": [],
  "warnings": [
    "Expected file config/settings.json not modified during task",
    "No notes added. Consider documenting what was done."
  ],
  "info": [],
  "auto_actions": [],
  "timestamp": "2025-12-05 11:45:30"
}
```

### With Error Pattern Suggestion
```json
{
  "gate": "post-execution",
  "task_id": "23",
  "passed": true,
  "blocking_failures": [],
  "warnings": [],
  "info": [
    "Review: DAX filter context errors common in similar tasks. See error catalog entry err-logic-001"
  ],
  "auto_actions": [],
  "timestamp": "2025-12-05 11:45:30"
}
```

## Parent Task Auto-Completion Logic

When a task with a parent completes:

1. **Load parent task**: Read parent task JSON file
2. **Find all siblings**: Get all tasks where `parent_task == parent_id`
3. **Check completion**: Verify ALL siblings have `status == "Finished"`
4. **Auto-complete parent**:
   - Set parent `status = "Finished"`
   - Update parent `updated_date = today`
   - Add to parent `notes`: "Auto-completed: all subtasks finished on {date}"
   - Save parent task JSON
5. **Recursive check**: If parent also has a parent, repeat this process
6. **Log action**: Add to gate result auto_actions array

### Example
```
Task 12 (parent, status: "Broken Down")
├── Task 13 (status: "Finished")
├── Task 14 (status: "Finished")
└── Task 15 (status: "In Progress" → "Finished")  ← Completing this task

When Task 15 finishes:
1. Post-execution gate runs
2. Detects parent_task: "12"
3. Loads Task 12, finds siblings 13, 14, 15
4. All siblings "Finished" → Auto-complete Task 12
5. Updates Task 12 status to "Finished"
6. Logs: "Parent task 12 auto-completed"
```
