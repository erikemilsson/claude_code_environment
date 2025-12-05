# Error Catalog

## Overview

The Error Catalog provides systematic error tracking and learning from failures. When errors occur, they're logged with analysis and prevention strategies. Future similar tasks receive proactive warnings based on historical mistakes.

## Purpose

- **Learning**: Capture what went wrong and why
- **Prevention**: Warn before making same mistake twice
- **Analysis**: Understand common LLM error patterns
- **Improvement**: Refine patterns and processes based on real failures

## Core Concepts

### Error Entry
A structured record of a mistake, including:
- **Error details**: What happened, symptoms, error message
- **Analysis**: Root cause, why LLMs make this mistake, impact
- **Resolution**: How to fix, verification steps, time estimate
- **Prevention**: Keywords, pre-checks, patterns, warning message
- **Examples**: Wrong vs. correct approaches

### Error Categories
Organized by technology/domain:
- **Power Query**: M language errors (Bronze/Silver layer violations, type issues)
- **DAX**: Measure calculation errors (VAR pattern, context confusion)
- **Python**: Common Python mistakes (encoding, exceptions)
- **File Operations**: Claude Code tool errors (Edit without Read)
- **Git**: Version control issues
- **Task Management**: Workflow errors
- **General**: Cross-cutting concerns

### Severity Levels
- **Critical**: Blocks all work, requires rollback
- **High**: Major issues, significant time lost
- **Medium**: Workarounds exist, moderate impact
- **Low**: Minor inconvenience, easily fixed

### Recurrence Tracking
Each error tracks how many times it occurred. Higher recurrence = higher priority for prevention warnings.

## Directory Structure

```
components/error-catalog/
├── README.md                    # This file
├── catalog/
│   └── common-errors.json       # Main error catalog with all entries
└── commands/
    ├── log-error.md             # Record new errors
    └── suggest-prevention.md    # Check for similar past errors
```

## Error Entry Schema

See `catalog/common-errors.json` for full schema and examples.

**Key fields:**
```json
{
  "id": "ERR-{CATEGORY_CODE}-{NUMBER}",
  "category": "Power Query | DAX | Python | ...",
  "severity": "critical | high | medium | low",
  "recurrence_count": 0,
  "context": {
    "technology": "Specific tech",
    "operation": "What was being done",
    "difficulty_range": [min, max]
  },
  "error": {
    "title": "Short description",
    "symptoms": ["Observable symptoms"],
    "error_message": "Actual error",
    "what_went_wrong": "Plain English"
  },
  "analysis": {
    "root_cause": "Why it happened",
    "why_llm_makes_mistake": "LLM-specific reason",
    "impact": "Consequences"
  },
  "resolution": {
    "immediate_fix": "How to fix",
    "verification": "How to verify",
    "time_to_fix_minutes": 5
  },
  "prevention": {
    "keywords": ["matching", "keywords"],
    "pre_execution_check": "What to verify before",
    "pattern_to_use": "pattern-file.md",
    "warning_message": "⚠ Short warning"
  },
  "examples": [
    {
      "task_description": "Example task",
      "wrong_approach": "Don't do this",
      "correct_approach": "Do this instead"
    }
  ]
}
```

## Command Workflows

### Logging Errors

When an error occurs during task execution:
```
/log-error 42

# Interactive prompts:
What technology was involved? Power Query
What was the error message? Expression.Error: Cannot apply operator > to types Text and Date
How severe was it? High (required rollback)
What were you trying to do? Filter date column

# Command analyzes and creates entry:
✓ Error logged: ERR-PQ-003

  Category: Power Query
  Severity: high
  Prevention keywords: power query, date, filter, type

  ⚠ Type Conversion Rule: Convert date columns with Date.From() before filtering!

  This error will now trigger warnings for similar tasks.
```

### Getting Prevention Warnings

Before starting a task (automatic via pre-execution gate):
```
/complete-task 42

Step 2: Running pre-execution validation...

⚠ ERROR PREVENTION WARNINGS (2 found):

[CRITICAL] ERR-PQ-002: Silver query sources directly from file
  → ⚠ Silver Layer Rule: ALWAYS source from Bronze query!
  → Pre-check: Verify first step is Bronze reference
  → Pattern: power-query-silver.pattern.md
  (Occurred 3 times previously)

[HIGH] ERR-PQ-001: Type conversion at Bronze layer
  → ⚠ Bronze Layer Rule: NO transformations at Bronze!
  → Pre-check: Verify Bronze has zero transformations
  → Pattern: power-query-bronze.pattern.md
  (Occurred 1 time previously)

Gate passed with warnings. Proceed? [Y/n]
```

### Manual Prevention Check

Can also check manually:
```
/suggest-prevention 42

⚠ PREVENTION WARNINGS for Task 42

Based on error history, watch out for these common mistakes:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [CRITICAL] Silver query sources directly from file
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms:
  • No Bronze metadata columns in Silver
  • Silver has Source = Excel.Workbook()
  • Cannot track data lineage

Prevention:
  ⚠ Silver Layer Rule: ALWAYS source from Bronze query!

Pre-execution check:
  → Verify Silver query FIRST STEP is Bronze reference

Recommended pattern: power-query-silver.pattern.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 1 potential issue identified
```

## Integration with Other Components

### Validation Gates
- **Pre-execution gate**: Calls suggest-prevention.md automatically
- **Error warnings**: Included in gate result "info" section
- **Gate output**: Shows top 3 matching errors before task starts

### Pattern Library
- **Pattern recommendations**: Errors link to patterns that prevent them
- **Anti-patterns**: Error examples can inform pattern anti-pattern sections
- **Pattern discovery**: Frequent errors suggest new patterns needed

### Checkpoint System
- **Rollback tracking**: Log errors that required rollback
- **Checkpoint reference**: Error entries can reference checkpoint where error occurred
- **Recovery**: Link errors to checkpoints for analysis

### Task Management
- **Task notes**: Errors can be referenced in task completion notes
- **Difficulty calibration**: Error patterns inform difficulty scoring
- **Learning**: Historical errors improve future task planning

## Keyword Matching Strategy

The suggest-prevention command matches tasks to errors using keywords:

**Extraction:**
- Technology keywords from file extensions (.pq → "power query")
- Operation keywords from task description ("load", "transform", "filter")
- Domain keywords from context ("sales", "customer", "date")

**Scoring:**
```
Base score:
  - Keyword match in error.prevention.keywords: +1
  - Category match: +2

Severity multiplier:
  - Critical: ×4
  - High: ×3
  - Medium: ×2
  - Low: ×1

Recurrence bonus:
  - +recurrence_count points

Final score = (base_score × severity_multiplier) + recurrence_count
```

**Example:**
```
Task: "Create Silver layer for sales data"
Keywords: ["silver", "sales", "data", "power query"]

Error ERR-PQ-002:
  Keywords: ["power query", "silver", "bronze reference"]
  Matches: "silver" (+1), "power query" (+1) = 2
  Severity: critical (×4) = 8
  Recurrence: 3 = +3
  Final: 11

Top match! Show this warning.
```

## Seed Errors

The catalog starts with 6 common errors:

1. **ERR-PQ-001**: Bronze type conversion (violates medallion architecture)
2. **ERR-PQ-002**: Silver direct source (should reference Bronze)
3. **ERR-DAX-001**: Missing VAR pattern (performance and debugging)
4. **ERR-DAX-002**: Measure in row context (context confusion)
5. **ERR-GEN-001**: Edit without Read (tool requirement)
6. **ERR-PY-001**: Missing encoding (UnicodeDecodeError)

These represent actual LLM failure patterns observed across domains.

## Best Practices

### When to Log Errors

**Always:**
- Error required rollback to checkpoint
- Error blocked task completion
- Error took >10 minutes to diagnose and fix

**Consider:**
- First occurrence of new error type
- Error with subtle root cause (worth documenting)
- Error that could be prevented with pattern

**Skip:**
- Simple typos (not systematic errors)
- One-off environmental issues
- User-caused errors (not LLM mistakes)

### Writing Good Error Entries

**Do:**
- Write clear, actionable warning messages
- Include specific symptoms (observable behaviors)
- Explain why LLMs specifically make this mistake
- Provide concrete examples (wrong vs. right)
- Link to applicable patterns
- Use precise keywords for matching

**Don't:**
- Write vague descriptions ("something went wrong")
- Skip root cause analysis
- Omit prevention strategies
- Use jargon without explanation
- Duplicate existing errors (update recurrence instead)

### Managing the Catalog

**Review periodically:**
- Check for duplicate entries (consolidate)
- Update prevention strategies as patterns evolve
- Remove obsolete errors (technology changes)
- Analyze recurrence patterns (what keeps happening?)

**Statistics:**
```json
{
  "total_errors": 6,
  "by_category": {
    "Power Query": 2,
    "DAX": 2,
    "File Operations": 1,
    "Python": 1
  },
  "by_severity": {
    "critical": 3,
    "high": 2,
    "medium": 1,
    "low": 0
  }
}
```

## Error ID Format

**Pattern:** `ERR-{CATEGORY_CODE}-{NUMBER}`

**Category codes:**
- `PQ`: Power Query
- `DAX`: DAX
- `PY`: Python
- `GO`: Git Operations
- `FO`: File Operations
- `TM`: Task Management
- `GEN`: General

**Numbering:**
- Sequential within category (001, 002, 003...)
- Leading zeros for sorting (ERR-PQ-003, not ERR-PQ-3)
- Check for highest existing before assigning new

**Examples:**
- `ERR-PQ-001`: First Power Query error
- `ERR-DAX-002`: Second DAX error
- `ERR-GEN-001`: First General error

## Prevention Workflow

```
1. Task created
   ↓
2. User runs /complete-task
   ↓
3. Pre-execution gate runs
   ↓
4. suggest-prevention.md called
   ↓
5. Task keywords extracted
   ↓
6. Error catalog searched
   ↓
7. Top matches scored and ranked
   ↓
8. Warnings displayed in gate results
   ↓
9. User sees warnings BEFORE starting
   ↓
10. User applies prevention strategies
   ↓
11. Error avoided! (or if error occurs, log it)
```

## Learning Loop

The error catalog creates a continuous improvement cycle:

```
Error Occurs
    ↓
Log Error (analyze root cause)
    ↓
Extract Prevention Strategy
    ↓
Add to Catalog with Keywords
    ↓
Suggest Prevention (future tasks)
    ↓
Error Avoided (or recurrence logged)
    ↓
Update Recurrence Count
    ↓
Higher Priority Warning
    ↓
Even Fewer Future Errors
```

## Advanced Features

### Recurrence Analysis
Track which errors keep happening:
```
Top recurring errors:
1. ERR-PQ-002 (Silver direct source): 5 times
2. ERR-DAX-001 (No VAR pattern): 3 times
3. ERR-PY-001 (Missing encoding): 2 times

Action: Enhance patterns for top recurring errors
```

### Error Relationships
Some errors occur together:
```
If ERR-PQ-002 occurs:
  Often followed by ERR-PQ-003 (type issues)

Prevention: Fix root cause (Silver sourcing) prevents cascade
```

### Confidence Levels
Show prediction confidence:
```
[CRITICAL] ERR-PQ-002 (Confidence: HIGH)
  Score: 11 | Recurred 5 times | Strong keyword match

[MEDIUM] ERR-PY-001 (Confidence: LOW)
  Score: 3 | Recurred 0 times | Weak keyword match
```

### Pattern Suggestions
Errors identify missing patterns:
```
Errors ERR-PQ-003, ERR-PQ-004, ERR-PQ-005 all relate to date handling.

Suggestion: Create power-query-date-handling.pattern.md
```

## Reporting

### Error Statistics
```
Error Catalog Statistics:
  Total errors: 6
  Critical: 3 (50%)
  High: 2 (33%)
  Medium: 1 (17%)

  Most common category: Power Query (2 errors)
  Highest recurrence: ERR-PQ-002 (5 times)

  Total prevented: ~15 errors (estimated from recurrence)
```

### Prevention Effectiveness
```
Task 42: 2 warnings shown
Result: No errors occurred ✓

Task 43: 1 warning shown
Result: Error ERR-PQ-002 occurred despite warning ✗
  → Update prevention strategy for better clarity

Overall effectiveness: 50% (1/2 prevented)
```

## Examples

### Example 1: First Error in New Category
```
# Bronze layer error occurs
/log-error 28

Technology: Power Query
Message: Expression.Error: Type mismatch in Silver
Severity: High

# Analysis determines:
Root cause: Applied transformations at Bronze
Category: Power Query
New error ID: ERR-PQ-001 (first in PQ category)

✓ Error logged with prevention strategy
```

### Example 2: Duplicate Error (Recurrence)
```
# Same error happens again
/log-error 35

Technology: Power Query
Message: Expression.Error: Type mismatch in Silver

# Command detects similarity:
Found existing error: ERR-PQ-001
Incrementing recurrence_count: 0 → 1
Updating last_occurred timestamp

✓ Error updated (now recurred 1 time)
```

### Example 3: Prevention Success
```
# Later task with similar keywords
/complete-task 42

Pre-execution gate:

⚠ ERROR PREVENTION:
  [HIGH] ERR-PQ-001: Bronze transformations
  (Occurred 1 time previously)

  → Pre-check: Verify Bronze has ZERO transformations

# User heeds warning, checks Bronze query
# No transformations found ✓
# Proceeds successfully, error avoided!
```

## See Also

- **Validation Gates**: Pre/post-execution validation (uses error prevention)
- **Pattern Library**: Reusable patterns (linked from error entries)
- **Checkpoint System**: State snapshots (referenced when errors require rollback)
- **Task Management**: Task lifecycle (errors inform difficulty scoring)
