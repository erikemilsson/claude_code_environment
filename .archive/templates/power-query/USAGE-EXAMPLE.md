# Power Query Template Usage Example

This document provides complete, real-world examples of bootstrapping a new Power Query project using this template.

## Table of Contents
1. [Example 1: Minimal Approach (Simple Data Transformation)](#example-1-minimal-approach)
2. [Example 2: Comprehensive Approach (Regulatory Calculation)](#example-2-comprehensive-approach)
3. [Phase 0 Workflow Walkthrough](#phase-0-workflow-walkthrough)
4. [Task Breakdown Examples](#task-breakdown-examples)

---

## Example 1: Minimal Approach

**Scenario**: You have an existing Excel workbook with Power Query transformations for cleaning customer data. You want to add version control and basic documentation.

### Step 1: Copy Template Files

```bash
# In your project directory
mkdir my-customer-data-project
cd my-customer-data-project

# Copy minimal CLAUDE.md
cp ../claude_code_environment/templates/power-query/CLAUDE-minimal.md CLAUDE.md

# Copy basic context files
cp ../claude_code_environment/templates/power-query/context/overview.md .claude/context/
cp ../claude_code_environment/templates/power-query/context/critical_rules.md .claude/context/

# Copy essential commands
cp ../claude_code_environment/templates/power-query/commands/extract-queries.md .claude/commands/
cp ../claude_code_environment/templates/power-query/commands/complete-task.md .claude/commands/
```

### Step 2: Edit Overview

Update `.claude/context/overview.md`:

```markdown
# Project Overview

Customer data cleaning and transformation pipeline for monthly reporting.

## Data Sources
- Excel file: customer_data.xlsx
- Source: CRM system export

## Goal
Clean and standardize customer records:
- Remove duplicates
- Standardize address formats
- Calculate customer lifetime value
- Flag inactive customers

## Deliverable
Cleaned dataset ready for Power BI import
```

### Step 3: Extract Existing Queries

Place your Excel file in `excel-files/` directory:

```bash
mkdir excel-files
cp ~/Downloads/customer_data.xlsx excel-files/
```

In Claude Code:
```
@.claude/commands/extract-queries.md

Extract queries from excel-files/customer_data.xlsx
```

Result:
```
power-query/
├── RemoveDuplicates.m
├── StandardizeAddresses.m
├── CalculateLifetimeValue.m
└── FlagInactiveCustomers.m
```

### Step 4: Create Simple Tasks

Create tasks for any improvements needed:

`.claude/tasks/task-1.json`:
```json
{
  "id": "1",
  "title": "Add error handling to address standardization",
  "description": "Wrap address parsing in try/otherwise to handle malformed addresses",
  "difficulty": 4,
  "status": "Pending",
  "created_date": "2025-11-16",
  "updated_date": "2025-11-16",
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "notes": "Currently fails on addresses with missing zip codes"
}
```

### Step 5: Work on Tasks

```
/complete-task 1
```

Claude Code will:
1. Load task-1.json
2. Read power-query/StandardizeAddresses.m
3. Add error handling
4. Test the changes
5. Mark task complete

### Minimal Approach Summary

**Time to set up**: ~15 minutes
**Files created**: 10-15
**Best for**:
- Simple transformations
- Solo developer
- No regulatory requirements
- Quick prototyping

---

## Example 2: Comprehensive Approach

**Scenario**: Implementing EU Battery Regulation calculations requiring exact compliance with legal definitions, multiple data sources, and audit trail.

### Step 1: Copy Full Template

```bash
# In your project directory
mkdir eu-battery-calculation
cd eu-battery-calculation

# Copy comprehensive CLAUDE.md
cp ../claude_code_environment/templates/power-query/CLAUDE-template.md CLAUDE.md

# Copy all template directories
cp -r ../claude_code_environment/templates/power-query/commands/ .claude/commands/
cp -r ../claude_code_environment/templates/power-query/context/ .claude/context/
cp -r ../claude_code_environment/templates/power-query/reference/ .claude/reference/

# Create project directories
mkdir calculation-docs
mkdir excel-files
mkdir power-query
mkdir tests/sample-data -p
```

### Step 2: Add Regulatory Documents

```bash
# Place regulatory PDFs in calculation-docs/
cp ~/Documents/EU_Battery_Regulation_2023-1542.pdf calculation-docs/
cp ~/Documents/Annex_VII_Calculation_Methods.pdf calculation-docs/
```

### Step 3: Edit Overview

Update `.claude/context/overview.md`:

```markdown
# Project Overview

Implementation of EU Battery Regulation 2023/1542 calculations for carbon footprint declaration.

## Regulatory Context
- **Regulation**: EU 2023/1542 (Battery Regulation)
- **Annex**: Annex VII - Carbon Footprint Calculation Rules
- **Scope**: Articles 7-12 (Battery carbon footprint)
- **Compliance Date**: August 18, 2025

## Data Sources
1. Manufacturing data (Excel): energy consumption, material weights
2. Supply chain data (Excel): transport distances, supplier carbon intensities
3. Reference tables (calculation-docs): emission factors, conversion rates

## Deliverables
1. Carbon footprint value (kg CO2e per battery)
2. Breakdown by lifecycle stage (material, manufacturing, transport)
3. Audit trail showing calculation steps
4. Data quality assessment report
```

### Step 4: Run Phase 0 Workflow

This is where the comprehensive approach differs significantly.

#### Phase 0 Step 1: Initialize Project

In Claude Code:
```
/initialize-project
```

Claude analyzes `calculation-docs/` and creates `.claude/reference/ambiguity-report.md`:

```markdown
# Ambiguity Report

## High-Priority Ambiguities

### AMB-001: Allocation Method for Shared Manufacturing
**Location**: Annex VII, Article 3.2
**Text**: "Where manufacturing processes serve multiple battery types, allocation shall be based on physical or economic causality"
**Ambiguity**: Does not specify which method to prioritize or when to use each
**Impact**: Affects denominator in allocation formula
**Questions**:
- Use physical (e.g., energy consumption per kg)?
- Use economic (e.g., production cost)?
- Combination approach?

### AMB-002: System Boundary for Transport
**Location**: Annex VII, Article 4.1.3
**Text**: "Transport includes movement of materials from extraction to battery assembly"
**Ambiguity**: Unclear if return journeys and internal facility transport are included
**Impact**: May double or miss transport emissions
**Questions**:
- Include return journeys (empty trucks)?
- Include intra-facility transport?
- Include packaging material transport?

[... 47 more ambiguities identified ...]
```

#### Phase 0 Step 2: Resolve Ambiguities

In Claude Code:
```
/resolve-ambiguities
```

Interactive session (batch resolution, 5 at a time):

```
AMBIGUITY BATCH 1/10 (5 ambiguities)

AMB-001: Allocation Method for Shared Manufacturing
Options:
A) Physical allocation (energy consumption per kg)
B) Economic allocation (production cost)
C) Hybrid approach (physical for direct, economic for indirect)

Your decision: C

Rationale: [Claude prompts for explanation]
> "Physical allocation for direct energy use (more accurate). Economic for shared overhead costs (pragmatic)."

RECORDED:
- Decision: Hybrid allocation method
- Glossary entry: allocation_method_manufacturing
- Assumption: "Physical causality used for direct energy, economic for shared costs"

---

AMB-002: System Boundary for Transport
[... continues for remaining 4 in batch ...]

Continue to next batch? (y/n): y
```

After resolving all 49 ambiguities, you have:
- `.claude/context/assumptions.md` (49 documented decisions)
- `.claude/context/glossary.md` (stub entries for 127 variables)

#### Phase 0 Step 3: Generate Artifacts

In Claude Code:
```
/generate-artifacts
```

Claude creates:

1. **Completed Glossary** (`.claude/context/glossary.md`):
```markdown
# Variable Glossary

## A

### allocation_method_manufacturing
**Definition**: Method for allocating energy consumption when manufacturing processes serve multiple battery types
**Value**: Hybrid approach - physical causality for direct energy, economic for shared costs
**Source**: Assumption AMB-001, Annex VII Article 3.2
**Unit**: Dimensionless (allocation factor)
**Used in**: Manufacturing_AllocateEnergy query

### annual_production_volume
**Definition**: Total number of batteries produced per year at facility
**Value**: From manufacturing_data.xlsx, column "Annual_Volume"
**Source**: Manufacturing Data
**Unit**: batteries/year
**Used in**: Manufacturing_AllocateEnergy query, Performance_CalculateIntensity query

[... 125 more variables ...]
```

2. **Data Contracts** (`.claude/reference/data-contracts.md`):
```markdown
# Data Contracts

## Source: manufacturing_data.xlsx

### Expected Schema
| Column Name | Data Type | Required | Validation | Example |
|------------|-----------|----------|------------|---------|
| Facility_ID | Text | Yes | Format: "FAC-[0-9]{4}" | "FAC-0001" |
| Annual_Volume | Number | Yes | > 0 | 50000 |
| Energy_Consumption_kWh | Number | Yes | ≥ 0 | 125000.5 |
| Production_Cost_EUR | Number | Yes | ≥ 0 | 850000 |

### Queries Consuming This Source
- Bronze_IngestManufacturing
- Manufacturing_AllocateEnergy

[... more sources ...]
```

3. **Query Manifest** (`.claude/reference/query-manifest.md`):
```markdown
# Query Manifest

## Bronze Layer (Data Ingestion)

### Bronze_IngestManufacturing
**Purpose**: Ingest raw manufacturing data from Excel
**Input**: excel-files/manufacturing_data.xlsx
**Output Schema**: Same as source + metadata columns (ingestion_timestamp, source_file)
**Dependencies**: None (source query)
**Complexity**: Low (1/10) - Simple table load

### Bronze_IngestSupplyChain
**Purpose**: Ingest raw supply chain data from Excel
[...]

## Silver Layer (Data Cleaning & Transformation)

### Silver_CleanManufacturing
**Purpose**: Validate and clean manufacturing data
**Input**: Bronze_IngestManufacturing
**Output Schema**: Cleaned manufacturing data with validation flags
**Dependencies**: Bronze_IngestManufacturing
**Transformations**:
- Remove rows where Energy_Consumption_kWh < 0
- Flag facilities with missing Facility_ID
- Standardize date formats
**Complexity**: Medium (4/10)

[... 23 more queries described ...]
```

4. **Dependency Graph** (`.claude/reference/dependency-graph.md`):
```markdown
# Query Dependency Graph

## Execution Order

### Stage 1: Bronze (Data Ingestion)
- Bronze_IngestManufacturing
- Bronze_IngestSupplyChain
- Bronze_IngestEmissionFactors

### Stage 2: Silver (Cleaning)
- Silver_CleanManufacturing (depends: Bronze_IngestManufacturing)
- Silver_CleanSupplyChain (depends: Bronze_IngestSupplyChain)
- Silver_ValidateEmissionFactors (depends: Bronze_IngestEmissionFactors)

### Stage 3: Silver (Business Logic)
- Manufacturing_AllocateEnergy (depends: Silver_CleanManufacturing)
- Transport_CalculateDistances (depends: Silver_CleanSupplyChain)
- Emission_LookupFactors (depends: Silver_ValidateEmissionFactors)

### Stage 4: Gold (Aggregation)
- Gold_CarbonFootprint_Manufacturing (depends: Manufacturing_AllocateEnergy, Emission_LookupFactors)
- Gold_CarbonFootprint_Transport (depends: Transport_CalculateDistances, Emission_LookupFactors)

### Stage 5: Gold (Final Output)
- Gold_TotalCarbonFootprint (depends: Gold_CarbonFootprint_Manufacturing, Gold_CarbonFootprint_Transport)

## Visual Representation

```
Bronze_IngestManufacturing → Silver_CleanManufacturing → Manufacturing_AllocateEnergy ↘
                                                                                        Gold_CarbonFootprint_Manufacturing ↘
Bronze_IngestEmissionFactors → Silver_ValidateEmissionFactors → Emission_LookupFactors ↗                                    ↘
                                                                                                                              Gold_TotalCarbonFootprint
Bronze_IngestSupplyChain → Silver_CleanSupplyChain → Transport_CalculateDistances ↘                                        ↗
                                                                                     Gold_CarbonFootprint_Transport ↗
```
```

5. **Initial Tasks** (`.claude/tasks/task-1.json` through `task-25.json`):

Example task (`.claude/tasks/task-12.json`):
```json
{
  "id": "12",
  "title": "Implement Manufacturing_AllocateEnergy query",
  "description": "Calculate allocated energy consumption using hybrid method (physical for direct, economic for shared costs). Apply allocation factors to total energy consumption. Handle edge cases (zero production volume, missing cost data).",
  "difficulty": 7,
  "status": "Pending",
  "created_date": "2025-11-16",
  "updated_date": "2025-11-16",
  "dependencies": ["4"],
  "subtasks": [],
  "parent_task": null,
  "notes": "References: glossary.md (allocation_method_manufacturing, annual_production_volume), data-contracts.md (manufacturing_data schema), assumptions.md (AMB-001). Formula complexity: 8/10. Error surface: 7/10 (division by zero). Must break down (difficulty ≥7)."
}
```

#### Phase 0 Step 4: Extract Queries Template

Since this is a new project, create empty Excel template:

In Claude Code:
```
/initialize-project excel-template
```

Claude creates `excel-files/battery_calculation_template.xlsx` with:
- Empty Power Query queries named according to manifest
- Proper folder organization (Bronze/, Silver/, Gold/)
- Connection-only queries configured

Or if you have an existing Excel file:
```
/extract-queries excel-files/battery_workbook.xlsx
```

### Step 5: Work Through Tasks with Breakdown

Task 12 has difficulty 7, so it must be broken down:

```
/breakdown 12
```

Claude creates subtasks:

`.claude/tasks/task-12.json` (updated):
```json
{
  "id": "12",
  "title": "Implement Manufacturing_AllocateEnergy query",
  "description": "Calculate allocated energy consumption using hybrid method...",
  "difficulty": 7,
  "status": "Broken Down",
  "created_date": "2025-11-16",
  "updated_date": "2025-11-16",
  "dependencies": ["4"],
  "subtasks": ["12.1", "12.2", "12.3", "12.4"],
  "parent_task": null,
  "notes": "Broken down into 4 subtasks. Auto-completes when all subtasks finish."
}
```

`.claude/tasks/task-12.1.json`:
```json
{
  "id": "12.1",
  "title": "Create query structure and load dependencies",
  "description": "Create Manufacturing_AllocateEnergy query. Load Silver_CleanManufacturing table. Add columns for allocation calculations.",
  "difficulty": 3,
  "status": "Pending",
  "created_date": "2025-11-16",
  "updated_date": "2025-11-16",
  "dependencies": [],
  "subtasks": [],
  "parent_task": "12",
  "notes": ""
}
```

`.claude/tasks/task-12.2.json`:
```json
{
  "id": "12.2",
  "title": "Implement physical allocation formula",
  "description": "Calculate physical allocation factor = (Battery_Energy_kWh / Total_Facility_Energy_kWh). Handle zero division. Add validation.",
  "difficulty": 4,
  "status": "Pending",
  "created_date": "2025-11-16",
  "updated_date": "2025-11-16",
  "dependencies": ["12.1"],
  "subtasks": [],
  "parent_task": "12",
  "notes": "Error handling: if Total_Facility_Energy_kWh = 0, return null and flag row"
}
```

`.claude/tasks/task-12.3.json`:
```json
{
  "id": "12.3",
  "title": "Implement economic allocation formula",
  "description": "Calculate economic allocation factor = (Battery_ProductionCost_EUR / Total_Facility_Cost_EUR). Handle missing cost data.",
  "difficulty": 4,
  "status": "Pending",
  "created_date": "2025-11-16",
  "updated_date": "2025-11-16",
  "dependencies": ["12.1"],
  "subtasks": [],
  "parent_task": "12",
  "notes": "Error handling: if cost data missing, fall back to physical allocation only"
}
```

`.claude/tasks/task-12.4.json`:
```json
{
  "id": "12.4",
  "title": "Apply hybrid allocation and test edge cases",
  "description": "Combine physical and economic factors per assumption AMB-001. Test with zero production, missing costs, negative values. Add LLM pitfall checks.",
  "difficulty": 5,
  "status": "Pending",
  "created_date": "2025-11-16",
  "updated_date": "2025-11-16",
  "dependencies": ["12.2", "12.3"],
  "subtasks": [],
  "parent_task": "12",
  "notes": "Check llm-pitfalls.md: unit consistency, null propagation, try/otherwise usage"
}
```

Now work on subtasks:

```
/complete-task 12.1
```

Claude:
1. Loads glossary.md, assumptions.md, llm-pitfalls.md (core context)
2. Loads data-contracts.md (schema for Silver_CleanManufacturing)
3. Loads query-manifest.md (query description)
4. Creates power-query/Manufacturing_AllocateEnergy.m
5. Marks task 12.1 as Finished

```
/complete-task 12.2
```

Claude:
1. Loads all core context
2. Reads power-query/Manufacturing_AllocateEnergy.m
3. Implements physical allocation with error handling
4. Tests zero division case
5. Marks task 12.2 as Finished

... continue through 12.3 and 12.4 ...

When task 12.4 finishes:
- Task 12.4 status → Finished
- Task 12.3 status → Finished (was already done)
- Task 12.2 status → Finished (was already done)
- Task 12.1 status → Finished (was already done)
- **Task 12 automatically transitions to Finished** (all subtasks complete)

### Step 6: Sync and Review

```
/sync-tasks
```

Updates `.claude/tasks/task-overview.md`:

```markdown
# Task Overview

| ID | Title | Difficulty | Status | Dependencies | Progress |
|----|-------|-----------|--------|--------------|----------|
| 1 | Implement Bronze_IngestManufacturing | 2 | Finished | - | - |
| 2 | Implement Bronze_IngestSupplyChain | 2 | Finished | - | - |
| ... | ... | ... | ... | ... | ... |
| 12 | Implement Manufacturing_AllocateEnergy | 7 | Finished | 4 | Broken Down (4/4 done) |
| 12.1 | Create query structure | 3 | Finished | - | - |
| 12.2 | Implement physical allocation | 4 | Finished | 12.1 | - |
| 12.3 | Implement economic allocation | 4 | Finished | 12.1 | - |
| 12.4 | Apply hybrid allocation | 5 | Finished | 12.2, 12.3 | - |
| ... | ... | ... | ... | ... | ... |
```

### Comprehensive Approach Summary

**Time to set up**: 2-4 hours (including ambiguity resolution)
**Files created**: 80-150
**Phase 0 artifacts**: 5 (glossary, assumptions, data contracts, manifest, dependency graph)
**Tasks created**: 25-50 (depending on complexity)
**Best for**:
- Regulatory/compliance calculations
- Ambiguous source documents
- Zero error tolerance
- Team collaboration
- Audit trail requirements

---

## Phase 0 Workflow Walkthrough

### Why Phase 0?

Traditional approach (BAD):
```
User: "Implement Article 7.2 calculation from the regulation"
Claude: "Sure, I'll implement..."
[implements based on misunderstood definition]
[discovers 20 ambiguities during implementation]
[refactors repeatedly as assumptions change]
```

Phase 0 approach (GOOD):
```
User: "Implement Article 7.2 calculation"
Claude: "I found 47 ambiguities. Let's resolve them first."
[interactive resolution session]
[generates glossary with every variable defined]
[implementation proceeds smoothly, no refactoring needed]
```

### Phase 0 Commands Deep Dive

#### Command 1: initialize-project.md

**What it does**:
- Scans all PDFs in `calculation-docs/`
- Extracts calculation formulas, definitions, and requirements
- Identifies ambiguities (unclear language, missing specifications)
- Creates ambiguity report with structured questions

**When to run**: Once, at project start

**Output**: `.claude/reference/ambiguity-report.md`

#### Command 2: resolve-ambiguities.md

**What it does**:
- Presents ambiguities in batches of 5
- Prompts for decisions with multiple-choice options
- Records rationale for each decision
- Updates glossary stubs and assumptions document

**When to run**: Once, after initialize-project

**Output**:
- `.claude/context/assumptions.md`
- `.claude/context/glossary.md` (stub entries)

#### Command 3: generate-artifacts.md

**What it does**:
- Expands glossary stubs into full definitions
- Creates data contracts from source file analysis
- Generates query manifest (what each query does)
- Builds dependency graph (execution order)
- Creates initial task breakdown

**When to run**: Once, after resolve-ambiguities

**Output**:
- `.claude/context/glossary.md` (completed)
- `.claude/reference/data-contracts.md`
- `.claude/reference/query-manifest.md`
- `.claude/reference/dependency-graph.md`
- `.claude/tasks/task-*.json` (initial tasks)

#### Command 4: extract-queries.md

**What it does**:
- Extracts Power Query .m files from Excel workbook
- Saves individual files to `power-query/` directory
- Enables watch mode for auto-sync (optional)
- Adds queries to git tracking

**When to run**:
- Once after generate-artifacts (if starting from template)
- Once at start (if working with existing Excel file)
- Anytime to refresh queries from Excel

**Output**: `power-query/*.m` files

---

## Task Breakdown Examples

### Example 1: Formula Complexity Triggers Breakdown

**Original Task**:
```json
{
  "id": "18",
  "title": "Calculate lifecycle carbon footprint",
  "description": "Sum carbon footprint across all lifecycle stages (material extraction, manufacturing, transport, use phase, end-of-life). Apply weighting factors from Annex VII Table 3. Handle missing stages gracefully.",
  "difficulty": 8
}
```

**5-Dimension Analysis**:
- Query Dependency Depth: 9/10 (depends on 8 upstream queries)
- Formula Complexity: 8/10 (weighted sum with conditional logic)
- Error Surface: 7/10 (null propagation from any upstream query)
- Regulatory Precision: 10/10 (final compliance number)
- Performance Impact: 5/10 (aggregation over moderate dataset)
- **Final Score**: (9+8+7+10+5)/5 = 7.8 → **8** (must break down)

**Broken Down Into**:

```json
{
  "id": "18.1",
  "title": "Load and validate upstream query results",
  "description": "Load all 8 upstream queries. Validate schemas match data contracts. Flag any missing data.",
  "difficulty": 3,
  "parent_task": "18"
}
```

```json
{
  "id": "18.2",
  "title": "Apply weighting factors from Annex VII",
  "description": "Join with regulatory weighting table. Handle battery type-specific weights. Default to conservative weights if type unknown.",
  "difficulty": 4,
  "dependencies": ["18.1"],
  "parent_task": "18"
}
```

```json
{
  "id": "18.3",
  "title": "Sum weighted carbon footprint",
  "description": "Calculate total = Σ(stage_carbon * stage_weight). Handle null propagation (if any stage missing, flag but continue with available data).",
  "difficulty": 5,
  "dependencies": ["18.2"],
  "parent_task": "18"
}
```

```json
{
  "id": "18.4",
  "title": "Add compliance checks and audit trail",
  "description": "Verify result against regulatory thresholds. Add metadata columns (calculation_timestamp, data_quality_score). Cross-check with llm-pitfalls.md.",
  "difficulty": 4,
  "dependencies": ["18.3"],
  "parent_task": "18"
}
```

### Example 2: Regulatory Precision Triggers Breakdown

**Original Task**:
```json
{
  "id": "22",
  "title": "Parse battery chemistry from product codes",
  "description": "Extract battery chemistry type from manufacturer product codes. Map to regulatory categories (NMC, LFP, LTO, etc.) per Annex II definitions.",
  "difficulty": 7
}
```

**5-Dimension Analysis**:
- Query Dependency Depth: 2/10 (minimal dependencies)
- Formula Complexity: 6/10 (string parsing + lookup)
- Error Surface: 8/10 (many edge cases: typos, new codes, ambiguous codes)
- Regulatory Precision: 9/10 (affects which regulations apply)
- Performance Impact: 3/10 (simple text operation)
- **Final Score**: (2+6+8+9+3)/5 = 5.6 → **6** (below threshold, but...)

**Why still break down**: High error surface + high regulatory precision = risky.

**Broken Down Into**:

```json
{
  "id": "22.1",
  "title": "Create chemistry code mapping table",
  "description": "Build comprehensive lookup table from Annex II definitions. Include common variations and legacy codes. Document assumptions for ambiguous cases.",
  "difficulty": 3,
  "parent_task": "22"
}
```

```json
{
  "id": "22.2",
  "title": "Implement parsing logic with error handling",
  "description": "Extract chemistry code from product string. Try multiple parsing strategies (regex, substring, delimiter). Flag unparseable codes.",
  "difficulty": 4,
  "dependencies": ["22.1"],
  "parent_task": "22"
}
```

```json
{
  "id": "22.3",
  "title": "Validate against real product codes and create fallback logic",
  "description": "Test with sample-data/product_codes.csv. For unknown codes: attempt fuzzy match, flag for manual review, default to conservative category.",
  "difficulty": 5,
  "dependencies": ["22.2"],
  "parent_task": "22"
}
```

### Example 3: Simple Task (No Breakdown Needed)

**Task**:
```json
{
  "id": "5",
  "title": "Add ingestion timestamp to Bronze queries",
  "description": "Add column 'ingestion_timestamp' with DateTime.LocalNow() to all Bronze layer queries for audit trail.",
  "difficulty": 2
}
```

**5-Dimension Analysis**:
- Query Dependency Depth: 1/10 (source queries)
- Formula Complexity: 1/10 (single function call)
- Error Surface: 1/10 (DateTime.LocalNow() never fails)
- Regulatory Precision: 2/10 (audit metadata, not core calculation)
- Performance Impact: 1/10 (negligible)
- **Final Score**: (1+1+1+2+1)/5 = 1.2 → **1** (no breakdown needed)

**Work directly**: `/complete-task 5`

---

## Key Takeaways

### When to Use Minimal Approach
- Solo developer
- Simple transformations
- No compliance requirements
- Existing Excel file needs version control
- Quick prototypes
- **Time saved**: Skip Phase 0 (saves 2-3 hours), but risk refactoring later

### When to Use Comprehensive Approach
- Team collaboration (shared understanding)
- Regulatory/compliance calculations
- Ambiguous source documents
- Zero error tolerance
- Audit trail required
- **Time invested**: Phase 0 takes 2-4 hours, but eliminates refactoring (saves 10-20 hours)

### Phase 0 ROI Calculation

**Scenario**: 25 queries, 15 ambiguities

**Without Phase 0**:
- Discover ambiguities during implementation: 15 × 30 min = 7.5 hours
- Refactor dependent queries: 15 × 45 min = 11.25 hours
- **Total**: 18.75 hours

**With Phase 0**:
- Resolve ambiguities upfront: 15 × 10 min = 2.5 hours
- Generate artifacts: 1 hour
- Implementation (no refactoring needed): 0 hours
- **Total**: 3.5 hours

**Savings**: 15.25 hours (81% reduction)

### Task Breakdown Decision Tree

```
Does difficulty ≥ 7?
├─ YES → MUST break down
└─ NO → Check risk factors
    ├─ High error surface (≥7) AND high regulatory precision (≥7)?
    │   └─ YES → SHOULD break down
    └─ Multiple complex dependencies (depth ≥6)?
        └─ YES → CONSIDER breaking down
        └─ NO → Work directly
```
