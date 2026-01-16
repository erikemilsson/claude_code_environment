# Suggest Prevention Command

## Purpose
Check error catalog before starting tasks to proactively warn about common mistakes.

## Context Required
- Task ID to check
- Task description and title (for keyword extraction)
- Optional: files_affected (for technology detection)

## Process

### 1. Load Task Information
Read task JSON file:
```
- Extract: title, description, difficulty
- Extract: files_affected (for file type detection)
- Combine into searchable text
```

### 2. Extract Task Keywords
Identify relevant keywords from task:

**Technology keywords:**
- File extensions: .pq → "power query", .dax → "dax", .py → "python"
- Explicit mentions: "Power Query", "DAX", "pandas", "Git"
- Implied: "measure" → "dax", "query" → "power query"

**Operation keywords:**
- Actions: "load", "transform", "filter", "create", "modify"
- Layers: "bronze", "silver", "gold", "medallion"
- Data types: "csv", "excel", "json", "date"

**Domain keywords:**
- Business terms: "sales", "revenue", "customer"
- Technical terms: "encoding", "var", "iterator"

**Algorithm:**
```
1. Convert task title + description to lowercase
2. Split into words
3. Remove stop words (the, a, an, is, etc.)
4. Extract significant terms (nouns, verbs, technical terms)
5. Include file extensions from files_affected
6. Return 5-15 keywords
```

**Example:**
```
Task: "Create Silver layer query for sales data with date filtering"
Keywords: ["silver", "query", "sales", "data", "date", "filter", "power query"]
```

### 3. Search Error Catalog
Load `common-errors.json` and search:
```
For each error in catalog:
  Calculate match score:
    - For each task keyword:
      - If keyword in error.prevention.keywords: +1 point
      - If keyword matches category (case-insensitive): +2 points
    - Multiply base score by severity weight:
      - critical: ×4
      - high: ×3
      - medium: ×2
      - low: ×1
    - Add recurrence bonus: +recurrence_count points

  If match score > 0:
    Add to matches with score
```

**Scoring example:**
```
Error: ERR-PQ-002 (Silver sources directly from file)
Task keywords: ["silver", "query", "sales", "filter"]
Prevention keywords: ["power query", "silver", "medallion", "transformation", "bronze reference"]

Matches:
- "silver" in prevention.keywords: +1
- "query" implied in "power query": +1
Base score: 2
Severity: critical (×4): 2 × 4 = 8
Recurrence: 3: +3
Final score: 11
```

### 4. Rank Matches
Sort errors by score (highest first):
```
1. ERR-PQ-002: score 11 (Silver direct source - critical)
2. ERR-PQ-001: score 9 (Bronze transformations - high)
3. ERR-DAX-001: score 4 (VAR pattern - high)
```

### 5. Display Top Warnings
Show top 3 matches (if any):

**Format:**
```
⚠ PREVENTION WARNINGS for Task {id}

Based on error history, watch out for these common mistakes:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [CRITICAL] Silver query sources directly from file
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms:
  • No Bronze metadata columns (_LoadTimestamp, _SourceFile) in Silver
  • Silver query has Source = Excel.Workbook() or Csv.Document()
  • Cannot track data lineage

Prevention:
  ⚠ Silver Layer Rule: ALWAYS source from Bronze query! Never connect
  directly to files. First line must be: Source = BronzeQueryName

Pre-execution check:
  → Verify Silver query FIRST STEP is Bronze query reference, NOT file source

Recommended pattern: power-query-silver.pattern.md

This error occurred 3 times previously (last: 2025-11-28)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. [HIGH] Type conversion at Bronze layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms:
  • Type errors in downstream Silver queries
  • Unable to reprocess raw data
  • Bronze table has typed columns instead of raw data

Prevention:
  ⚠ Bronze Layer Rule: NO transformations at Bronze! Only add metadata
  (_LoadTimestamp, _SourceFile). All type conversions go in Silver.

Pre-execution check:
  → Verify Bronze query has ZERO transformations

Recommended pattern: power-query-bronze.pattern.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 2 potential issues identified
Review these warnings before proceeding with task execution.
```

### 6. Return Structured Data
For integration with pre-execution gate:
```json
{
  "suggestions": [
    {
      "error_id": "ERR-PQ-002",
      "severity": "critical",
      "match_score": 11,
      "title": "Silver query sources directly from file",
      "warning_message": "⚠ Silver Layer Rule: ALWAYS source from Bronze query!...",
      "pre_execution_check": "Verify Silver query FIRST STEP is Bronze query reference",
      "pattern": "power-query-silver.pattern.md",
      "recurrence_count": 3
    },
    {
      "error_id": "ERR-PQ-001",
      "severity": "high",
      "match_score": 9,
      "title": "Type conversion at Bronze layer",
      "warning_message": "⚠ Bronze Layer Rule: NO transformations at Bronze!...",
      "pre_execution_check": "Verify Bronze query has ZERO transformations",
      "pattern": "power-query-bronze.pattern.md",
      "recurrence_count": 1
    }
  ],
  "total_matches": 2,
  "task_keywords": ["silver", "query", "sales", "filter", "power query"]
}
```

## Output Location
- Console display (no file modifications)
- Structured JSON for integration with pre-execution gate

## Display Modes

### Detailed Mode (Default)
Full warnings with symptoms, prevention, checks (shown above)

### Summary Mode (--summary)
```
⚠ PREVENTION WARNINGS (2 found):
  [CRITICAL] ERR-PQ-002: Silver direct source (score: 11)
  [HIGH]     ERR-PQ-001: Bronze transformations (score: 9)

Use suggest-prevention {task_id} for details.
```

### Compact Mode (--compact)
```
⚠ Watch: Silver direct source, Bronze transformations
```

## Critical Rules
- Always show warnings in severity order (critical first)
- Limit to top 3 matches (avoid overwhelming)
- Only show matches with score > 0
- Include recurrence count (shows learning from history)
- Link to patterns when available

## Keyword Matching Strategy

### Direct Matches (Exact)
```
Task keyword: "bronze"
Error keyword: "bronze"
Result: MATCH (+1 point)
```

### Partial Matches (Substring)
```
Task keyword: "query"
Error keyword: "power query"
Result: MATCH (+1 point)
```

### Semantic Matches (Technology Detection)
```
File: sales-bronze.pq
Detected: "power query"
Error keywords: ["power query", "bronze"]
Result: MATCH (+2 points for category, +1 for bronze)
```

### Stop Words
Ignore common words that don't indicate error relevance:
```
Ignore: "the", "a", "an", "is", "are", "and", "or", "with", "for", "to", "from"
Keep: "bronze", "silver", "dax", "var", "encoding", "filter", "date"
```

## Integration Points
- Called by pre-execution gate automatically
- Can be called manually before starting work
- Results included in gate result "info" section
- Used to enhance pattern suggestions

## Error Handling
- If common-errors.json missing: Return "No error history available"
- If no matches: Return "No similar errors in history"
- If task keywords empty: Use title only or return "Insufficient task information"
- If catalog malformed: Skip invalid entries, process valid ones

## Advanced Features

### Machine Learning Enhancement
Track prediction accuracy:
```
For each task:
  - Suggestions made: [ERR-PQ-002, ERR-PQ-001]
  - Actual errors: [ERR-PQ-002]
  - Hit rate: 50% (1/2 suggestions were relevant)

Use hit rate to refine keyword extraction and scoring algorithm.
```

### Context-Aware Ranking
Boost scores based on task context:
```
If task difficulty ≥ 7:
  Boost "critical" errors by additional ×1.5

If task has checkpoint in files_affected:
  Boost errors that previously required rollback

If task modifies >5 files:
  Boost errors related to bulk operations
```

### Related Errors
Show error relationships:
```
Primary warning: ERR-PQ-002 (Silver direct source)
Related errors often occur together:
  → ERR-PQ-001 (Bronze transformations)
  → ERR-PQ-003 (Date type conversion)

If you encounter primary, check for related errors too.
```

### Confidence Level
Show prediction confidence:
```
⚠ [CRITICAL] Silver direct source (Confidence: HIGH)
   Match score: 11 | Recurred 3 times | Strong keyword overlap

⚠ [MEDIUM] Missing encoding (Confidence: LOW)
   Match score: 3 | Recurred 0 times | Weak keyword overlap
```

## Example Workflows

### Scenario 1: High Match Score
```
Task 42: "Create Silver layer for sales data with date filtering"

/suggest-prevention 42

⚠ PREVENTION WARNINGS (3 found)

[CRITICAL] Silver query sources directly from file
  → Pre-check: Verify first step is Bronze reference

[HIGH] Bronze transformations
  → Pre-check: Verify Bronze has zero transformations

[HIGH] Date comparison without type conversion
  → Pre-check: Verify Date.From() used before filtering

Review warnings before starting task.
```

### Scenario 2: No Matches
```
Task 15: "Update README documentation"

/suggest-prevention 15

✓ No similar errors in history for this task type

Proceed with confidence, but consider creating checkpoint before starting.
```

### Scenario 3: Integration with Pre-Execution Gate
```
/complete-task 42

Step 2: Running pre-execution validation...

⚠ Pre-execution Gate Results:
  Status Check: ✓ Pass
  Dependency Check: ✓ Pass
  Difficulty Check: ✓ Pass
  Context Check: ⚠ Warning (1 file doesn't exist yet)
  Error Prevention: ⚠ 2 warnings

  Error Prevention Warnings:
    [CRITICAL] ERR-PQ-002: Silver direct source
    [HIGH] ERR-PQ-001: Bronze transformations

Gate passed with warnings. Proceed? [Y/n]
```

## See Also

- **Log Error Command**: Records new errors to catalog
- **Common Errors Catalog**: Source of prevention data
- **Pre-Execution Gate**: Uses suggestions to warn before tasks
- **Pattern Library**: Recommended patterns to prevent errors
