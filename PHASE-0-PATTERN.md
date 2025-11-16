# Phase 0: Ambiguity Resolution Pattern

## Overview

**Phase 0** is a front-loading workflow pattern that resolves all ambiguities, defines all variables, and generates project artifacts **before** implementation begins. It prevents costly refactoring caused by discovering ambiguities mid-implementation.

## Problem Statement

Traditional development workflow:
```
Requirements → Start coding → Discover ambiguity → Ask questions → Refactor → Discover another → Refactor again...
```

**Cost**: Each ambiguity discovered during implementation triggers refactoring of dependent code. In complex projects (regulatory compliance, scientific calculations, legal implementations), this can cause:
- 5-10x implementation time vs. estimated
- Inconsistent interpretations across modules
- Missing audit trail for decisions
- Team confusion about shared definitions

## Phase 0 Solution

```
Requirements → Resolve ALL ambiguities → Generate artifacts → Implement (no refactoring)
```

**Benefit**:
- All decisions made upfront with full context
- Documented rationale for every interpretation
- Shared glossary eliminates miscommunication
- Implementation proceeds smoothly (no surprises)
- **ROI**: 70-85% reduction in total project time for high-ambiguity domains

## When to Use Phase 0

### High-Value Scenarios (MUST use)
- Regulatory/compliance implementations (laws, standards, regulations)
- Scientific calculations from research papers
- Legal document automation
- Financial calculations with audit requirements
- Medical/pharmaceutical protocols
- Engineering standards implementation

### Indicators
✅ Use Phase 0 if 3+ apply:
- [ ] Source documents use ambiguous language (legal, regulatory, academic)
- [ ] Multiple interpretations possible for key requirements
- [ ] Team needs shared understanding of definitions
- [ ] Zero error tolerance (compliance, safety, financial)
- [ ] Audit trail required for decisions
- [ ] Source documents reference other documents (circular dependencies)
- [ ] Domain experts needed to clarify requirements

❌ Skip Phase 0 if all apply:
- [ ] Requirements are crystal clear
- [ ] Solo developer with full domain knowledge
- [ ] Prototype/experiment (not production)
- [ ] Errors are low-consequence
- [ ] No external documentation to interpret

### Domain-Specific Examples

| Domain | When to Use Phase 0 | Example |
|--------|---------------------|---------|
| **Regulatory** | Always | EU Battery Regulation, ISO standards, tax law |
| **Scientific** | Complex formulas | Climate models, pharmacokinetics, physics simulations |
| **Legal** | Contract automation | SLA enforcement, compliance checking, policy implementation |
| **Financial** | Audit required | Investment calculations, risk models, accounting standards |
| **Data Engineering** | Complex transformations | Multi-source reconciliation, regulatory reporting |
| **Medical** | Clinical protocols | Dosage calculations, diagnostic criteria, treatment pathways |

## Phase 0 Workflow

### Four-Step Process

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0: Ambiguity Resolution (Before Implementation)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: ANALYZE                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Command: initialize-project                              │  │
│  │ Input: Source documents (PDFs, specs, standards)         │  │
│  │ Output: Ambiguity report                                 │  │
│  │                                                           │  │
│  │ - Scan all source documents                              │  │
│  │ - Extract requirements, formulas, definitions            │  │
│  │ - Identify ambiguities (unclear, contradictory, missing) │  │
│  │ - Structure as answerable questions                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  Step 2: RESOLVE                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Command: resolve-ambiguities                             │  │
│  │ Input: Ambiguity report                                  │  │
│  │ Output: Assumptions document + Glossary stubs            │  │
│  │                                                           │  │
│  │ - Present ambiguities in batches (5 at a time)           │  │
│  │ - User makes decisions with rationale                    │  │
│  │ - Record all decisions and reasoning                     │  │
│  │ - Create glossary entries for new terms                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  Step 3: GENERATE                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Command: generate-artifacts                              │  │
│  │ Input: Assumptions + Source documents                    │  │
│  │ Output: 4-5 artifacts (see below)                        │  │
│  │                                                           │  │
│  │ - Complete glossary (all variables defined)              │  │
│  │ - Data contracts (schemas, validation rules)             │  │
│  │ - Component manifest (what each component does)          │  │
│  │ - Dependency graph (execution order)                     │  │
│  │ - Initial task breakdown                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  Step 4: EXTRACT/INITIALIZE                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Command: Domain-specific initialization                  │  │
│  │ Input: Generated artifacts                               │  │
│  │ Output: Project structure ready for implementation       │  │
│  │                                                           │  │
│  │ Examples:                                                 │  │
│  │ - Power Query: Extract .m files from Excel               │  │
│  │ - Python: Generate module structure + stubs              │  │
│  │ - SQL: Create schema definition files                    │  │
│  │ - API: Generate OpenAPI spec + endpoint stubs            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Implementation Phase (No refactoring needed!)                   │
│ - All ambiguities resolved                                      │
│ - All variables defined                                         │
│ - Work proceeds smoothly using artifacts                        │
└─────────────────────────────────────────────────────────────────┘
```

## Command Structure

### Command 1: initialize-project.md

**Purpose**: Analyze source documents and identify all ambiguities

**Template Structure**:
```markdown
# Initialize Project Command

## Purpose
Analyze source documents (PDFs, specifications, standards) and identify all ambiguities, unclear definitions, and missing information that must be resolved before implementation.

## Context Required
- Source documents in calculation-docs/ (or equivalent directory)
- Project overview (.claude/context/overview.md) with regulatory/domain context

## Process

### 1. Scan Source Documents
Read all files in calculation-docs/:
- PDFs of regulations, standards, specifications
- Reference materials
- Example calculations or templates

### 2. Extract Requirements
For each document, identify:
- Calculation formulas and methods
- Variable definitions
- Data requirements
- Validation rules
- Edge case handling
- Referenced external documents

### 3. Identify Ambiguities
Flag items that are:
- **Unclear**: Vague language, multiple interpretations possible
- **Contradictory**: Different sections conflict
- **Missing**: Referenced but not defined
- **Implicit**: Assumptions not stated explicitly
- **Circular**: Definition depends on itself or creates loop

### 4. Structure as Questions
For each ambiguity, create structured entry:
- **ID**: AMB-001, AMB-002, etc.
- **Location**: Document name, section, article, page
- **Text**: Exact quote from source
- **Ambiguity**: What is unclear
- **Impact**: What this affects in implementation
- **Questions**: Specific questions to resolve it

## Output Location
`.claude/reference/ambiguity-report.md`

## Example Output Format

```markdown
# Ambiguity Report

## Summary
- Total ambiguities found: 47
- High priority: 12
- Medium priority: 23
- Low priority: 12

## High-Priority Ambiguities

### AMB-001: [Short description]
**Location**: [Document name, section]
**Text**: "[Exact quote]"
**Ambiguity**: [What is unclear]
**Impact**: [What this affects]
**Questions**:
1. [Specific question]
2. [Specific question]

[... more ambiguities ...]
```

## Domain Adaptations

### Regulatory/Compliance
Focus on:
- Legal language interpretation
- Allocation methods (when multiple options exist)
- System boundaries (what's included/excluded)
- Calculation methods (when regulation allows choices)

### Scientific/Research
Focus on:
- Formula notation ambiguities
- Implicit assumptions in papers
- Missing experimental details
- Unit conversions and conventions

### Legal/Contract
Focus on:
- Clause interpretation
- Undefined terms
- Conflicting provisions
- Implicit requirements
```

### Command 2: resolve-ambiguities.md

**Purpose**: Interactive session to resolve all ambiguities with documented rationale

**Template Structure**:
```markdown
# Resolve Ambiguities Command

## Purpose
Present ambiguities in manageable batches and guide user through resolution with documented rationale. Create audit trail of all decisions.

## Context Required
- Ambiguity report (.claude/reference/ambiguity-report.md)
- Project overview for domain context
- Access to domain expert or user with decision authority

## Process

### 1. Load Ambiguity Report
Read .claude/reference/ambiguity-report.md
Count total ambiguities
Calculate number of batches (5 ambiguities per batch)

### 2. Present Batch
For each batch of 5 ambiguities:

```
AMBIGUITY BATCH [X]/[Y]

AMB-[ID]: [Short description]
Location: [Document reference]
Text: "[Quote]"
Ambiguity: [What's unclear]

[If analysis suggests options, present as multiple choice:]
Options:
A) [Interpretation 1] - [Implications]
B) [Interpretation 2] - [Implications]
C) [Interpretation 3] - [Implications]
D) Other (user specifies)

[If open-ended:]
Question: [Specific question to resolve]

Your decision: ___________

Rationale: ___________
```

### 3. Record Decisions
For each resolved ambiguity:

**In .claude/context/assumptions.md**:
- Add assumption entry with ID, decision, rationale
- Reference source ambiguity
- Note any dependencies or implications

**In .claude/context/glossary.md** (if new term introduced):
- Create stub entry for variable/term
- Link to assumption
- Mark for completion in generate-artifacts step

### 4. Validate Completeness
After all batches:
- Review for consistency (no contradictory decisions)
- Check for new ambiguities introduced by decisions
- Confirm all high-priority items resolved

## Output Location
- `.claude/context/assumptions.md` (decisions with rationale)
- `.claude/context/glossary.md` (stub entries for new terms)

## Example Interaction

**Batch 1**:
```
AMB-001: Allocation method for shared manufacturing

Options:
A) Physical allocation (energy per kg) - More accurate but requires detailed metering
B) Economic allocation (production cost) - Pragmatic but less precise
C) Hybrid (physical for direct, economic for indirect) - Balanced approach

Your decision: C

Rationale: Physical allocation for direct energy use provides accuracy where
measurement is straightforward. Economic allocation for shared overhead costs
is pragmatic where metering is impractical. This aligns with regulatory
guidance on "best available data."
```

**Recorded in assumptions.md**:
```markdown
## AMB-001: Allocation Method for Shared Manufacturing

**Decision**: Hybrid allocation method
- Physical causality for direct energy consumption
- Economic causality for shared overhead costs

**Rationale**: Physical allocation provides higher accuracy for directly
metered energy use. Economic allocation is pragmatic for shared costs where
direct measurement is not feasible. This approach aligns with Annex VII
guidance on "best available data" principle.

**Source**: Annex VII, Article 3.2

**Variables Affected**:
- allocation_factor_physical
- allocation_factor_economic
- energy_allocated_kwh

**Queries Affected**:
- Manufacturing_AllocateEnergy
- Manufacturing_CalculateCarbonFootprint
```

## Domain Adaptations

### Regulatory/Compliance
- Emphasize regulatory citations for decisions
- Document conservative vs. aggressive interpretations
- Note compliance risk level for each decision

### Scientific/Research
- Reference literature for standard practices
- Document assumptions that need experimental validation
- Flag decisions that affect reproducibility
```

### Command 3: generate-artifacts.md

**Purpose**: Generate all project artifacts from resolved ambiguities

**Template Structure**:
```markdown
# Generate Artifacts Command

## Purpose
Using resolved ambiguities and assumptions, generate comprehensive project artifacts: glossary, data contracts, component manifest, dependency graph, and initial tasks.

## Context Required
- Assumptions document (.claude/context/assumptions.md)
- Glossary stubs (.claude/context/glossary.md)
- Source documents (calculation-docs/)
- Project overview

## Process

### 1. Complete Glossary
Expand glossary stubs into full definitions:

For each variable/term:
- **Definition**: Clear, unambiguous definition
- **Value**: Literal value, formula, or data source
- **Source**: Where it comes from (document, assumption, data file)
- **Unit**: Physical units or data type
- **Used in**: Which components use this variable
- **Validation**: Constraints, ranges, formats
- **Notes**: Special handling, edge cases

### 2. Generate Data Contracts
For each data source:
- **Schema**: Expected columns, types, required/optional
- **Validation Rules**: Constraints, formats, ranges
- **Consumers**: Which components read this data
- **Quality Checks**: How to validate incoming data
- **Error Handling**: What to do with invalid data

### 3. Create Component Manifest
For each component (query, function, module, endpoint):
- **Purpose**: What it does (single responsibility)
- **Inputs**: Dependencies and data sources
- **Outputs**: Schema of results
- **Transformations**: Logic description
- **Complexity Score**: Using domain-specific difficulty scoring
- **Dependencies**: Upstream components

### 4. Build Dependency Graph
- Map component dependencies
- Identify execution order (stages/layers)
- Flag circular dependencies
- Visualize as text diagram

### 5. Generate Initial Tasks
Create task JSON files:
- One task per component
- Include difficulty score, dependencies
- Add notes referencing glossary, assumptions, data contracts
- Flag tasks requiring breakdown (difficulty ≥7)

## Output Location
- `.claude/context/glossary.md` (completed)
- `.claude/reference/data-contracts.md`
- `.claude/reference/component-manifest.md` (or domain-specific: query-manifest.md, function-manifest.md, etc.)
- `.claude/reference/dependency-graph.md`
- `.claude/tasks/task-*.json`

## Domain Adaptations

### Power Query
- Component manifest → Query manifest
- Dependency graph → Bronze-Silver-Gold layers
- Difficulty scoring → 5-dimension PQ-specific scoring

### Python/API
- Component manifest → Function/endpoint manifest
- Dependency graph → Module import graph
- Difficulty scoring → Cyclomatic complexity + API surface

### SQL
- Component manifest → Table/view/procedure manifest
- Dependency graph → Table lineage
- Difficulty scoring → Query complexity + join depth

### Research/Analysis
- Component manifest → Analysis step manifest
- Dependency graph → Analysis pipeline
- Difficulty scoring → Statistical complexity + data volume
```

### Command 4: [Domain-Specific Initialization]

**Purpose**: Domain-specific setup (varies by project type)

**Examples**:

#### extract-queries.md (Power Query)
```markdown
# Extract Queries Command

Extract Power Query .m files from Excel workbook and save to power-query/
directory for version control.

[See templates/power-query/commands/extract-queries.md for full implementation]
```

#### generate-stubs.md (Python)
```markdown
# Generate Stubs Command

Generate Python module structure with function stubs based on function manifest.

- Create module hierarchy
- Generate stub functions with docstrings from glossary
- Add type hints from data contracts
- Create test file templates
```

#### create-schema.md (SQL)
```markdown
# Create Schema Command

Generate SQL schema definition files from data contracts.

- Create DDL statements for tables
- Add constraints from validation rules
- Generate index definitions
- Create migration scripts
```

## Phase 0 Artifacts Reference

### 1. Ambiguity Report
**File**: `.claude/reference/ambiguity-report.md`
**Created by**: initialize-project
**Purpose**: Catalog all unclear, contradictory, or missing information
**Structure**:
```markdown
# Ambiguity Report

## Summary
[Statistics]

## High-Priority Ambiguities
[Ambiguity entries with ID, location, text, questions]

## Medium-Priority Ambiguities
[...]

## Low-Priority Ambiguities
[...]
```

### 2. Assumptions Document
**File**: `.claude/context/assumptions.md`
**Created by**: resolve-ambiguities
**Purpose**: Audit trail of all decisions with rationale
**Structure**:
```markdown
# Assumptions

## [AMB-ID]: [Description]

**Decision**: [What was decided]
**Rationale**: [Why this decision was made]
**Source**: [Document reference]
**Variables Affected**: [List]
**Components Affected**: [List]
**Compliance Notes**: [If regulatory]
**Risk Level**: [If applicable]
```

### 3. Glossary
**File**: `.claude/context/glossary.md`
**Created by**: resolve-ambiguities (stubs), generate-artifacts (completed)
**Purpose**: Single source of truth for all variable definitions
**Structure**:
```markdown
# Variable Glossary

## [Letter]

### [variable_name]
**Definition**: [Clear definition]
**Value**: [Literal, formula, or source]
**Source**: [Document/assumption/data]
**Unit**: [Units or type]
**Used in**: [Components list]
**Validation**: [Constraints]
**Notes**: [Special handling]
```

### 4. Data Contracts
**File**: `.claude/reference/data-contracts.md`
**Created by**: generate-artifacts
**Purpose**: Schema and validation for all data sources
**Structure**:
```markdown
# Data Contracts

## Source: [filename]

### Expected Schema
| Column | Type | Required | Validation | Example |
|--------|------|----------|------------|---------|
[...]

### Queries/Components Consuming This Source
[List]

### Quality Checks
[Validation rules]

### Error Handling
[What to do with invalid data]
```

### 5. Component Manifest
**File**: `.claude/reference/[domain]-manifest.md` (e.g., query-manifest.md, function-manifest.md)
**Created by**: generate-artifacts
**Purpose**: Catalog of all components with descriptions
**Structure**:
```markdown
# [Component Type] Manifest

## [Layer/Category]

### [component_name]
**Purpose**: [What it does]
**Input**: [Dependencies and sources]
**Output Schema**: [Result structure]
**Dependencies**: [Upstream components]
**Transformations**: [Logic description]
**Complexity**: [Score/10]
```

### 6. Dependency Graph
**File**: `.claude/reference/dependency-graph.md`
**Created by**: generate-artifacts
**Purpose**: Execution order and dependency visualization
**Structure**:
```markdown
# Dependency Graph

## Execution Order

### Stage 1: [Name]
- [component_a]
- [component_b]

### Stage 2: [Name]
- [component_c] (depends: component_a)
[...]

## Visual Representation
[Text diagram showing dependencies]
```

## Integration with Task Management

### Task Creation from Artifacts

After Phase 0, tasks are generated from component manifest:

1. **One task per component**
   ```json
   {
     "id": "5",
     "title": "Implement [component_name]",
     "description": "[From manifest: purpose + transformations]",
     "difficulty": 6,
     "dependencies": ["2", "3"],
     "notes": "References: glossary.md ([variables]), data-contracts.md ([source]), assumptions.md ([AMB-IDs])"
   }
   ```

2. **Automatic breakdown for high difficulty**
   - Tasks with difficulty ≥7 flagged for breakdown
   - Use standard breakdown workflow
   - Subtasks reference same artifacts

3. **Dependency tracking**
   - Dependencies copied from dependency graph
   - Ensures correct implementation order

### Workflow Integration

```
Phase 0 Complete
    ↓
Tasks Generated (task-*.json)
    ↓
For each task:
    ↓
    Difficulty ≥7?
    ├─ YES → /breakdown [task-id]
    │          ↓
    │        Subtasks Created
    │          ↓
    │        Work on Subtasks (/complete-task [subtask-id])
    │          ↓
    │        All Subtasks Done → Parent Auto-Completes
    │
    └─ NO → /complete-task [task-id]
               ↓
             Task Complete
                ↓
             Load Context:
             - glossary.md (variables)
             - assumptions.md (decisions)
             - data-contracts.md (schemas)
             - [component]-manifest.md (description)
             - dependency-graph.md (order)
                ↓
             Implement using artifacts
                ↓
             Mark Finished
```

## Domain-Specific Adaptations

### Power Query / Excel

**Source Documents**: Regulatory PDFs, calculation specifications
**Ambiguities**: Legal language, allocation methods, system boundaries
**Artifacts**:
- Query manifest (Bronze-Silver-Gold layers)
- Dependency graph (query execution order)
- Data contracts (Excel file schemas)
**Initialization**: Extract .m files from Excel
**Difficulty Scoring**: 5-dimension PQ-specific

See: `templates/power-query/` for full implementation

### Python Scientific Computing

**Source Documents**: Research papers, experimental protocols
**Ambiguities**: Formula notation, implicit assumptions, missing parameters
**Artifacts**:
- Function manifest (analysis steps)
- Dependency graph (module imports)
- Data contracts (DataFrame schemas)
**Initialization**: Generate module stubs with type hints
**Difficulty Scoring**: Algorithmic complexity + numerical stability

### SQL Data Warehouse

**Source Documents**: Business requirements, ER diagrams, SLAs
**Ambiguities**: Join logic, aggregation rules, slowly changing dimensions
**Artifacts**:
- Table manifest (fact/dimension tables)
- Dependency graph (table lineage)
- Data contracts (column definitions, constraints)
**Initialization**: Generate DDL scripts
**Difficulty Scoring**: Query complexity + data volume

### REST API Development

**Source Documents**: API specifications, business rules, integration guides
**Ambiguities**: Error handling, rate limits, authentication flows
**Artifacts**:
- Endpoint manifest (routes, methods, parameters)
- Dependency graph (service call chains)
- Data contracts (request/response schemas)
**Initialization**: Generate OpenAPI spec + stub handlers
**Difficulty Scoring**: API surface + error handling complexity

### Legal/Contract Automation

**Source Documents**: Laws, regulations, contracts, policies
**Ambiguities**: Clause interpretation, undefined terms, jurisdictional differences
**Artifacts**:
- Rule manifest (decision logic)
- Dependency graph (rule evaluation order)
- Data contracts (input data requirements)
**Initialization**: Generate rule engine structure
**Difficulty Scoring**: Legal complexity + edge cases

## ROI Analysis

### Time Investment vs. Savings

**Typical Phase 0 Investment** (for 50-ambiguity project):
- Step 1 (Analyze): 1-2 hours (LLM-assisted)
- Step 2 (Resolve): 2-4 hours (15 min per ambiguity batch)
- Step 3 (Generate): 1 hour (mostly automated)
- Step 4 (Initialize): 30 min
- **Total**: 4.5-7.5 hours

**Savings from Avoided Refactoring**:
- Without Phase 0: Discover ambiguity during implementation
  - Discovery: 30 min per ambiguity × 50 = 25 hours
  - Refactoring: 45 min per ambiguity × 50 = 37.5 hours
  - **Total cost**: 62.5 hours

- With Phase 0:
  - Implementation proceeds smoothly
  - **Total cost**: 7.5 hours (Phase 0) + implementation time

**Net Savings**: 55 hours (88% reduction in ambiguity-related time)

### Break-Even Point

Phase 0 breaks even at approximately **10 ambiguities**:
- Phase 0 cost: ~5 hours
- Per-ambiguity refactoring cost: 30 + 45 min = 1.25 hours
- Break-even: 5 hours / 1.25 hours = 4 ambiguities
- **Safety margin**: Use Phase 0 when ≥10 ambiguities expected

## Best Practices

### During Phase 0

1. **Be thorough in Step 1 (Analyze)**
   - Don't rush ambiguity identification
   - Better to flag too many than miss critical ones
   - LLMs are good at finding ambiguities humans miss

2. **Involve domain experts in Step 2 (Resolve)**
   - User making decisions should have authority
   - Document rationale thoroughly (future you will thank you)
   - Don't make assumptions for user - always ask

3. **Validate artifacts in Step 3 (Generate)**
   - Cross-check glossary for consistency
   - Verify dependency graph has no cycles
   - Ensure all components have difficulty scores

4. **Test initialization in Step 4**
   - Verify generated structure is correct
   - Check that templates compile/parse
   - Confirm git tracking is configured

### After Phase 0

1. **Treat artifacts as source of truth**
   - Implementation questions? Check glossary first
   - Unsure about schema? Check data contracts
   - Forgot rationale? Check assumptions

2. **Update artifacts when requirements change**
   - New ambiguity discovered? Add to assumptions.md
   - New variable? Add to glossary.md
   - Schema changes? Update data-contracts.md

3. **Reference artifacts in task notes**
   - Link to relevant glossary entries
   - Cite assumption IDs
   - Reference data contract sections

4. **Use artifacts for onboarding**
   - New team member? Start with glossary + assumptions
   - Handoff project? Artifacts contain all decisions
   - Audit? Assumptions document provides trail

## Troubleshooting

### "Too many ambiguities found (200+)"

**Cause**: Source documents are extremely ambiguous or pattern is too aggressive

**Solutions**:
- Prioritize: Only resolve high/medium priority in Phase 0
- Batch by module: Complete Phase 0 for one module at a time
- Escalate: Some ambiguities may require external clarification

### "Ambiguities keep spawning new ambiguities"

**Cause**: Circular dependencies or poorly structured source documents

**Solutions**:
- Break the cycle: Make pragmatic decision on one to unblock others
- Document explicitly: Note in assumptions.md why cycle was broken
- Escalate: May indicate source documents need revision

### "Phase 0 taking longer than expected"

**Cause**: Underestimated ambiguity count or complexity

**Solutions**:
- Time-box resolution: Limit time per ambiguity
- Defer low-priority: Mark "to be resolved during implementation"
- Parallelize: Split ambiguity batches across team members

### "Artifacts are inconsistent"

**Cause**: Decisions made in isolation without cross-checking

**Solutions**:
- Validation pass: Review all artifacts together
- Glossary cross-check: Ensure all variables used are defined
- Dependency audit: Verify graph matches manifest

## Conclusion

Phase 0 is a high-leverage workflow pattern for projects with significant ambiguity. By front-loading analysis and resolution, it prevents costly mid-implementation refactoring and creates a shared understanding across teams.

**Key Takeaways**:
- Use Phase 0 for regulatory, scientific, legal, or complex technical projects
- Four steps: Analyze → Resolve → Generate → Initialize
- Creates 5-6 artifacts that serve as project source of truth
- Integrates with task management via generated tasks
- ROI: 70-85% time savings for high-ambiguity domains
- Adaptable to any domain with structured command templates

**Next Steps**:
1. Evaluate your project against Phase 0 indicators
2. Adapt command templates for your domain
3. Run Phase 0 on a pilot module
4. Measure time savings and adjust process
5. Scale to full project once validated
