# Power Query Template Usage Example

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
