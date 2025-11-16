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
Complete walkthrough showing how to bootstrap a new Power Query project using this template. Includes both minimal and comprehensive approaches with real-world Phase 0 workflow.

---

## Scenario: EU Battery Regulation Carbon Footprint Calculator

**Project Goal**: Implement Carbon Footprint Formula (CFF) calculation per Article 7 of EU Battery Regulation 2023/1542.

**Context**:
- Regulatory compliance project (automotive industry)
- Source document: 50-page EU Delegated Act with legal language
- Multiple ambiguous calculation steps
- Zero error tolerance (market access depends on compliance)
- Team of 2 developers + 1 domain expert

---

## Approach Decision: Minimal vs. Comprehensive

### Decision Matrix

| Factor | Minimal | Comprehensive |
|--------|---------|---------------|
| Source document ambiguity | Low | **High** ✓ |
| Regulatory requirements | None/low | **High** ✓ |
| Team size | Solo | **Multi-person** ✓ |
| Error tolerance | Medium/high | **Zero** ✓ |
| Project duration | <1 week | **Multi-week** ✓ |
| Need for audit trail | No | **Yes** ✓ |

**Decision**: **Comprehensive approach** (Phase 0 workflow)

**Rationale**: Source document has ambiguous legal language, high regulatory stakes, and multi-person team needs shared variable definitions.

---

## Part 1: Project Bootstrapping

### Step 1: Copy Template to New Project

```bash
# Clone or copy the template repository
cp -r /path/to/claude_code_environment/templates/power-query ~/projects/battery-cff-calc

# Navigate to new project
cd ~/projects/battery-cff-calc
```

### Step 2: Add Source Documents

```bash
# Add calculation method documents
cp ~/Documents/EU-Battery-Regulation-Delegated-Act.pdf calculation-docs/
cp ~/Documents/ISO-22628-Carbon-Footprint.pdf calculation-docs/

# Add Excel files with obfuscated/dummy data
cp ~/Documents/battery-data-template.xlsx excel-files/
```

### Step 3: Customize Overview

Edit `.claude/context/overview.md`:

```markdown
# EU Battery CFF Calculator

## Project Goals
Implement Carbon Footprint Formula (CFF) calculation per Article 7 of EU Battery Regulation 2023/1542 for automotive lithium-ion batteries.

## Calculation Methods
1. **Primary**: EU Delegated Act Article 7 - Carbon footprint of battery
2. **Supporting**: ISO 22628:2002 - Road vehicles, recyclability and recoverability

## Data Sources
- Battery production data (materials, masses, manufacturing location)
- Emission factors database (IPCC, Ecoinvent)
- Recycled content declarations (supplier-provided)
- Pre-consumer scrap records
- Post-consumer scrap records

## Special Requirements
- Regulatory compliance (EU market access)
- Audit trail required
- Calculation must be traceable to source documents
- Zero error tolerance for regulatory submission

## Constraints
- Excel-based (Power Query in Excel)
- Client requires Excel workbook deliverable
- Data contains proprietary information (must use obfuscated sample data)
- Timeline: 6 weeks to implementation, 2 weeks buffer for validation
```

---

## Part 2: Phase 0 Workflow

### Phase 0 Overview

Phase 0 front-loads all ambiguity resolution **before** coding begins. This prevents back-and-forth interpretation questions during implementation.

**Goals**:
1. Extract all ambiguities from source documents
2. Resolve ambiguities interactively with domain expert
3. Generate shared artifacts (glossary, assumptions, data contracts)
4. Create initial task breakdown

**Time Investment**: 4-8 hours (saves 20-40 hours of rework)

---

### Step 1: Initialize Project

Run the initialize command in Claude Code:

```
@.claude/commands/initialize-project.md
```

**What it does**:
1. Reads all PDFs in `calculation-docs/`
2. Analyzes calculation methods
3. Identifies ambiguities
4. Generates `ambiguity-report.md`

**Example Output** (`.claude/reference/ambiguity-report.md`):

```markdown
# Ambiguity Report - EU Battery CFF Calculation

**Generated**: 2025-01-15
**Source Documents**: 2 files analyzed

## Ambiguities Found: 23

### Ambiguity 1: Scope of "Pre-Consumer Scrap"
**Location**: Delegated Act, Article 7, paragraph 2(a)

**Issue**: Article refers to "manufacturing scrap incorporated back into production" but does not specify:
- Whether scrap from external suppliers counts
- Time limit for scrap reincorporation
- Whether production test waste counts as scrap

**Possible Interpretations**:
A. Only scrap generated and reused within same facility
B. Scrap from any supplier if reused in battery production
C. Any manufacturing waste if documented and traceable

**Impact**: Affects recycled content percentage calculation
**Regulatory Risk**: High (audit target)

---

### Ambiguity 2: Emission Factor Selection Hierarchy
**Location**: Delegated Act, Annex II, Section 3.1

**Issue**: Multiple emission factor databases referenced without clear precedence:
- IPCC 2021 Guidelines
- Ecoinvent v3.8
- Manufacturer-specific declarations

**Possible Interpretations**:
A. Use IPCC by default, fallback to Ecoinvent
B. Use most conservative (highest) value
C. Use manufacturer data if available and verified
D. Use Ecoinvent primary, IPCC secondary

**Impact**: Affects total emissions calculation
**Regulatory Risk**: Medium (methodology question)

---

[...21 more ambiguities...]
```

**Status Update**: `.claude/tasks/_phase-0-status.md` now shows:

```markdown
- [x] Step 1: Initialize project (23 ambiguities found)
- [ ] Step 2: Resolve ambiguities (0/23 resolved)
- [ ] Step 3: Generate artifacts
- [ ] Step 4: Extract queries
```

---

### Step 2: Resolve Ambiguities

Run the resolution command (interactive):

```
@.claude/commands/resolve-ambiguities.md
```

**What it does**:
1. Presents 5 ambiguities at a time
2. User discusses with domain expert
3. Records interpretation decision
4. Updates `assumptions.md`
5. Tracks progress in `_phase-0-status.md`

**Example Interaction**:

```
Claude Code presents:

=== Ambiguity Batch 1 (5 of 23) ===

**Ambiguity 1: Scope of "Pre-Consumer Scrap"**

Possible interpretations:
A. Only scrap generated and reused within same facility
B. Scrap from any supplier if reused in battery production
C. Any manufacturing waste if documented and traceable

Which interpretation should we use? (Or provide custom interpretation)
```

**User Response**:

```
After discussing with compliance team:

Interpretation B with additional constraint: Scrap from external suppliers counts
ONLY if:
1. Supplier provides emission factor documentation
2. Scrap is chemically equivalent to virgin material
3. Traceability documentation exists

Rationale: Aligns with Article 7(2)(b) requirement for "verifiable recycled content"
```

**Claude Code Records** (in `.claude/context/assumptions.md`):

```markdown
## Assumption 1: Pre-Consumer Scrap Scope

**Source**: EU Battery Regulation Delegated Act, Article 7(2)(a)

**Ambiguity**: Definition of "manufacturing scrap" scope unclear

**Decision**: Scrap from any supplier (internal or external) counts as recycled content if:
1. Supplier provides emission factor documentation
2. Material is chemically equivalent to virgin material
3. Traceability documentation exists

**Rationale**:
- Aligns with Article 7(2)(b) "verifiable recycled content" requirement
- Approved by compliance team (2025-01-15)
- Enables broader sourcing of recycled materials while maintaining audit trail

**Implementation Impact**:
- Add validation rules for supplier documentation
- Require chemical equivalence certificate in data contract
- Create traceability_doc column in scrap table
```

**Progress Update**: After resolving all 23 ambiguities (took ~3 hours with domain expert):

```markdown
- [x] Step 1: Initialize project (23 ambiguities found)
- [x] Step 2: Resolve ambiguities (23/23 resolved)
- [ ] Step 3: Generate artifacts
- [ ] Step 4: Extract queries
```

---

### Step 3: Generate Artifacts

Run the generation command:

```
@.claude/commands/generate-artifacts.md
```

**What it does**:
1. Reads resolved ambiguities from `assumptions.md`
2. Generates glossary (variable dictionary)
3. Generates data contracts (expected schemas)
4. Generates query manifest (what each query does)
5. Generates dependency graph (query execution order)
6. Creates initial task breakdown
7. Updates `CLAUDE.md` for Phase 1

**Example Output 1** (`.claude/context/glossary.md`):

```markdown
# Variable Glossary

Auto-generated from resolved ambiguities. Every variable name, type, unit, and source.

## Material Data Variables

| Concept | Variable Name | Type | Unit | Source | Notes |
|---------|--------------|------|------|--------|-------|
| Battery total mass | BatteryTotalMass | Decimal | kg | Manufacturer declaration | Assumption 3 |
| Cathode active material mass | CathodeActiveMaterialMass | Decimal | kg | Component specification | - |
| Pre-consumer scrap mass | PreConsumerScrapMass | Decimal | kg | Scrap documentation | Assumption 1 |
| Post-consumer scrap mass | PostConsumerScrapMass | Decimal | kg | Recycling certificate | Assumption 4 |
| Recycled content share | RecycledContentShare | Decimal | % (0-1) | Calculated (Art. 7(2)) | Formula in Assumption 5 |

## Emission Factor Variables

| Concept | Variable Name | Type | Unit | Source | Notes |
|---------|--------------|------|------|--------|-------|
| Material emission factor | MaterialEmissionFactor | Decimal | kg CO2e/kg | IPCC/Ecoinvent | Assumption 2 |
| Manufacturing emission factor | ManufacturingEmissionFactor | Decimal | kg CO2e/kWh | IPCC 2021 | Assumption 8 |
| Transport emission factor | TransportEmissionFactor | Decimal | kg CO2e/tkm | ISO 22628 default | - |

[...40 more variables...]
```

**Example Output 2** (`.claude/reference/data-contracts.md`):

```markdown
# Data Contracts

Expected schemas for each Power Query.

## Bronze Layer Queries

### Bronze_Source_BatteryData

**Purpose**: Import raw battery data from supplier files

**Output Schema**:
- battery_id: text, non-null, unique, format: "BAT-YYYYMMDD-NNNN"
- total_mass_kg: decimal, non-null, range: 100-800 (automotive batteries)
- manufacturing_location: text, non-null, values: {EU, US, CN, JP, KR}
- production_date: date, non-null, range: 2020-present

**Validation Rules**:
- No duplicate battery_id
- Total mass reasonable for automotive use
- Production date not in future

**Source**: excel-files/battery-data-template.xlsx, Sheet: "BatteryMaster"

---

### Bronze_Source_EmissionFactors

**Purpose**: Import emission factors from approved databases

**Output Schema**:
- material_type: text, non-null, references MaterialClassification
- emission_factor_kg_co2e_per_kg: decimal, non-null, range: 0-100
- database_source: text, non-null, values: {IPCC2021, Ecoinvent3.8, ManufacturerVerified}
- data_quality_tier: integer, non-null, range: 1-3 (1=highest quality)

**Validation Rules**:
- Emission factors from Assumption 2 hierarchy
- Data quality tier per Assumption 7
- All material types have at least one emission factor

**Source**: excel-files/emission-factors.xlsx, Sheet: "EmissionFactors"

[...10 more queries...]
```

**Example Output 3** (`.claude/reference/dependency-graph.md`):

```markdown
# Query Dependency Graph

```
                    ┌─────────────────────────────┐
                    │  Gold_Report_CFP_Summary    │
                    │  (Final regulatory report)  │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
         ┌──────────▼──────────┐      ┌───────────▼──────────┐
         │ Gold_Calculate_CFF   │      │ Gold_Validate_Data   │
         │ (Article 7 formula)  │      │ (Compliance checks)  │
         └──────────┬───────────┘      └──────────────────────┘
                    │
         ┌──────────┴───────────────────────┐
         │                                  │
    ┌────▼──────────────┐     ┌────────────▼──────────────┐
    │ Silver_Materials   │     │ Silver_Emissions          │
    │ (Classified+calc)  │     │ (Factors applied)         │
    └────┬───────────────┘     └────────────┬──────────────┘
         │                                  │
         │        ┌─────────────────────────┴──────┐
         │        │                                │
    ┌────▼────────▼────┐   ┌──────────────────┐  ┌▼────────────────────┐
    │ Bronze_Materials  │   │ Bronze_Scrap     │  │ Bronze_EmissionFact │
    │ (Raw battery data)│   │ (Recycled data)  │  │ (Factors database)  │
    └───────────────────┘   └──────────────────┘  └─────────────────────┘
```

**Execution Order**:
1. Bronze layer (parallel): Materials, Scrap, EmissionFactors
2. Silver layer: Silver_Materials, Silver_Emissions
3. Gold layer: Gold_Calculate_CFF, Gold_Validate_Data
4. Report layer: Gold_Report_CFP_Summary
```

**Example Output 4** (Initial tasks generated in `.claude/tasks/task-*.json`):

```markdown
# Generated Tasks (12 total)

## Bronze Layer (4 tasks)
- Task 1: Create Bronze_Source_BatteryData (diff: 3)
- Task 2: Create Bronze_Source_EmissionFactors (diff: 4)
- Task 3: Create Bronze_Source_ScrapData (diff: 4)
- Task 4: Create Bronze_Source_MaterialClassification (diff: 3)

## Silver Layer (3 tasks)
- Task 5: Create Silver_Materials_Classified (diff: 5)
- Task 6: Create Silver_Emissions_Applied (diff: 6)
- Task 7: Create Silver_Scrap_Consolidated (diff: 5)

## Gold Layer (3 tasks)
- Task 8: Implement Gold_Calculate_CFF (diff: 9) 🔴 BREAKDOWN REQUIRED
- Task 9: Create Gold_Validate_Compliance (diff: 7) 🔴 BREAKDOWN REQUIRED
- Task 10: Create Gold_Audit_Trail (diff: 6)

## Reporting (2 tasks)
- Task 11: Create Gold_Report_CFP_Summary (diff: 5)
- Task 12: Create documentation and validation tests (diff: 6)
```

**Phase 0 Complete**: `.claude/tasks/_phase-0-status.md` shows:

```markdown
- [x] Step 1: Initialize project (23 ambiguities found)
- [x] Step 2: Resolve ambiguities (23/23 resolved)
- [x] Step 3: Generate artifacts (glossary, contracts, manifest, tasks created)
- [ ] Step 4: Extract queries
```

---

### Step 4: Extract Queries (First Time)

Run the extraction command:

```
@.claude/commands/extract-queries.md
```

**What it does**:
1. Scans Excel files in `excel-files/`
2. Extracts Power Query M code from each query
3. Saves as individual `.m` files in `power-query/`
4. Creates git commit
5. Enables watch mode (auto-extracts on Excel changes)

**Example Output**:

```
Extracted 8 queries from battery-data-template.xlsx:
- Bronze_Source_BatteryData.m (156 lines)
- Bronze_Source_EmissionFactors.m (89 lines)
- Bronze_Source_ScrapData.m (112 lines)
...

Git commit created: "Initial Power Query extraction from Excel"

Watch mode enabled:
- Monitoring excel-files/ for changes
- Will auto-extract and commit when Excel files saved
- Run sync-tasks.md after making changes
```

**Phase 0 Complete**:

```markdown
- [x] Step 1: Initialize project
- [x] Step 2: Resolve ambiguities
- [x] Step 3: Generate artifacts
- [x] Step 4: Extract queries

Phase 0 Complete! Ready for Phase 1 (implementation).
```

**Time Investment**: ~5 hours total (including domain expert discussions)

---

## Part 3: Phase 1 - Implementation

Phase 1 uses the artifacts from Phase 0 to implement tasks systematically.

### Task Selection: Start with Bronze Layer

**Why Bronze first?**
- No dependencies (can implement in parallel)
- Validates data contracts
- Provides foundation for Silver layer

**Task chosen**: Task 1 - Create Bronze_Source_BatteryData (difficulty 3)

---

### Implementing a Task

Run the complete-task command:

```
@.claude/commands/complete-task.md 1
```

**What it does**:
1. Loads task-1.json
2. Loads relevant context:
   - glossary.md (variable definitions)
   - assumptions.md (interpretation decisions)
   - data-contracts.md (expected schema for this query)
   - llm-pitfalls.md (common mistakes checklist)
   - standards/power-query.md (M code conventions)
3. Implements the query
4. Validates schema against data contract
5. Updates task status to "Finished"
6. Commits changes
7. Updates task-overview.md

**Example Implementation** (Bronze_Source_BatteryData.m):

```m
// Bronze_Source_BatteryData
// Purpose: Import raw battery data from supplier files
// Data Contract: .claude/reference/data-contracts.md
// See glossary: BatteryTotalMass, ManufacturingLocation

let
    // Step 1: Load from Excel
    Source = Excel.Workbook(
        File.Contents("excel-files/battery-data-template.xlsx"),
        null,
        true
    ),

    // Step 2: Get BatteryMaster sheet
    BatteryMaster_Sheet = Source{[Item="BatteryMaster",Kind="Sheet"]}[Data],

    // Step 3: Promote headers
    PromotedHeaders = Table.PromoteHeaders(BatteryMaster_Sheet, [PromoteAllScalars=true]),

    // Step 4: Set data types per data contract
    TypedColumns = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"battery_id", type text},
            {"total_mass_kg", type number},
            {"manufacturing_location", type text},
            {"production_date", type date}
        }
    ),

    // Step 5: Validate per data contract
    // - No duplicate battery_id
    CheckDuplicates = if List.Count(TypedColumns[battery_id]) <>
                         List.Count(List.Distinct(TypedColumns[battery_id]))
                      then error Error.Record(
                          "Validation Failed",
                          "Duplicate battery_id found in source data",
                          "Check BatteryMaster sheet for duplicates"
                      )
                      else TypedColumns,

    // Step 6: Range validation (total_mass_kg: 100-800 kg for automotive)
    RangeValidation = Table.SelectRows(
        CheckDuplicates,
        each [total_mass_kg] >= 100 and [total_mass_kg] <= 800
    ),

    // Step 7: Future date validation (production_date not in future)
    DateValidation = Table.SelectRows(
        RangeValidation,
        each [production_date] <= DateTime.LocalNow()
    ),

    // Step 8: Manufacturing location validation (from Assumption 11)
    ValidLocations = {"EU", "US", "CN", "JP", "KR"},
    LocationValidation = Table.SelectRows(
        DateValidation,
        each List.Contains(ValidLocations, [manufacturing_location])
    )

in
    LocationValidation
```

**Validation Check** (against data contract):

```
Schema Validation: ✅ Pass
- battery_id: text ✓
- total_mass_kg: decimal ✓ (range: 100-800)
- manufacturing_location: text ✓ (valid values)
- production_date: date ✓ (not future)

Uniqueness Check: ✅ Pass
- battery_id unique

Row Count: 156 rows imported
Errors: 0
```

**Git Commit**:

```
commit a3f4d8e
Task 1 Complete: Bronze_Source_BatteryData

- Implemented Bronze_Source_BatteryData.m
- All validation rules from data contract applied
- Schema matches contract
- 156 battery records imported
- Zero errors
```

**Task Status Update** (task-1.json):

```json
{
  "id": "1",
  "title": "Create Bronze_Source_BatteryData",
  "status": "Finished",
  "notes": "Implemented per data contract. All validations pass. 156 rows imported."
}
```

---

### Handling High-Difficulty Tasks: Breakdown Required

**Task 8**: Implement Gold_Calculate_CFF (difficulty 9)

This task is flagged 🔴 BREAKDOWN REQUIRED.

Run the breakdown command:

```
@.claude/commands/breakdown.md 8
```

**What it does**:
1. Analyzes task-8.json
2. Reads data contract for Gold_Calculate_CFF
3. Reads Article 7 formula from assumptions.md
4. Scores across 5 dimensions:
   ```
   Query Dependency Depth:    7  (needs Silver_Materials, Silver_Emissions, Silver_Scrap)
   Formula Complexity:        8  (multi-step regulatory formula)
   Error Surface:             8  (nulls, divisions by zero, range checks)
   Regulatory Precision:     10  (EU audit target)
   Performance Impact:        5  (medium dataset)

   Average: (7+8+8+10+5)/5 = 7.6
   Context Multiplier: 1.3x (3 dependencies)
   Final: 7.6 × 1.3 = 9.9 → 10
   ```
5. Creates 7 subtasks (each ≤6 difficulty)
6. Updates parent task to "Broken Down (0/7 done)"

**Generated Subtasks**:

```markdown
## Task 8: Implement Gold_Calculate_CFF
**Status**: Broken Down (0/7 done)
**Original Difficulty**: 9

### Subtasks Created:

**Task 8.1**: Extract and validate inputs (diff: 4)
- Load Silver_Materials, Silver_Emissions, Silver_Scrap
- Validate schemas match data contracts
- Check for nulls in required fields
- Error if validation fails

**Task 8.2**: Implement material classification routing (diff: 5)
- Route materials by type (Assumption 6: cathode, anode, electrolyte, casing)
- Apply material-specific emission factors
- Handle unknown material types per Assumption 12

**Task 8.3**: Calculate pre-consumer scrap component (diff: 4)
- Implement Article 7(2)(a) pre-consumer scrap formula
- Apply Assumption 1 scope rules
- Validate traceability documentation exists
- Calculate emission reduction from scrap

**Task 8.4**: Calculate post-consumer scrap component (diff: 4)
- Implement Article 7(2)(b) post-consumer scrap formula
- Apply Assumption 4 verification rules
- Validate recycling certificates
- Calculate emission reduction from scrap

**Task 8.5**: Combine components per Article 7 formula (diff: 5)
- Add material emissions + manufacturing emissions + transport emissions
- Subtract pre-consumer scrap emissions
- Subtract post-consumer scrap emissions
- Calculate final CFF value in kg CO2e per kWh

**Task 8.6**: Add compliance flag and validation (diff: 4)
- Compare CFF to regulatory thresholds (Assumption 15)
- Set compliance_flag: PASS/FAIL
- Add validation warnings for edge cases
- Check result reasonableness

**Task 8.7**: Output validation and audit trail (diff: 3)
- Verify output schema matches data contract
- Add calculation_date, assumptions_version columns
- Create audit trail with intermediate values
- Log all assumption IDs used
```

**Implementation**: Now complete subtasks 8.1 through 8.7 sequentially using `complete-task.md`.

As each subtask finishes, parent task progress updates:
- After 8.1: "Broken Down (1/7 done)"
- After 8.2: "Broken Down (2/7 done)"
- ...
- After 8.7: **Automatically transitions to "Finished"**

---

## Part 4: Results and Benefits

### Time Comparison

**Without Phase 0** (estimated):
- Start coding immediately: +0 hours
- Hit first ambiguity: +0.5 hours → context switch to ask domain expert
- Hit second ambiguity: +1 hour → another context switch
- Realize inconsistent variable names: +2 hours → refactor all queries
- Regulatory interpretation error found in QA: +8 hours → rework calculations
- **Total**: ~35-45 hours (with high rework risk)

**With Phase 0**:
- Phase 0 (front-load ambiguities): +5 hours
- Implementation (with glossary & data contracts): +18 hours
- QA (minimal issues, clear audit trail): +2 hours
- **Total**: ~25 hours (predictable, low rework risk)

**Time Saved**: 10-20 hours
**Rework Risk**: Eliminated

---

### Artifacts Created

**Phase 0 Outputs**:
1. `.claude/context/glossary.md` - 47 variables defined
2. `.claude/context/assumptions.md` - 23 interpretation decisions documented
3. `.claude/reference/data-contracts.md` - 12 queries with schemas
4. `.claude/reference/query-manifest.md` - Purpose of each query
5. `.claude/reference/dependency-graph.md` - Execution order
6. `.claude/tasks/task-*.json` - 12 initial tasks + 7 subtasks from breakdown

**Phase 1 Outputs**:
1. `power-query/*.m` - 12 Power Query M files (version controlled)
2. `excel-files/battery-cff-calc.xlsx` - Excel workbook with all queries
3. Git history - Full audit trail of all changes

---

### Regulatory Audit Readiness

**Auditor Question**: "How did you interpret 'pre-consumer scrap' in Article 7(2)(a)?"

**Answer** (referencing `.claude/context/assumptions.md`):

> "Assumption 1, documented 2025-01-15:
>
> We interpret 'manufacturing scrap' to include scrap from external suppliers if:
> 1. Supplier provides emission factor documentation
> 2. Material is chemically equivalent to virgin material
> 3. Traceability documentation exists
>
> Rationale: Aligns with Article 7(2)(b) 'verifiable recycled content' requirement.
> Approved by compliance team (meeting minutes attached).
>
> Implementation: See Bronze_Source_ScrapData.m lines 45-67 for validation logic."

**Result**: Clear audit trail from regulation → interpretation → code implementation.

---

## Part 5: Minimal Approach Example

For comparison, here's the same project with **minimal approach** (no Phase 0):

### Minimal Setup

```bash
# Copy minimal CLAUDE.md
cp templates/power-query/CLAUDE-minimal.md ~/projects/battery-cff-calc/CLAUDE.md

# Copy critical rules template
cp templates/power-query/context/critical_rules.md ~/projects/battery-cff-calc/docs/

# Create tasks manually as you go
# No glossary, no assumptions documentation, no data contracts
```

### When Minimal Makes Sense

Use minimal approach when:
- ✅ Source documents are clear and unambiguous
- ✅ Solo developer (no shared context needed)
- ✅ Low regulatory stakes (internal use only)
- ✅ Short project (<1 week)
- ✅ Existing PQ project just needs documentation

**Example Minimal Use Case**:
> "Add data refresh automation to existing Excel Power Query workbook. Queries already implemented and tested, just need to document and version control."

---

## Summary

### Comprehensive Approach (Phase 0)

**Best for**:
- Regulatory/compliance projects
- Ambiguous source documents
- Multi-person teams
- High regulatory stakes
- Multi-week projects

**Benefits**:
- Eliminates interpretation ambiguity
- Shared variable definitions
- Clear audit trail
- Predictable timeline
- Low rework risk

**Time Investment**:
- Phase 0: 4-8 hours
- Pays back: 10-20 hours saved in rework

### Minimal Approach

**Best for**:
- Clear, unambiguous requirements
- Solo developer
- Low stakes (internal use)
- Short duration (<1 week)
- Existing projects needing docs

**Benefits**:
- Fast startup
- Low overhead
- Simple structure

**Trade-offs**:
- Higher rework risk
- No audit trail
- Interpretation questions during implementation
- Difficult for team collaboration

---

## Next Steps

After completing this usage example:
1. Review QUICKSTART.md for faster setup
2. Read SETUP-GUIDE.md for detailed configuration
3. Check FILE-MANIFEST.md to understand all template files
4. Explore `.claude/commands/` for available workflows
5. Start your project and iterate on the template
After completing this example project, you would have:

1. ✅ Complete Power Query implementation (12 queries)
2. ✅ Full audit trail (assumptions, glossary, git history)
3. ✅ Regulatory compliance documentation
4. ✅ Version-controlled M code
5. ✅ Excel workbook deliverable
6. ✅ Clear variable definitions for team
7. ✅ Reusable patterns for similar projects

**Reuse for next project**:
- Copy `.claude/context/llm-pitfalls.md` (regulatory checklist)
- Reuse Bronze-Silver-Gold architecture pattern
- Reference difficulty scoring for similar tasks
- Adapt Phase 0 workflow for new regulations
