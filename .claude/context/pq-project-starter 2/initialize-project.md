# Command: Initialize Project (Phase 0 - Step 1)

## Purpose
Analyze calculation method documents and extract all variables, formulas, and logic to identify ambiguities.

## Prerequisites
- Project description completed in `.claude/context/overview.md`
- Calculation documents placed in `calculation-docs/`
- Excel files placed in `excel-files/`

## Process

### 1. Read Project Context
Load `.claude/context/overview.md` to understand project goals and requirements.

### 2. Analyze Calculation Documents
For each document in `calculation-docs/`:

**Extract:**
- All variables, terms, and definitions
- All mathematical formulas and equations
- All conditional logic (if/then/else statements)
- All references to standards, regulations, articles
- All tables, figures with calculation relevance
- All units of measurement mentioned

**Record:**
- Document name and section for each item
- Exact quotes for key definitions
- Formula notation as written

### 3. Identify Ambiguities
Flag items that are:

**Undefined Terms:**
- Variables used but not defined
- Acronyms without expansion
- References like "it", "this", "these" without clear antecedent

**Ambiguous Logic:**
- "and/or" constructions
- "may" vs "must" (optional vs required)
- Conflicting statements between documents
- Implicit calculation steps (jumps in logic)

**Unit Issues:**
- Multiple units for same concept (kg vs tonnes)
- Unit conversions not explicitly stated
- Percentages vs decimals ambiguity

**Circular References:**
- Formula A depends on Formula B which depends on Formula A
- Unclear execution order

**Conditional Edge Cases:**
- What happens when condition is partially true?
- Missing else clauses
- Overlapping conditions

**Data Quality Assumptions:**
- How to handle missing values?
- How to handle out-of-range values?
- Precision requirements

### 4. Generate Ambiguity Report
Create `.claude/reference/ambiguity-report.md`:

```markdown
# Ambiguity Report

**Project:** [Name]
**Generated:** [Date]
**Total Ambiguities Found:** [Count]
**Batches Required:** [Ceil(Count/5)]

---

## Ambiguity 1: [Category]

**Source:** [Document name, Section/Article]

**Quote/Context:**
> [Exact text from document]

**Issue:**
[Description of ambiguity]

**Possible Interpretations:**
A) [Interpretation option 1]
B) [Interpretation option 2]
C) [Interpretation option 3, if applicable]

**Impact:**
- Affects: [Which queries/calculations]
- Risk: [Low/Medium/High]

**Status:** ⏳ Pending Resolution

---

## Ambiguity 2: [Category]
...
```

### 5. Generate Phase 0 Status
Create `.claude/tasks/_phase-0-status.md`:

```markdown
# Phase 0 Initialization Status

**Current Step:** 1 of 4 - Initialize Project ✅
**Next Step:** 2 of 4 - Resolve Ambiguities

## Progress
- [x] Initialize Project
- [ ] Resolve Ambiguities (0 of [N] batches)
- [ ] Generate Artifacts
- [ ] Extract Queries

## Statistics
- Documents analyzed: [Count]
- Ambiguities found: [Count]
- Batches to resolve: [Ceil(Count/5)]
- Estimated resolution time: [Count*2] minutes

## Files Generated
- `.claude/reference/ambiguity-report.md`
- `.claude/tasks/_phase-0-status.md`
```

### 6. Report to User
Present summary:

```
Phase 0 - Step 1 Complete ✅

Documents Analyzed:
- [List documents]

Ambiguities Found: [Count]
- Undefined terms: [Count]
- Ambiguous logic: [Count]
- Unit issues: [Count]
- Circular references: [Count]
- Conditional edge cases: [Count]
- Data quality assumptions: [Count]

Next Step: Run @.claude/commands/resolve-ambiguities.md
This will present the first batch of up to 5 ambiguities for resolution.

Estimated time to resolve all ambiguities: [Count*2] minutes
```

## Output Files
- `.claude/reference/ambiguity-report.md` - Complete list of ambiguities
- `.claude/tasks/_phase-0-status.md` - Phase 0 progress tracker

## Error Handling
If no calculation documents found:
- Check `calculation-docs/` folder exists and contains files
- Inform user to add documents before running this command

If no ambiguities found:
- Still create ambiguity-report.md with "No ambiguities detected"
- Proceed to generate-artifacts.md (skip resolve-ambiguities.md)

## Notes
- This is a READ-ONLY analysis step
- No code is generated yet
- No decisions are made yet
- All interpretation happens in Step 2 (resolve-ambiguities)
