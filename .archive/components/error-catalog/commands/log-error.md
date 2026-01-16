# Log Error Command

## Purpose
Record errors during task execution for future prevention and learning.

## Context Required
- Task ID where error occurred
- Error details (message, symptoms, context)
- What was attempted (operation, approach)
- Optional: checkpoint ID if rollback was needed

## Process

### 1. Gather Error Information
Collect details from current situation:
```
Error occurred during task: {task_id}
Task title: {title}
Operation being performed: {description}

Please describe the error:
- What error message appeared?
- What symptoms did you observe?
- What were you trying to do?
- What approach did you take?
```

**Minimum required information:**
- Error message or behavior
- What operation was being performed
- Technology/tool involved

### 2. Analyze and Categorize Error

**Determine category:**
- Analyze technology involved (Power Query, DAX, Python, Git, etc.)
- Match to existing categories in common-errors.json
- Create new category if needed

**Determine severity:**
- **Critical**: Blocks all progress, requires rollback
- **High**: Major issues, significant time lost
- **Medium**: Workarounds exist, moderate impact
- **Low**: Minor inconvenience, easily fixed

**Analyze root cause:**
```
Ask questions to identify:
- Why did this error occur?
- Why might an LLM specifically make this mistake?
- What was the underlying misunderstanding?
- What principle or rule was violated?
```

### 3. Extract Prevention Strategy

**Identify keywords:**
Extract from task description and error context:
- Technology names (e.g., "power query", "dax", "pandas")
- Operation types (e.g., "bronze", "transform", "csv")
- File types (e.g., "excel", "json")
- Concepts (e.g., "encoding", "var pattern", "medallion")

**Determine pre-execution check:**
What should be verified BEFORE starting similar tasks?
```
Example: "Verify Bronze query has ZERO transformations"
Example: "Verify all file operations have encoding parameter"
```

**Link to pattern:**
Which pattern file would prevent this error?
```
Search pattern library for matching pattern
If none exists, note: "Consider creating pattern for this"
```

**Create warning message:**
Short, actionable warning (1-2 sentences)
```
Format: "⚠ {Rule Name}: {What to do/avoid}. {Why it matters}."
Example: "⚠ Bronze Layer Rule: NO transformations at Bronze! All type conversions go in Silver layer."
```

### 4. Check for Duplicate
Search existing errors for similar issues:
```
- Load components/error-catalog/catalog/common-errors.json
- Check for errors with similar:
  - Category
  - Keywords
  - Error message patterns
  - Root cause
```

**If duplicate found:**
- Increment `recurrence_count`
- Update `last_occurred` timestamp
- Add to examples if new variation
- Report: "Similar error ERR-XX-YY found, updated recurrence count"

**If new error:**
- Generate new ID
- Continue to step 5

### 5. Generate Error ID
Create unique identifier:
```
Format: ERR-{CATEGORY_CODE}-{NUMBER}

Category codes:
- PQ: Power Query
- DAX: DAX
- PY: Python
- GO: Git Operations
- FO: File Operations
- TM: Task Management
- GEN: General

Number: Next available in category (001, 002, 003...)
```

**Algorithm:**
```
1. Load common-errors.json
2. Find all errors in same category
3. Extract highest number
4. Increment by 1 (or use 001 if first in category)
5. Format as ERR-{CODE}-{NUMBER:03d}
```

Example: If ERR-PQ-002 exists, next is ERR-PQ-003

### 6. Create Error Entry
Build complete error object following schema:
```json
{
  "id": "ERR-PQ-003",
  "category": "Power Query",
  "severity": "high",
  "recurrence_count": 1,
  "context": {
    "technology": "Power Query (M language)",
    "operation": "Date filtering",
    "difficulty_range": [4, 6]
  },
  "error": {
    "title": "Date comparison with text column causes type error",
    "symptoms": [
      "Expression.Error: We cannot apply operator > to types Text and Date",
      "Filter step fails",
      "Query returns no rows unexpectedly"
    ],
    "error_message": "Expression.Error: We cannot apply operator > to types Text and Date",
    "what_went_wrong": "Attempted to filter date column without first converting from Text type"
  },
  "analysis": {
    "root_cause": "Assumed Excel date import automatically converts to Date type, but Bronze preserves as Text",
    "why_llm_makes_mistake": "Natural assumption that dates are Date type, forgetting Bronze layer preserves raw types",
    "impact": "Filter fails, query breaks, must rollback and fix type conversion"
  },
  "resolution": {
    "immediate_fix": "Add Date.From() conversion before filtering: Date.From([DateColumn]) > #date(2024,1,1)",
    "verification": "Filter step executes without error, returns expected rows",
    "time_to_fix_minutes": 5
  },
  "prevention": {
    "keywords": ["power query", "date", "filter", "type", "comparison"],
    "pre_execution_check": "Verify date columns converted to Date type before comparisons",
    "pattern_to_use": "power-query-silver.pattern.md",
    "warning_message": "⚠ Type Conversion Rule: Convert date columns with Date.From() before filtering or comparing!"
  },
  "examples": [
    {
      "task_description": "Filter sales data for dates after 2024-01-01",
      "wrong_approach": "Table.SelectRows(Source, each [OrderDate] > #date(2024,1,1))",
      "correct_approach": "Table.SelectRows(Source, each Date.From([OrderDate]) > #date(2024,1,1))"
    }
  ],
  "last_occurred": "2025-12-05T14:30:00Z",
  "created_date": "2025-12-05",
  "updated_date": "2025-12-05"
}
```

### 7. Add to Common Errors Catalog
Update common-errors.json:
```
1. Load file
2. Append new error to "errors" array
3. Update statistics:
   - Increment total_errors
   - Update by_category count
   - Update by_severity count
4. Write file (preserve formatting)
```

### 8. Check for Pattern Updates
Determine if existing patterns need enhancement:
```
If pattern_to_use exists:
  - Note: "Pattern {name} could be enhanced with this error's prevention"
  - Add to pattern's anti-patterns section (manual task)

If no pattern exists:
  - Note: "Consider creating new pattern for {operation}"
  - Add suggestion to pattern library backlog
```

### 9. Report Logged Error
Display summary:
```
✓ Error logged: ERR-PQ-003

  Category: Power Query
  Severity: high
  Recurrence: First occurrence

  Prevention keywords: power query, date, filter, type, comparison
  Pattern suggested: power-query-silver.pattern.md

  Warning message:
  ⚠ Type Conversion Rule: Convert date columns with Date.From() before filtering or comparing!

  This error will now trigger warnings for similar tasks in pre-execution gate.

  To review all errors: cat components/error-catalog/catalog/common-errors.json
  To see prevention suggestions: Use complete-task command (pre-execution gate)
```

## Output Location
- Updated `components/error-catalog/catalog/common-errors.json`
- No task JSON changes (error logged separately)

## Critical Rules
- Always get error message and context (required fields)
- Generate unique IDs (check for duplicates first)
- Extract meaningful keywords (3-8 keywords minimum)
- Write actionable warning messages
- Increment recurrence_count for duplicates
- Update statistics section

## Integration Points
- Called manually when errors occur during task execution
- Can be called from post-execution gate if failures detected
- Prevention data used by suggest-prevention.md command
- Referenced by pre-execution gate to show warnings

## Error Handling
- If common-errors.json missing: Create new file with schema
- If duplicate error: Update existing entry instead of creating new
- If category code unknown: Use GEN (General)
- If cannot determine severity: Default to medium

## Advanced Features

### Interactive Mode
Guide user through error entry:
```
log-error 42

Error Logging for Task 42: Integrate payment API

1. What technology was involved?
   [1] Power Query
   [2] DAX
   [3] Python
   [4] Other: ___

2. What was the error message?
   > Expression.Error: Cannot convert...

3. How severe was the impact?
   [1] Critical (blocked all work)
   [2] High (major issues)
   [3] Medium (workaround exists)
   [4] Low (minor)

4. What were you trying to do?
   > Filter date column for recent records

[Continues gathering information...]

✓ Error logged: ERR-PQ-003
```

### Auto-Analysis Mode
Analyze from checkpoint diff:
```
log-error 42 --from-checkpoint chk-42-2

Analyzing changes from checkpoint...
- Modified: src/queries/sales-silver.pq
- Error occurred in: Table.SelectRows step

Detected pattern: Date comparison without type conversion

Suggest logging as:
  Category: Power Query
  Root cause: Missing Date.From() conversion

Confirm? [Y/n]
```

### Link to Task Notes
Add error reference to task JSON:
```
Update task 42 notes:
"Task completed with error ERR-PQ-003 (date type conversion). See error catalog for details."

This creates bidirectional link:
- Error entry → task where it occurred
- Task notes → error entry for reference
```

## Example Workflow

### Scenario: Error During Task Execution
```
# Working on task 42, error occurs
> Error: Expression.Error: We cannot apply operator > to types Text and Date

# Log the error
/log-error 42

# Interactive prompts gather info
> Technology: Power Query
> Error message: Expression.Error: We cannot apply operator > to types Text and Date
> Severity: High (required rollback to checkpoint)
> Operation: Filtering date column

# Command analyzes and creates entry
✓ Error logged: ERR-PQ-003

# Fix the issue
/rollback-to chk-42-1
# Implement correct approach with Date.From()

# Complete task successfully
/complete-task 42

# Future similar tasks will get warning from pre-execution gate:
# "⚠ Type Conversion Rule: Convert date columns with Date.From() before filtering!"
```

## See Also

- **Common Errors Catalog**: `components/error-catalog/catalog/common-errors.json`
- **Suggest Prevention Command**: Uses logged errors to warn before tasks
- **Checkpoint System**: Provides rollback when errors occur
- **Validation Gates**: Displays error prevention warnings
