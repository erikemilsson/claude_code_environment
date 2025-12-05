# Pre-Execution Validation Gate

## Purpose
Verify task is ready for execution. Blocks start if critical checks fail.

## Checks (in order)

### 1. Status Check (BLOCKING)
- Task status MUST be "Pending" or "In Progress"
- Task status MUST NOT be "Broken Down" or "Finished"
- **If FAIL**: "Cannot start task {id}: status is {status}"
- **Remediation**:
  - If "Broken Down": Work on subtasks instead
  - If "Finished": Task already complete
  - Otherwise: Update status to "Pending" first

### 2. Dependency Check (BLOCKING)
- All tasks in `dependencies` array MUST have status "Finished"
- **If FAIL**: "Cannot start task {id}: dependency {dep_id} not finished"
- **Remediation**: Complete dependency task {dep_id} first

### 3. Difficulty Check (BLOCKING)
- If difficulty >= 7 AND status != "Broken Down":
  - **FAIL**: "Task {id} has difficulty {d}. Must break down first."
  - **Remediation**: Use breakdown.md command to split into subtasks

### 4. Context Check (WARNING)
- If `files_affected` specified, verify files exist
- **If WARN**: "File {path} not found. Verify path before proceeding."
- **Note**: New files to be created should be listed but won't exist yet

### 5. Pattern Check (INFO)
- Search pattern library for matching patterns
- Match task title and description against pattern triggers
- **If found**: "Pattern available: {pattern_name}. Consider using."
- **Note**: Call find-pattern.md command if pattern library exists

### 6. Error Prevention Check (INFO)
- Search error catalog for similar past mistakes
- Call suggest-prevention.md command if error catalog exists
- Match task keywords against error prevention keywords
- **If matches found**: Include top error warnings in info section
- **Format**:
  ```
  ERROR PREVENTION: [SEVERITY] Error {id}: {title}
    → {warning_message}
    → Pre-check: {pre_execution_check}
    → Pattern: {pattern_to_use}
    (Occurred {recurrence_count} times previously)
  ```
- **Note**: Helps learn from past failures and prevent repeated mistakes

## Output Format

Returns a gate result object conforming to gate-result.schema.json:

```json
{
  "gate": "pre-execution",
  "task_id": "string",
  "passed": boolean,
  "blocking_failures": [
    {
      "check": "string",
      "message": "string",
      "remediation": "string"
    }
  ],
  "warnings": ["string"],
  "info": ["string"],
  "timestamp": "YYYY-MM-DD HH:MM:SS"
}
```

## Integration
- Called by `complete-task.md` after loading task, before status change
- If `passed: false`, HALT execution and display blocking failures with remediations
- If warnings exist, display but allow user to continue
- If patterns found, offer to apply them

## Example Results

### Passing Gate
```json
{
  "gate": "pre-execution",
  "task_id": "15",
  "passed": true,
  "blocking_failures": [],
  "warnings": [],
  "info": ["Pattern available: pattern-microsoft-pq-bronze"],
  "timestamp": "2025-12-05 10:30:15"
}
```

### Failing Gate (Unfinished Dependency)
```json
{
  "gate": "pre-execution",
  "task_id": "15",
  "passed": false,
  "blocking_failures": [
    {
      "check": "Dependency Check",
      "message": "Cannot start task 15: dependency 12 not finished",
      "remediation": "Complete dependency task 12 first"
    }
  ],
  "warnings": [],
  "info": [],
  "timestamp": "2025-12-05 10:30:15"
}
```

### Passing with Warning
```json
{
  "gate": "pre-execution",
  "task_id": "15",
  "passed": true,
  "blocking_failures": [],
  "warnings": ["File queries/Bronze_SalesData.m not found. Verify path before proceeding."],
  "info": ["Pattern available: pattern-microsoft-pq-bronze"],
  "timestamp": "2025-12-05 10:30:15"
}
```

### Passing with Error Prevention Warnings
```json
{
  "gate": "pre-execution",
  "task_id": "42",
  "passed": true,
  "blocking_failures": [],
  "warnings": [],
  "info": [
    "Pattern available: power-query-silver.pattern.md",
    "ERROR PREVENTION: [CRITICAL] Error ERR-PQ-002: Silver query sources directly from file",
    "  → ⚠ Silver Layer Rule: ALWAYS source from Bronze query! Never connect directly to files.",
    "  → Pre-check: Verify Silver query FIRST STEP is Bronze query reference, NOT file source",
    "  → Pattern: power-query-silver.pattern.md",
    "  (Occurred 3 times previously)",
    "ERROR PREVENTION: [HIGH] Error ERR-PQ-001: Type conversion at Bronze layer",
    "  → ⚠ Bronze Layer Rule: NO transformations at Bronze! All type conversions go in Silver.",
    "  → Pre-check: Verify Bronze query has ZERO transformations",
    "  → Pattern: power-query-bronze.pattern.md",
    "  (Occurred 1 time previously)"
  ],
  "timestamp": "2025-12-05 14:30:15"
}
```
