# Command: Run Validation Gate

## Purpose
Execute a specific validation gate (pre-execution, post-execution, or checkpoint) and return structured validation results.

## Context Required
- Gate type (`pre-execution`, `post-execution`, or `checkpoint`)
- Task JSON file (`.claude/tasks/task-{id}.json`)
- Gate definition file from `components/validation-gates/gates/{gate-type}.md`
- Optional: `components/pattern-library/` (for pattern matching)
- Optional: `components/error-catalog/catalog/` (for error suggestions)

## Process

### 1. Load Task
- Read task JSON file for specified task ID
- Verify task file exists
- Parse task data

### 2. Load Gate Definition
- Read gate markdown file based on gate type:
  - `pre-execution` → `components/validation-gates/gates/pre-execution.md`
  - `post-execution` → `components/validation-gates/gates/post-execution.md`
  - `checkpoint` → `components/validation-gates/gates/checkpoint-gate.md`

### 3. Execute Checks
For each check defined in the gate:

#### Pre-Execution Checks:
1. **Status Check** (BLOCKING):
   - Verify status is "Pending" or "In Progress"
   - If status is "Broken Down" or "Finished", add blocking failure

2. **Dependency Check** (BLOCKING):
   - Load each dependency task JSON
   - Verify all have status "Finished"
   - If any incomplete, add blocking failure with dep ID

3. **Difficulty Check** (BLOCKING):
   - If difficulty >= 7 AND status != "Broken Down"
   - Add blocking failure requiring breakdown

4. **Context Check** (WARNING):
   - For each path in files_affected
   - Check if file exists
   - If not found, add warning (may be intentional for new files)

5. **Pattern Check** (INFO):
   - If pattern library exists, call find-pattern.md
   - Match task title/description against pattern triggers
   - Add available patterns to info array

#### Post-Execution Checks:
1. **Files Modified Check** (WARNING):
   - For each file in files_affected
   - Check modification timestamp
   - If older than task start time, add warning

2. **Notes Check** (WARNING):
   - Compare notes field length before/after
   - If unchanged, add warning

3. **Time Tracking Check** (INFO):
   - If estimated_hours exists and actual_hours doesn't
   - Add info suggestion

4. **Parent Completion Check** (AUTO):
   - If parent_task field exists:
     - Load parent task
     - Find all sibling tasks (same parent_task value)
     - Count siblings with status "Finished"
     - If ALL finished:
       - Update parent status to "Finished"
       - Update parent updated_date
       - Add to parent notes
       - Add to auto_actions array
       - Recursively check parent's parent

5. **Error Pattern Check** (INFO):
   - If error catalog exists, call suggest-prevention.md
   - Match task keywords against error keywords
   - Add relevant error warnings to info array

### 4. Determine Pass/Fail
- If ANY blocking failures exist: `passed = false`
- Otherwise: `passed = true`
- **Note**: Warnings and info don't affect passed status

### 5. Generate Result Object
Create gate result conforming to schemas/gate-result.schema.json:
- `gate`: Gate type executed
- `task_id`: Task ID
- `passed`: Boolean result
- `blocking_failures`: Array of blocking issues
- `warnings`: Array of warnings
- `info`: Array of informational messages
- `auto_actions`: Array of automated actions taken
- `timestamp`: Current timestamp in "YYYY-MM-DD HH:MM:SS" format

### 6. Return Result
- Return gate result object as JSON
- Display formatted output to user:
  - If failed: Show blocking failures prominently with remediations
  - If warnings: List warnings clearly
  - If info: Show suggestions
  - If auto_actions: Confirm what was automated

## Output Location
- Gate result returned as JSON object (not saved to file)
- Used by calling command (e.g., complete-task.md)
- Optionally logged to task notes

## Example Usage

### Pre-Execution Gate
```
Input: run-gate.md --gate=pre-execution --task-id=15

Process:
1. Load task-15.json
2. Check status: "Pending" ✓
3. Check dependencies: [12] → Load task-12.json → status "Finished" ✓
4. Check difficulty: 4 < 7 ✓
5. Check files_affected: ["queries/Bronze_SalesData.m"] → Not found (warning)
6. Check patterns: Found "pattern-microsoft-pq-bronze" (info)

Output:
{
  "gate": "pre-execution",
  "task_id": "15",
  "passed": true,
  "blocking_failures": [],
  "warnings": ["File queries/Bronze_SalesData.m not found. Verify path before proceeding."],
  "info": ["Pattern available: pattern-microsoft-pq-bronze. Consider using."],
  "timestamp": "2025-12-05 10:30:15"
}

Display:
✓ Pre-execution validation PASSED

⚠ Warnings:
  - File queries/Bronze_SalesData.m not found. Verify path before proceeding.

ℹ Suggestions:
  - Pattern available: pattern-microsoft-pq-bronze. Consider using.
```

### Post-Execution with Auto-Completion
```
Input: run-gate.md --gate=post-execution --task-id=17

Process:
1. Load task-17.json
2. Check files_affected: All modified ✓
3. Check notes: Added ✓
4. Check parent_task: "12"
5. Load task-12.json, find siblings [13, 14, 15, 16, 17]
6. Check sibling status: All "Finished" → Auto-complete parent 12
7. Update task-12.json: status = "Finished"

Output:
{
  "gate": "post-execution",
  "task_id": "17",
  "passed": true,
  "blocking_failures": [],
  "warnings": [],
  "info": [],
  "auto_actions": ["Parent task 12 auto-completed (all subtasks finished)"],
  "timestamp": "2025-12-05 11:45:30"
}

Display:
✓ Post-execution validation PASSED

⚡ Auto-actions:
  - Parent task 12 auto-completed (all subtasks finished)
```

### Failed Pre-Execution
```
Input: run-gate.md --gate=pre-execution --task-id=25

Process:
1. Load task-25.json
2. Check status: "Pending" ✓
3. Check dependencies: [22, 23] → Load task-23.json → status "In Progress" ✗
4. Check difficulty: 5 < 7 ✓

Output:
{
  "gate": "pre-execution",
  "task_id": "25",
  "passed": false,
  "blocking_failures": [
    {
      "check": "Dependency Check",
      "message": "Cannot start task 25: dependency 23 not finished",
      "remediation": "Complete dependency task 23 first"
    }
  ],
  "warnings": [],
  "info": [],
  "timestamp": "2025-12-05 12:00:00"
}

Display:
✗ Pre-execution validation FAILED

🛑 Blocking Issues:
  [Dependency Check] Cannot start task 25: dependency 23 not finished
  → Remediation: Complete dependency task 23 first

Task execution halted. Resolve blocking issues before proceeding.
```

## Integration Notes
- This command is called by `complete-task.md` at specific points
- Can also be called manually for testing or verification
- Gate results can be stored in task JSON under optional `validation` field
- Auto-actions are executed immediately and logged
