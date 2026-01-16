# Command: Find Pattern

## Purpose
Search pattern library for patterns matching task description or keywords. Returns scored matches to help select the best pattern for a task.

## Context Required
- `components/pattern-library/patterns/` (all pattern files)
- Task description or keywords to match against
- Optional: Task JSON file (for difficulty matching)

## Process

### 1. Extract Keywords
**From task title and description**, extract:
- **Technology names**: Python, Power Query, DAX, Excel, CSV, JSON, etc.
- **Action verbs**: create, modify, transform, load, parse, generate, etc.
- **Domain terms**: bronze, silver, measure, function, class, test, etc.
- **File types**: Mentioned extensions (.py, .m, .csv, .json, etc.)

**Normalization:**
- Convert to lowercase
- Remove common words (the, a, an, for, with, etc.)
- Stem similar terms (creating → create, loading → load)

### 2. Load All Patterns
**Scan pattern directories:**
```
components/pattern-library/patterns/
├── file-operations/*.pattern.md
├── code-generation/*.pattern.md
├── data-operations/*.pattern.md
└── microsoft-stack/*.pattern.md
```

**For each pattern file:**
- Read pattern metadata section
- Extract:
  - Pattern ID
  - Triggers (keyword list)
  - File types
  - Difficulty range
  - Category

### 3. Score Patterns
**For each pattern**, calculate match score:

#### Trigger Keyword Matching (3 points each)
- Compare task keywords against pattern triggers
- Case-insensitive matching
- Partial matches count (e.g., "bronze" matches "bronze layer")
- **Score += 3** for each trigger keyword that matches

#### File Type Matching (2 points each)
- Compare mentioned/affected file types against pattern file types
- Exact extension match (.py, .m, .csv, etc.)
- **Score += 2** for each file type match

#### Difficulty Range Matching (1 point)
- If task difficulty provided
- Check if difficulty falls within pattern's difficulty range
- **Score += 1** if in range

**Example Scoring:**
```
Task: "Create Bronze layer query for sales Excel file"
Difficulty: 4
Keywords: [bronze, layer, query, excel, sales, create]
File types: [.xlsx]

Pattern: power-query-bronze
- Triggers: ["bronze layer" ✓, "load raw data" ✗, "initial data load" ✗]
  → 1 match × 3 = 3 points
- File types: [.m, .pq]
  → 0 matches × 2 = 0 points
- Difficulty: range 3-5, task 4
  → In range × 1 = 1 point
Total: 4 points (Medium confidence)
```

### 4. Rank Results
**Sort patterns by score (highest first)**

**Filter by confidence:**
- **Score >= 6**: High confidence match
- **Score 3-5**: Medium confidence match
- **Score < 3**: Low confidence, don't suggest

**Limit results:**
- Show top 3 matches maximum
- Only show medium+ confidence matches

### 5. Present Results
**Display format:**

```
Pattern matches for: "{task description}"

🟢 High Confidence (Score 6+)
1. pattern-microsoft-pq-bronze (Score: 9) - RECOMMENDED
   Category: microsoft-stack
   Triggers matched: "bronze layer", "load raw data", "excel"
   Difficulty: 3-5 (task: 4)
   Description: Bronze layer data loading with metadata columns

🟡 Medium Confidence (Score 3-5)
2. pattern-data-excel-read (Score: 5)
   Category: data-operations
   Triggers matched: "excel", "read"
   Difficulty: 3-5 (task: 4)
   Description: Excel file reading with pandas and error handling

3. pattern-file-create (Score: 3)
   Category: file-operations
   Triggers matched: "create"
   Difficulty: 1-3 (task: 4 - outside range)
   Description: Create new file with proper headers

---
Recommended action:
→ Use pattern-microsoft-pq-bronze (highest score, difficulty match)

Apply this pattern? [Y/N]
```

### 6. User Interaction
**Options:**
1. **Y**: Proceed to apply-pattern.md with selected pattern
2. **N**: Show next match or exit
3. **[number]**: Select specific pattern from list
4. **details**: Show full pattern details for a specific pattern

### 7. Return Selected Pattern
- Return pattern ID for use by apply-pattern.md or complete-task.md
- If no patterns match (all < 3 score): "No applicable patterns found"

## Output
- List of matching patterns with scores
- Recommendation for best match
- Selected pattern ID (if user chooses one)

## Example Usage

### High Confidence Match
```
User: @find-pattern.md
Prompt: Enter task description or keywords
Input: Create Bronze layer query for sales Excel file

[Processing...]

Pattern matches for: "Create Bronze layer query for sales Excel file"

🟢 High Confidence
1. pattern-microsoft-pq-bronze (Score: 9) - RECOMMENDED
   Matched: "bronze layer", "load", "excel"
   Perfect difficulty match (3-5)

Apply pattern-microsoft-pq-bronze? [Y/N]
> Y

✓ Pattern selected: pattern-microsoft-pq-bronze
  Next: Use apply-pattern.md to execute with parameters
```

### No Good Matches
```
Input: Refactor legacy monolith to microservices

[Processing...]

No high or medium confidence patterns found.

This task may require custom implementation.
Consider:
- Breaking down into smaller tasks (difficulty likely ≥7)
- Creating a new pattern if this becomes recurring
```

### Multiple Medium Matches
```
Input: Parse JSON configuration file

[Processing...]

Pattern matches for: "Parse JSON configuration file"

🟡 Medium Confidence
1. pattern-data-json-parse (Score: 5)
   Matched: "json", "parse"

2. pattern-file-operations-read (Score: 4)
   Matched: "file", "read"

3. pattern-code-python-function (Score: 3)
   Matched: "function" (inferred from "parse")

Select pattern [1-3] or N to skip:
> 1

✓ Pattern selected: pattern-data-json-parse
```

## Integration

### Called By
- `components/validation-gates/gates/pre-execution.md` (automatic suggestion)
- `components/task-management/commands/complete-task.md` (user prompt)
- Manual user invocation

### Calls
- None (reads pattern files directly)

### Outputs To
- `apply-pattern.md` (passes selected pattern ID)
- User display (pattern suggestions)

## Algorithm Tuning

### Keyword Extraction Improvements
- Add domain-specific term recognition
- Use task history to learn keyword patterns
- Weight keywords by position (title > description)

### Scoring Refinements
- **Adjust weights**: Currently 3:2:1 (trigger:file:difficulty)
- **Add negative scoring**: Anti-trigger keywords that reduce score
- **Consider pattern usage history**: Boost frequently successful patterns

### Confidence Thresholds
- **High**: >= 6 (current)
- **Medium**: 3-5 (current)
- Can be adjusted based on pattern library size and accuracy

## Notes
- Pattern matching is fuzzy, not exact
- Multiple patterns can apply to same task
- User always has final choice
- Pattern application is optional, never forced
