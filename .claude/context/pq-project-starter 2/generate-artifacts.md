# Command: Generate Artifacts (Phase 0 - Step 3)

## Purpose
Generate all project artifacts (glossary, data contracts, query manifest, tasks) based on resolved ambiguities.

## Prerequisites
- `resolve-ambiguities.md` has been run for all batches
- All ambiguities have status "✅ Resolved"
- `.claude/context/assumptions.md` is complete

## Process

### 1. Verify Prerequisites
Check `.claude/reference/ambiguity-report.md`:
- Confirm no ambiguities with "⏳ Pending Resolution" status
- If any unresolved, inform user to complete resolve-ambiguities.md first

### 2. Generate Glossary
Create `.claude/context/glossary.md`:

**Structure:**
```markdown
# Variable & Term Glossary

**Purpose:** Defines exact names, types, and units for all variables used in Power Query queries. Claude must NEVER deviate from these names without explicit approval.

**Last Updated:** [Date]

---

## Variables

| Variable Name | Type | Unit | Description | Source Reference |
|---------------|------|------|-------------|------------------|
| RecycledContentShare | Decimal | % | Share of recycled content in material | Delegated Act Art. 7(1) |
| PreConsumerScrap | Decimal | kg | Material from production waste | ISO 22628:2002 §3.1.2 |
| ... | ... | ... | ... | ... |

## Column Naming Conventions

**Pattern:** `snake_case` for data columns, `PascalCase` for calculated variables

**Examples:**
- Input column: `emission_factor_primary`
- Calculated variable: `TotalEmissionsCO2`

## Query Naming Convention

**Pattern:** `[Stage]_[Purpose]_[Entity]`

**Stages:** Bronze, Silver, Gold
**Purpose:** Source, Clean, Validate, Calculate, Transform, Report
**Entity:** Specific data subject (EmissionFactors, Inputs, CFF, Compliance)

**Examples:**
- `Bronze_Source_EmissionFactors`
- `Silver_Validate_Inputs`
- `Gold_Calculate_CFF`

## Units and Conversions

| Measurement | Standard Unit | Conversions |
|-------------|---------------|-------------|
| Mass | kg | 1 tonne = 1000 kg |
| Emissions | kg CO2-eq | Report in kg, store in kg |
| Percentage | decimal | 0.15 = 15%, store as decimal |

## Data Types

| Type | M Language Type | Notes |
|------|-----------------|-------|
| Decimal | type number | Use for all numerical calculations |
| Percentage | type number | Store as decimal (0.15 not 15) |
| Text | type text | For identifiers, categories |
| Date | type date | ISO 8601 format |
| Integer | type number | Use only for counts, IDs |

## Critical Rules

1. **NEVER** use synonyms - one concept = one name
2. **ALWAYS** include units in comments: `// MaterialMassRaw in kg`
3. **ALWAYS** use approved names from this glossary
4. When in doubt, ASK - don't guess or create new names
5. All variable names must be traceable to source document

---

## Terms by Source Document

### [Document 1 Name]
[List terms defined in this document]

### [Document 2 Name]
[List terms defined in this document]

---

**References:**
- Assumptions: `.claude/context/assumptions.md`
- Source Documents: `calculation-docs/`
```

**Content Generation:**
- Extract every variable from calculation documents
- Apply resolved ambiguities from assumptions.md
- Ensure consistent naming across all terms
- Cross-reference with source documents
- Include derived variables (calculated from others)

### 3. Generate Data Contracts
Create `.claude/reference/data-contracts.md`:

**Structure:**
```markdown
# Data Contracts

**Purpose:** Defines expected input and output schemas for all Power Query queries.

**Last Updated:** [Date]

---

## Query: [Query Name]

**Stage:** [Bronze/Silver/Gold]
**Purpose:** [What this query does]

### Input Schema
| Column Name | Data Type | Nullable | Validation Rules | Source |
|-------------|-----------|----------|------------------|--------|
| company_id | text | No | Length > 0 | Input table |
| emission_factor | number | No | > 0 | Emission factors table |
| ... | ... | ... | ... | ... |

### Output Schema
| Column Name | Data Type | Nullable | Description | Unit |
|-------------|-----------|----------|-------------|------|
| company_id | text | No | Company identifier | - |
| total_emissions | number | No | Calculated total emissions | kg CO2-eq |
| ... | ... | ... | ... | ... |

### Transformations
1. [Step 1 description]
2. [Step 2 description]

### Dependencies
- Depends on: [List of queries this needs]
- Used by: [List of queries that use this]

### Validation Rules
- [Rule 1]
- [Rule 2]

---

[Repeat for each query]

---

## Schema Validation Checklist

For each query, verify:
- [ ] All input columns documented
- [ ] All output columns documented
- [ ] Data types specified
- [ ] Nullable fields identified
- [ ] Validation rules defined
- [ ] Dependencies mapped
```

**Content Generation:**
- Analyze calculation formulas to determine data needs
- Infer input schemas from Excel file structures
- Design output schemas based on requirements
- Apply naming conventions from glossary
- Include validation rules from assumptions

### 4. Generate Query Manifest
Create `.claude/reference/query-manifest.md`:

**Structure:**
```markdown
# Query Manifest

**Purpose:** Master list of all Power Query queries with descriptions and relationships.

**Last Updated:** [Date]

---

## Bronze Layer: Data Ingestion

### Bronze_Source_EmissionFactors
**Purpose:** Load emission factors from reference table
**Input:** `EmissionFactors` table from `emission-factors.xlsx`
**Output:** Raw emission factors with all columns
**Transformations:** None (source only)
**Dependencies:** None
**Used By:** Silver_Clean_EmissionFactors

---

### Bronze_Source_InputTables
[Similar structure]

---

## Silver Layer: Data Cleaning & Validation

### Silver_Clean_EmissionFactors
**Purpose:** Clean and validate emission factors
**Input:** Bronze_Source_EmissionFactors
**Output:** Validated emission factors
**Transformations:**
1. Remove rows with null emission factors
2. Validate EF > 0
3. Type conversions
4. Add validation flags
**Dependencies:** Bronze_Source_EmissionFactors
**Used By:** Gold_Calculate_CFF

---

[Continue for all queries]

---

## Gold Layer: Business Logic

### Gold_Calculate_CFF
**Purpose:** Calculate Carbon Footprint Formula per Article 7
**Input:** Silver_Clean_EmissionFactors, Silver_Validate_Inputs
**Output:** Final CFF values with compliance flags
**Transformations:**
1. [Detailed calculation steps]
**Dependencies:** Multiple silver queries
**Used By:** Gold_Compliance_Report

---

## Query Execution Order

1. Bronze_Source_EmissionFactors
2. Bronze_Source_InputTables
3. Silver_Clean_EmissionFactors (depends on #1)
4. Silver_Validate_Inputs (depends on #2)
5. Gold_Calculate_CFF (depends on #3, #4)
6. Gold_Compliance_Report (depends on #5)

---

## Query Count by Stage

- **Bronze:** [Count] queries
- **Silver:** [Count] queries
- **Gold:** [Count] queries
- **Total:** [Count] queries
```

**Content Generation:**
- Derive queries needed from calculation requirements
- Map bronze-silver-gold architecture
- Establish query dependencies
- Determine execution order
- Ensure all calculations are covered

### 5. Generate Dependency Graph
Create `.claude/reference/dependency-graph.md`:

**Structure:**
```markdown
# Query Dependency Graph

**Purpose:** Visual representation of query relationships and execution order.

**Last Updated:** [Date]

---

## Dependency Tree

```
Bronze Layer
├── Bronze_Source_EmissionFactors
│   └──> Used by: Silver_Clean_EmissionFactors
│
└── Bronze_Source_InputTables
    └──> Used by: Silver_Validate_Inputs

Silver Layer
├── Silver_Clean_EmissionFactors
│   ├── Depends on: Bronze_Source_EmissionFactors
│   └──> Used by: Gold_Calculate_CFF
│
└── Silver_Validate_Inputs
    ├── Depends on: Bronze_Source_InputTables
    └──> Used by: Gold_Calculate_CFF

Gold Layer
├── Gold_Calculate_CFF
│   ├── Depends on: Silver_Clean_EmissionFactors
│   ├── Depends on: Silver_Validate_Inputs
│   └──> Used by: Gold_Compliance_Report
│
└── Gold_Compliance_Report
    └── Depends on: Gold_Calculate_CFF
```

---

## Critical Path

Longest execution chain:
Bronze_Source_InputTables → Silver_Validate_Inputs → Gold_Calculate_CFF → Gold_Compliance_Report

---

## Dependency Rules

1. **No circular dependencies** - Verified ✓
2. **Bronze has no dependencies** - Verified ✓
3. **Silver depends only on Bronze** - Verified ✓
4. **Gold depends on Silver/Gold** - Verified ✓

---

## Impact Analysis

**If Bronze_Source_EmissionFactors changes:**
- Affects: Silver_Clean_EmissionFactors → Gold_Calculate_CFF → Gold_Compliance_Report
- Queries to refresh: 3
- Impact level: High

[Similar analysis for other key queries]
```

**Content Generation:**
- Build dependency tree from query manifest
- Verify no circular dependencies
- Identify critical paths
- Calculate impact of changes

### 6. Generate Initial Tasks
Create task files in `.claude/tasks/`:

**Task Generation Logic:**
- One task per query to implement
- Additional tasks for:
  - Data validation setup
  - Error handling implementation
  - Testing with sample data
  - Documentation
- Apply difficulty scoring per `.claude/reference/difficulty-guide-pq.md`
- Tasks with difficulty ≥7 flagged for breakdown

**Task Structure (task-N.json):**
```json
{
  "id": "1",
  "title": "Implement Bronze_Source_EmissionFactors query",
  "description": "Create source query to load emission factors from Excel table. See data-contracts.md for schema.",
  "difficulty": 3,
  "status": "Pending",
  "created_date": "2024-01-15",
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "notes": "Context: glossary.md for variable names, assumptions.md #5 for null handling"
}
```

**Task Sequence:**
1. Bronze queries (low difficulty, no dependencies)
2. Silver queries (medium difficulty, depend on bronze)
3. Gold queries (high difficulty, complex logic)
4. Validation and testing tasks

**Generate task-overview.md:**
```markdown
# Task Overview

**Project:** [Name]
**Generated:** [Date]
**Total Tasks:** [Count]

---

## Pending Tasks

| ID | Title | Difficulty | Dependencies | Notes |
|----|-------|------------|--------------|-------|
| 1 | Implement Bronze_Source_EmissionFactors | 3 | None | |
| 2 | Implement Bronze_Source_InputTables | 3 | None | |
| 3 | Implement Silver_Clean_EmissionFactors | 5 | 1 | |
| ... | ... | ... | ... | ... |

## High-Difficulty Tasks (Need Breakdown)

| ID | Title | Difficulty |
|----|-------|------------|
| 8 | Implement Gold_Calculate_CFF | 8 | 🔴

**Note:** Tasks with 🔴 marker should be broken down using `@.claude/commands/breakdown.md [id]` before starting work.

---

**Statistics:**
- Total Tasks: [Count]
- Pending: [Count]
- Need Breakdown: [Count with difficulty ≥7]

**Next Action:** Review task list, then run `@.claude/commands/extract-queries.md`
```

### 7. Update CLAUDE.md
Replace Phase 0 instructions with Phase 1 instructions:

```markdown
# Power Query Project: [Project Name]

## Phase 1: Task Execution

Phase 0 Complete ✅ ([Date])
- [N] terms defined in glossary
- [N] assumptions documented
- [N] queries planned
- [N] tasks generated

## Current Status

**Next Task:** [First pending task]

See `.claude/tasks/task-overview.md` for complete task list.

## Quick Commands

**Task Management:**
- `@.claude/commands/complete-task.md [id]` - Work on a task
- `@.claude/commands/breakdown.md [id]` - Split high-difficulty task (≥7)
- `@.claude/commands/update-tasks.md` - Validate task structure
- `@.claude/commands/sync-tasks.md` - Update task overview

**Query Operations:**
- `@.claude/commands/validate-query.md [name]` - Check schema compliance
- Power Query files in `power-query/` directory
- Extension auto-syncs changes to Excel

## Key Context Files

**Always Referenced:**
- **Glossary:** `.claude/context/glossary.md` - Variable definitions
- **Assumptions:** `.claude/context/assumptions.md` - Interpretation decisions
- **LLM Pitfalls:** `.claude/context/llm-pitfalls.md` - Checklist for implementation

**Query-Specific:**
- **Data Contracts:** `.claude/reference/data-contracts.md` - Expected schemas
- **Query Manifest:** `.claude/reference/query-manifest.md` - What each query does
- **Dependencies:** `.claude/reference/dependency-graph.md` - Query relationships

## Development Workflow

1. Select task: `@.claude/commands/complete-task.md [id]`
2. Claude loads relevant context automatically
3. Claude implements query following specs
4. Extension auto-syncs to Excel
5. Validate: `@.claude/commands/validate-query.md [QueryName]`
6. Task completes, git commit

## Project Statistics

- **Queries:** [Count] total ([Bronze]/[Silver]/[Gold])
- **Tasks:** [Pending]/[Total] remaining
- **High-Difficulty:** [Count] tasks need breakdown first

---

**Ready to start?** Run `@.claude/commands/complete-task.md 1`
```

### 8. Update Phase 0 Status
Mark Phase 0 complete in `.claude/tasks/_phase-0-status.md`:

```markdown
# Phase 0 Initialization Status

**Status:** ✅ COMPLETE
**Completed:** [Date]

## Final Statistics

- Documents analyzed: [Count]
- Ambiguities resolved: [Count]
- Terms defined: [Count]
- Queries planned: [Count]
- Tasks generated: [Count]

## Generated Artifacts

✅ `.claude/context/glossary.md` - [N] terms defined
✅ `.claude/context/assumptions.md` - [N] decisions documented
✅ `.claude/reference/data-contracts.md` - [N] query schemas
✅ `.claude/reference/query-manifest.md` - [N] queries planned
✅ `.claude/reference/dependency-graph.md` - Dependencies mapped
✅ `.claude/tasks/*.json` - [N] task files created
✅ `.claude/tasks/task-overview.md` - Task summary
✅ `CLAUDE.md` - Updated with Phase 1 instructions

## Next Steps

1. Run `@.claude/commands/extract-queries.md`
2. Begin task execution with `@.claude/commands/complete-task.md [id]`
```

## Output Summary

Present to user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 0 - Step 3 Complete ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated Artifacts:

📖 Glossary: [N] terms defined
   - All variables standardized
   - Naming conventions established
   - Unit conversions documented

📋 Data Contracts: [N] query schemas
   - Input/output schemas defined
   - Validation rules specified
   - Data types standardized

📊 Query Manifest: [N] queries planned
   - Bronze layer: [Count] queries
   - Silver layer: [Count] queries
   - Gold layer: [Count] queries

🔗 Dependency Graph:
   - Execution order established
   - No circular dependencies
   - Impact analysis ready

✅ Tasks: [N] tasks generated
   - [Count] ready to work
   - [Count] need breakdown (difficulty ≥7)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Step: Run @.claude/commands/extract-queries.md

This will:
1. Guide you through extracting .m files from Excel
2. Set up watch mode
3. Prepare for first task execution

Review the generated artifacts before proceeding.
```

## Quality Checks

Before finalizing:
- [ ] All glossary terms traceable to source
- [ ] No undefined variables in queries
- [ ] Data contracts match Excel structure
- [ ] Query dependencies are valid (no cycles)
- [ ] All tasks reference correct context files
- [ ] Difficulty scores are reasonable
- [ ] CLAUDE.md updated correctly

## Notes

- This step is primarily artifact generation
- No user interaction required after running
- Review all generated files before proceeding
- Can regenerate if needed (will overwrite)
- Changes to source documents require re-running Phase 0
