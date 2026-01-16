# Command: Apply Pattern

## Purpose
Execute a selected pattern with task-specific parameters. Gathers inputs, applies template, verifies conditions, and records pattern usage.

## Context Required
- Pattern file from `components/pattern-library/patterns/{category}/{pattern-id}.pattern.md`
- Task JSON file (`.claude/tasks/task-{id}.json`)
- User-provided parameter values

## Process

### 1. Load Pattern
**Read pattern file:**
- Parse markdown structure
- Extract sections:
  - Metadata (ID, version, category, difficulty range)
  - Parameters table
  - Pre-conditions checklist
  - Template code/content
  - Post-conditions checklist
  - Anti-patterns warnings

**Validate pattern file:**
- Confirm all required sections present
- Check parameter table is well-formed
- Verify template has proper placeholders

### 2. Display Pattern Information
**Show user:**
```
Applying Pattern: {pattern_name}
Version: {version}
Category: {category}

Description: {what this pattern does}

Required Parameters: {count}
Optional Parameters: {count}
```

### 3. Gather Parameters
**For each parameter in Parameters table:**

#### Required Parameters
1. **Check if inferrable** from task JSON:
   - Task title might contain values
   - Task description might specify values
   - files_affected might indicate paths

2. **If not inferrable, prompt user:**
   ```
   Parameter: {param_name}
   Type: {type}
   Description: {description}

   Enter value for {param_name}:
   ```

3. **Validate input:**
   - Type check (string, number, boolean, etc.)
   - Format check (if pattern specifies format)
   - Required values must be non-empty

#### Optional Parameters
1. **Show defaults** if specified in pattern
2. **Ask user:**
   ```
   Optional parameter: {param_name} (default: {default})
   Press Enter to use default, or enter custom value:
   ```

3. **Use default if blank**, otherwise validate custom value

**Example Parameter Gathering:**
```
Pattern: power-query-bronze

Required Parameters:
1. source_name
   → Inferred from task: "Sales Data" (from "sales Excel file")
   Confirmed? [Y/N]: Y

2. source_type (Excel/CSV/SQL/API)
   → Cannot infer, prompting user
   Enter source_type: Excel

3. source_path
   → Not specified in task
   Enter source_path: C:\Data\sales.xlsx

4. output_table
   → Following naming convention: Bronze_{source_name}
   Generated: "Bronze_SalesData"
   Confirmed? [Y/N]: Y

Optional Parameters:
5. error_handling_strategy (default: "log and continue")
   Press Enter for default or customize: [Enter]
   → Using default
```

### 4. Verify Pre-Conditions
**Check each pre-condition:**

For each checkbox in Pre-Conditions section:
1. **Evaluate condition** (may require checks):
   - File exists?
   - Table name follows convention?
   - Required software installed?
   - Dependencies met?

2. **Mark status:**
   - ✓ Satisfied
   - ✗ Not satisfied
   - ? Uncertain (manual check needed)

3. **Display results:**
   ```
   Pre-Condition Checks:
   ✓ Source file/connection accessible
   ✓ Output table name follows naming convention (Bronze_*)
   ? Error handling strategy defined
     → Please confirm: Error handling strategy defined? [Y/N]
   ```

4. **If any fail:**
   ```
   ✗ Pre-condition not met: {condition}

   Resolve before applying pattern:
   → {remediation suggestion}

   Continue anyway? [Y/N] (not recommended)
   ```

### 5. Apply Template
**Replace placeholders:**

1. **Scan template** for {{placeholder}} patterns
2. **For each placeholder:**
   - Match to parameter name
   - Replace with gathered value
   - Handle special placeholders:
     - `{{timestamp}}`: Current date/time
     - `{{task_id}}`: Task ID
     - `{{user}}`: Username (if available)

3. **Handle conditional sections** (if pattern uses them):
   ```
   {{#if optional_param}}
   This section only included if optional_param provided
   {{/if}}
   ```

4. **Generate output code/content**

**Example Template Application:**
```
Template:
```powerquery-m
// Bronze Layer: {{source_name}}
// Source: {{source_type}}
// Generated: {{timestamp}}

let
    Source = {{source_connection_code}},
    AddedLoadTimestamp = Table.AddColumn(Source, "_LoadTimestamp",
        each DateTime.LocalNow(), type datetime),
in
    AddedLoadTimestamp
```

After substitution:
```powerquery-m
// Bronze Layer: Sales Data
// Source: Excel
// Generated: 2025-12-05 10:30:00

let
    Source = Excel.Workbook(File.Contents("C:\Data\sales.xlsx"), null, true),
    AddedLoadTimestamp = Table.AddColumn(Source, "_LoadTimestamp",
        each DateTime.LocalNow(), type datetime),
in
    AddedLoadTimestamp
```
```

### 6. Display Generated Output
**Show user the result:**
```
Generated output:

---
{generated code/content}
---

Review output:
1. Copy to clipboard and paste where needed
2. Save to file specified in task
3. Edit before using

Looks good? [Y/N]
```

### 7. Verify Post-Conditions
**Present post-condition checklist:**
```
Post-Condition Checklist:
After applying this pattern, verify:

□ All source columns preserved
□ _LoadTimestamp column added
□ _SourceFile column added
□ No data transformations applied
□ Query refreshes without error

Check these after implementing the generated code.
```

**Options:**
- Save checklist to task notes for later verification
- Include in task completion criteria

### 8. Record Pattern Usage
**Update task JSON:**

Add to task's optional `patterns` field:
```json
{
  "id": "15",
  "patterns": {
    "pattern_id": "pattern-microsoft-pq-bronze",
    "applied_at": "2025-12-05"
  },
  "notes": "Applied pattern: pattern-microsoft-pq-bronze with parameters..."
}
```

**Add to task notes:**
```
Applied pattern: pattern-microsoft-pq-bronze (v1.0.0)
Parameters used:
- source_name: Sales Data
- source_type: Excel
- source_path: C:\Data\sales.xlsx
- output_table: Bronze_SalesData
```

### 9. Display Anti-Patterns Warning
**Show common mistakes to avoid:**
```
⚠️ Anti-Patterns to Avoid:

DON'T:
- Apply type conversions at Bronze layer
- Filter or remove rows
- Rename columns (except metadata)

WHY:
Bronze layer is about faithful data capture.
Transformations belong in Silver layer.

Keep these in mind during implementation.
```

### 10. Summary
**Final output:**
```
✓ Pattern Applied: pattern-microsoft-pq-bronze

Summary:
- Generated output: 15 lines of Power Query M code
- Parameters used: 4 required, 1 optional (default)
- Pre-conditions: All satisfied
- Post-conditions: 5 checks to verify after implementation
- Task metadata: Updated with pattern usage

Next steps:
1. Implement the generated code
2. Verify post-conditions
3. Mark task complete when done

Pattern usage recorded in task-15.json
```

## Output Location
- Generated code/content: Displayed to user (not automatically saved)
- Updated task JSON: `.claude/tasks/task-{id}.json` (patterns field)
- Pattern usage log: Added to task notes

## Example Full Workflow

### Simple Pattern Application
```
Input: @apply-pattern.md pattern-code-python-function

Loading pattern: python-function (v1.0.0)

Required Parameters:
1. function_name
   Enter value: calculate_total

2. description
   Enter value: Calculate total from list of numbers

3. parameters
   Enter value: numbers: list[float]

4. return_type
   Enter value: float

Optional Parameters:
5. docstring_style (default: "google")
   [Enter] → Using google

Pre-Condition Checks:
✓ Function name follows naming convention
✓ Type hints are valid Python syntax

Generated output:
---
def calculate_total(numbers: list[float]) -> float:
    """Calculate total from list of numbers.

    Args:
        numbers: List of floating point numbers to sum

    Returns:
        Total sum of all numbers

    Raises:
        ValueError: If numbers list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate total of empty list")
    return sum(numbers)
---

Looks good? [Y]: Y

Post-Conditions:
□ Function has docstring
□ Type hints present for all parameters and return
□ Error handling for edge cases included

✓ Pattern applied successfully
  Task metadata updated
```

### Pattern Application with Failed Pre-Condition
```
Input: @apply-pattern.md pattern-microsoft-pq-bronze

[Parameter gathering...]

Pre-Condition Checks:
✗ Source file/connection accessible
  → File "C:\Data\missing.xlsx" not found

Resolve before applying pattern:
→ Verify source file path is correct
→ Ensure file exists and is accessible

Continue anyway? [Y/N]: N

Pattern application cancelled.
Please resolve pre-conditions and try again.
```

## Integration

### Called By
- `find-pattern.md` (after pattern selection)
- `complete-task.md` (if user chooses to apply suggested pattern)
- Manual user invocation with pattern ID

### Updates
- Task JSON file (patterns field, notes)
- Does NOT modify actual project files (user implements generated code)

## Error Handling

**Invalid pattern ID:**
```
Error: Pattern 'pattern-invalid-id' not found
Available patterns in library: {count}
Use find-pattern.md to discover patterns
```

**Missing required parameter:**
```
Error: Required parameter 'source_name' not provided
Cannot apply pattern without all required parameters
```

**Template substitution failure:**
```
Error: Template placeholder {{unknown_param}} has no corresponding parameter
Pattern file may be malformed
Please report this issue
```

## Notes
- Pattern application generates output but doesn't automatically execute it
- User always reviews generated code before use
- Post-conditions provide verification checklist
- Pattern usage tracked for error correlation and effectiveness metrics
