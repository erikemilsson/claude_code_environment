# Project Overview

⚠️ **EDIT THIS FILE BEFORE RUNNING PHASE 0 INITIALIZATION**

---

## Project Name

[Enter project name here]

---

## Project Description

[2-4 sentence description of what you're building]

Example:
"Implement EU Battery Regulation Carbon Footprint Formula (CFF) calculation pipeline following delegated act Article 7 requirements. Must process material composition data and emission factors to generate compliance reporting with full audit trail. Bronze-silver-gold architecture for data quality assurance."

---

## Goals and Success Criteria

**Primary Goal:**
[What is the main objective?]

**Success Criteria:**
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

**Example:**
- All queries implement CFF formula per delegated act
- Output passes schema validation
- Compliance reporting generates without errors
- Full traceability to source documents

---

## Source Documents

List calculation method documents in `calculation-docs/`:

- **Document 1:** [filename.pdf] - [Brief description]
- **Document 2:** [filename.pdf] - [Brief description]

**Example:**
- **CFF-delegated-act.pdf** - EU Battery Regulation Article 7 implementation
- **ISO-22628.pdf** - Recyclability calculation methodology
- **GREET-database.pdf** - Emission factors reference

---

## Data Sources

### Excel Files

List Excel files in `excel-files/`:

- **File 1:** [filename.xlsx] - [Purpose, tables contained]
- **File 2:** [filename.xlsx] - [Purpose, tables contained]

**Example:**
- **battery-cff-input.xlsx** - Material composition, production volumes
- **emission-factors.xlsx** - Emission factors by material type and process

### Data Considerations

**Data Status:**
- [ ] Real data (sensitive - obfuscated for Claude)
- [ ] Dummy/synthetic data (safe to share)
- [ ] Mixed (some columns obfuscated)

**Obfuscation Applied:**
[If applicable, note which fields are obfuscated]

---

## Architecture

**Data Pipeline Pattern:**
- [ ] Bronze-Silver-Gold
- [ ] Star schema
- [ ] Other: [describe]

**Query Organization:**
Describe how queries will be organized:

**Example:**
```
Bronze Layer: Raw data ingestion from Excel tables
Silver Layer: Data cleaning, validation, type conversions
Gold Layer: Business logic, calculations, compliance reporting
```

---

## Special Requirements

**Regulatory Compliance:**
[Any specific regulatory requirements?]

**Performance:**
[Any performance targets or constraints?]

**Data Privacy:**
[Any special privacy considerations?]

**Validation:**
[Required validation or testing approach?]

**Example:**
- Regulatory: All formulas must be traceable to source document article/section
- Data Privacy: Company names obfuscated, actual emission values scrambled ±10%
- Validation: Schema validation only (no real data execution in Claude)

---

## Timeline and Constraints

**Target Completion:** [Date or timeframe]

**Constraints:**
- [Any blockers or dependencies?]
- [Any resource limitations?]
- [Any external deadlines?]

---

## Success Metrics

How will you know this project is complete and successful?

1. [Metric 1]
2. [Metric 2]
3. [Metric 3]

**Example:**
1. All planned queries implemented and validated
2. Sample data produces expected compliance report
3. Zero schema validation errors
4. All ambiguities documented in assumptions.md

---

## Additional Context

[Any other information Claude should know?]

**Example:**
- This is iteration 2 - previous version had performance issues
- Will be used by 5 team members, code clarity is important
- May be audited by regulators, need strong documentation
- Plan to extend to other battery types later

---

## Notes for Phase 0

[Any specific guidance for the initialization process?]

**Example:**
- Pay special attention to unit conversions in CFF formula
- Material classification logic has known ambiguities
- Previous project had issues with null handling - be extra careful

---

**Last Updated:** [Date]
**Updated By:** [Your name]
