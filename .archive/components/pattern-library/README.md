# Pattern Library Component

## Overview

The Pattern Library component provides reusable, pre-validated execution patterns to reduce LLM improvisation and prevent common errors. Most mistakes come from the LLM "figuring it out" - patterns provide proven paths.

## Purpose

**Reduce errors through standardization.** Pre-validated patterns ensure:
- Consistent approach to common tasks
- Reduced improvisation and experimentation
- Captured best practices and anti-patterns
- Faster task execution with templates

## Component Structure

```
components/pattern-library/
├── README.md                          # This file
├── patterns/
│   ├── file-operations/               # File system operations
│   │   ├── create-file.pattern.md
│   │   ├── modify-file.pattern.md
│   │   └── bulk-rename.pattern.md
│   ├── code-generation/               # Code creation patterns
│   │   ├── python-function.pattern.md
│   │   ├── python-class.pattern.md
│   │   └── test-file.pattern.md
│   ├── data-operations/               # Data processing
│   │   ├── csv-transform.pattern.md
│   │   ├── json-parse.pattern.md
│   │   └── excel-read.pattern.md
│   └── microsoft-stack/               # Microsoft technologies
│       ├── power-query-bronze.pattern.md
│       ├── power-query-silver.pattern.md
│       ├── dax-measure.pattern.md
│       └── dataflow-gen2.pattern.md
└── commands/
    ├── find-pattern.md                # Search for applicable patterns
    └── apply-pattern.md               # Execute pattern with parameters
```

## Pattern Format Specification

Every `.pattern.md` file follows this standard structure:

### Required Sections

#### 1. Header
```markdown
# Pattern: [Name]
```

#### 2. Metadata
```markdown
## Metadata
- **ID**: pattern-[category]-[name]
- **Version**: X.Y.Z
- **Category**: file-operations|code-generation|data-operations|microsoft-stack
- **Difficulty Range**: [1-3|3-5|5-7|7-10] (tasks this pattern suits)
```

#### 3. Triggers
```markdown
## Triggers
Keywords that suggest this pattern applies:
- keyword1
- keyword2
- keyword3

File types: [.ext, .ext2]
```

#### 4. Parameters
```markdown
## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | yes | What it does |
| param2 | number | no | Optional param |
```

#### 5. Pre-Conditions
```markdown
## Pre-Conditions
- [ ] Condition 1 that must be true before applying pattern
- [ ] Condition 2 that must be true
```

#### 6. Template
```markdown
## Template

```[language]
# Template with {{parameter}} placeholders
{{param1}}
{{param2}}
```
```

#### 7. Post-Conditions
```markdown
## Post-Conditions
- [ ] What should be true after execution
- [ ] What to verify
```

#### 8. Anti-Patterns
```markdown
## Anti-Patterns
**DON'T do this:**
- Common mistake 1
- Common mistake 2

**WHY**: Explanation of why these are mistakes
```

#### 9. Examples
```markdown
## Examples

### Example 1: [Scenario]
**Input:**
```
param1: value1
param2: value2
```
**Output:**
```
[Expected result]
```
```

## Pattern Categories

### File Operations
**Purpose:** Safe, consistent file system operations

**Patterns:**
- `create-file.pattern.md` - Create new files with proper headers
- `modify-file.pattern.md` - Edit existing files safely
- `bulk-rename.pattern.md` - Rename multiple files systematically

### Code Generation
**Purpose:** Generate code with proper structure and conventions

**Patterns:**
- `python-function.pattern.md` - Functions with docstrings and type hints
- `python-class.pattern.md` - Classes with proper initialization
- `test-file.pattern.md` - Test files with proper structure

### Data Operations
**Purpose:** Handle data processing with error handling

**Patterns:**
- `csv-transform.pattern.md` - CSV reading and transformation
- `json-parse.pattern.md` - JSON parsing with validation
- `excel-read.pattern.md` - Excel file reading with pandas

### Microsoft Stack
**Purpose:** Microsoft-specific technologies and best practices

**Patterns:**
- `power-query-bronze.pattern.md` - Bronze layer data loading
- `power-query-silver.pattern.md` - Silver layer transformations
- `dax-measure.pattern.md` - DAX measure creation
- `dataflow-gen2.pattern.md` - Fabric Dataflow Gen2 patterns

## Using Patterns

### 1. Find Patterns (Automatic)
When you use `complete-task.md`, the pre-execution gate automatically:
1. Extracts keywords from task title and description
2. Scores patterns by trigger matches and difficulty range
3. Suggests top matches: "Pattern available: {pattern_name}"

### 2. Find Patterns (Manual)
Use the find-pattern command:
```
@components/pattern-library/commands/find-pattern.md
```

**Process:**
- Enter task keywords or description
- Review scored matches (6+ = high confidence)
- Select pattern to apply

### 3. Apply Pattern
Once pattern is selected:
```
@components/pattern-library/commands/apply-pattern.md {pattern_id}
```

**Process:**
1. Load pattern template
2. Gather required parameters
3. Verify pre-conditions
4. Apply template with parameter substitution
5. Verify post-conditions
6. Record pattern use in task metadata

## Pattern Matching Algorithm

**Scoring System:**
- Trigger keyword match: **3 points** per keyword
- File type match: **2 points** per type
- Difficulty in range: **1 point**

**Confidence Levels:**
- **High (6+)**: Strongly recommended
- **Medium (3-5)**: Consider using
- **Low (<3)**: Not suggested

**Example:**
```
Task: "Create Bronze layer query for sales Excel file"
Keywords extracted: Bronze, layer, query, Excel

Pattern: power-query-bronze
- Triggers match: "bronze layer" (3), "load raw data" (0) = 3 points
- File type match: .m (2) = 2 points
- Difficulty match: task=4, range=3-5 (1) = 1 point
Total: 6 points → High confidence match
```

## Integration with Task System

### Task JSON Extension
When a pattern is applied, task JSON updated:
```json
{
  "id": "15",
  "patterns": {
    "pattern_id": "pattern-microsoft-pq-bronze",
    "applied_at": "2025-12-05"
  }
}
```

### Workflow Integration
1. **Pre-execution gate** → Suggests patterns
2. **User confirmation** → Option to apply pattern
3. **Apply pattern** → Parameters gathered, template applied
4. **Task execution** → Follow pattern template
5. **Post-execution gate** → Verify pattern post-conditions met

## Creating New Patterns

### 1. Identify Need
- Recurring task type with consistent approach
- Common errors in a specific domain
- Best practices to capture

### 2. Create Pattern File
- Use standard format (see above)
- Place in appropriate category directory
- Name as `{name}.pattern.md`

### 3. Populate Sections
- **Metadata**: Assign unique ID, version, category
- **Triggers**: Keywords that indicate this pattern
- **Parameters**: What varies between uses
- **Template**: Actual code/content with placeholders
- **Anti-patterns**: Common mistakes to avoid

### 4. Test Pattern
- Apply to real task
- Verify pre/post conditions work
- Refine based on usage

### 5. Version Pattern
- Start at 1.0.0
- Increment for changes (semver)
- Document changes in pattern notes

## Pattern Versioning

**Semantic Versioning:**
- **Major (X.0.0)**: Breaking changes to template or parameters
- **Minor (x.Y.0)**: New features, additional checks
- **Patch (x.y.Z)**: Bug fixes, clarifications

**Example:**
```
1.0.0 → Initial pattern
1.1.0 → Added error handling to template
1.1.1 → Fixed typo in documentation
2.0.0 → Changed required parameters (breaking)
```

## Benefits

1. **Reduced Errors**: Pre-validated templates minimize mistakes
2. **Faster Execution**: No need to "figure out" common tasks
3. **Consistency**: Same approach every time
4. **Knowledge Capture**: Best practices documented
5. **Onboarding**: New team members see proven approaches
6. **Quality**: Anti-patterns prevent known issues

## Pattern Library Metrics

Track pattern effectiveness:
- **Usage rate**: % of applicable tasks using patterns
- **Error reduction**: Fewer errors in pattern-using tasks
- **Time savings**: Faster execution with patterns
- **Pattern coverage**: % of task types with patterns

## Dependencies

### Required
- Task management component (for task metadata)
- Validation gates component (for pattern suggestions)

### Optional
- Error catalog component (to correlate patterns with error reduction)

## Version History

- **v1.0.0** (2025-12-05): Initial release
  - 4 pattern categories
  - 13 patterns total
  - Find and apply commands
  - Automatic suggestion in pre-execution gate

## See Also

- `components/validation-gates/` - Pattern suggestion integration
- `components/task-management/` - Task metadata for pattern tracking
- `components/error-catalog/` - Error prevention correlation
