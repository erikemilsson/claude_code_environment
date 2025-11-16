# LLM Pitfalls for Regulatory Document Interpretation

## Purpose
This document lists common mistakes large language models make when interpreting complex calculation methods, particularly regulatory and compliance documents. Claude must treat this as a **MANDATORY CHECKLIST** before implementing any formula or calculation.

**Last Updated:** [Template - will be customized per project]

---

## ⚠️ CRITICAL: Use This as a Checklist

Before implementing ANY calculation from a regulatory or technical document:

1. Read this document completely
2. Check each pitfall against your implementation
3. If you identify a pitfall, STOP and flag it
4. Document your check in code comments

---

## General Pitfalls

### 1. Ambiguity in Legal Language

**Problem:** Regulatory documents use ambiguous language like "and/or", nested clauses, undefined pronouns ("it", "this", "these"), and conditional structures.

**LLM Behavior:** Chooses one interpretation without flagging the ambiguity to the user.

**Required Action:**
- Flag EVERY ambiguous phrase with a code comment: `// AMBIGUITY FLAGGED: [description]`
- Check `.claude/context/assumptions.md` for resolved ambiguities
- If ambiguity not in assumptions.md, STOP and ask user
- Never guess or assume interpretation

**Example:**
```m
// AMBIGUITY CHECKED: Art. 7(2) "production waste and/or post-consumer scrap"
// RESOLUTION: Per assumptions.md #5 - treating as cumulative (both can apply)
let
    TotalRecycled = PreConsumerScrap + PostConsumerScrap
in
    TotalRecycled
```

---

### 2. Implicit Calculation Steps

**Problem:** Regulatory documents skip "obvious" intermediate calculations, assuming expert knowledge.

**LLM Behavior:** Implements direct formula, missing normalization, unit conversions, or data preparation steps.

**Required Action:**
- ALWAYS break formulas into explicit steps
- Document EVERY transformation: raw → intermediate → final
- Add comments explaining each step
- Reference source document for each step

**Example:**
```m
// BAD - Missing intermediate steps
FinalResult = Value1 / Value2

// GOOD - Explicit steps
let
    // Step 1: Raw inputs in kg (from source table)
    RawMassKg = Source[mass_kg],
    
    // Step 2: Convert to tonnes (regulatory reporting unit)
    // Source: Delegated Act Annex 1, requires tonnes
    MassTonnes = RawMassKg / 1000,
    
    // Step 3: Normalize per vehicle (calculation requirement)
    // Source: Art. 7(3) specifies per-vehicle basis
    MassPerVehicle = MassTonnes / ProductionVolume,
    
    // Step 4: Final result
    FinalResult = MassPerVehicle
in
    FinalResult
```

---

### 3. Unit Inconsistencies

**Problem:** Documents switch between kg/tonnes, percentages/decimals without explicit conversion.

**LLM Behavior:** Mixes units, creating magnitude errors (1000x, 100x).

**Required Action:**
- ALWAYS add unit comments: `// Value in kg`
- Verify units match glossary definitions
- Create explicit conversion steps
- Use descriptive variable names with units: `MassKg`, `MassTonnes`

**Example:**
```m
// BAD - No unit documentation
EmissionFactor = 5.2,
TotalEmissions = Mass * EmissionFactor

// GOOD - Units explicit
let
    // Emission factor in kg CO2-eq per kg material
    // Source: GREET database, updated 2024
    EmissionFactorKgCO2perKg = 5.2,
    
    // Material mass in kg (from input table)
    MaterialMassKg = Source[mass_kg],
    
    // Total emissions in kg CO2-eq
    TotalEmissionsKgCO2 = MaterialMassKg * EmissionFactorKgCO2perKg,
    
    // Convert to tonnes CO2-eq for reporting
    // Regulatory requirement: Report in tonnes
    TotalEmissionsTonnesCO2 = TotalEmissionsKgCO2 / 1000
in
    TotalEmissionsTonnesCO2
```

---

### 4. Circular References in Nested Formulas

**Problem:** Formula A needs output from Formula B, which needs Formula A's intermediate result.

**LLM Behavior:** Creates invalid circular dependency or doesn't detect it.

**Required Action:**
- Check `.claude/reference/dependency-graph.md` before implementing
- If circular reference detected, STOP and flag to user
- Break circular references into iterative calculations
- Document execution order explicitly

---

### 5. Conditional Logic Interpretation

**Problem:** "If material is X, apply formula Y, otherwise use Z" - but what if material is partially X?

**LLM Behavior:** Implements binary if/else, missing edge cases.

**Required Action:**
- ALWAYS ask: "What happens at the boundaries?"
- List ALL conditions: primary, fallback, error cases
- Add explicit error for unexpected cases
- Document each condition with source reference

**Example:**
```m
// BAD - Binary logic only
if MaterialType = "Primary" then Formula1 else Formula2

// GOOD - Exhaustive conditions
let
    Result = 
        // Primary material: Use standard formula
        // Source: Art. 7(1)(a)
        if MaterialType = "Primary" then 
            PrimaryFormula
        
        // Secondary material: Use recycled formula
        // Source: Art. 7(1)(b)
        else if MaterialType = "Secondary" then 
            SecondaryFormula
        
        // Mixed material: Weighted average
        // Source: Interpretation guide §3.2
        else if MaterialType = "Mixed" then
            MixedFormula
        
        // Unknown/invalid material type
        else
            error Error.Record(
                "InvalidMaterialType", 
                "Material type '" & MaterialType & "' not recognized. " &
                "Valid types: Primary, Secondary, Mixed",
                MaterialType
            )
in
    Result
```

---

## Power Query-Specific Pitfalls

### 6. Null Propagation

**Problem:** M language propagates nulls differently than Excel formulas.

**LLM Behavior:** Assumes null = 0, or doesn't handle nulls at all.

**Required Action:**
- Check `.claude/context/assumptions.md` for null handling decisions
- Default to ERROR on null for required fields
- Use `?? 0` only when explicitly specified
- Document null handling for each field

**Example:**
```m
// BAD - Silent null handling
Value1 + Value2

// GOOD - Explicit null handling
let
    // Check: Is Value1 required? (per data-contracts.md: Yes)
    ValidatedValue1 = 
        if Value1 = null then 
            error "Value1 is required but null"
        else 
            Value1,
    
    // Check: Is Value2 optional? (per data-contracts.md: Optional, default 0)
    ValidatedValue2 = Value2 ?? 0,
    
    Result = ValidatedValue1 + ValidatedValue2
in
    Result
```

---

### 7. Error Handling Overwrites

**Problem:** `try ... otherwise` can mask data quality issues.

**LLM Behavior:** Adds try blocks everywhere for "robustness".

**Required Action:**
- NO try blocks without explicit justification in comments
- Let errors surface - they indicate data quality issues
- Use try only for expected failures (optional data sources, nullable fields)
- Log all errors, don't silently replace with defaults

**Example:**
```m
// BAD - Silent error masking
try Source[column] otherwise 0

// GOOD - Explicit error handling
let
    // Check if column exists (optional source)
    // Rationale: Different source systems may omit this column
    Value = 
        if List.Contains(Table.ColumnNames(Source), "column") then
            Source[column]
        else
            null,
    
    // Apply default only for valid null, not errors
    Result = Value ?? 0
in
    Result
```

---

### 8. Table.Buffer Misuse

**Problem:** Buffering queries breaks refresh dependencies and can hide errors.

**LLM Behavior:** Adds Table.Buffer for "performance" without understanding impact.

**Required Action:**
- NEVER use Table.Buffer unless specifically requested
- Document why buffering is needed when used
- Consider alternatives (query folding, incremental refresh)

---

## Pre-Implementation Checklist

Before implementing ANY calculation, verify:

- [ ] Have I checked `.claude/context/assumptions.md` for relevant decisions?
- [ ] Have I verified all variable names in `.claude/context/glossary.md`?
- [ ] Have I broken the formula into explicit steps with comments?
- [ ] Have I documented units for every numerical value?
- [ ] Have I checked `.claude/reference/dependency-graph.md` for circular refs?
- [ ] Have I defined all edge cases and boundary conditions?
- [ ] Have I handled nulls explicitly per data contract?
- [ ] Have I avoided silent error handling (no unexplained try blocks)?
- [ ] Have I cross-referenced the source document for each step?
- [ ] Have I added validation for data quality issues?

---

## In-Code Validation Block

Add this to EVERY query implementation:

```m
// IMPLEMENTATION CHECKLIST
// [x] Variable names from glossary.md: RecycledContentShare, TotalEmissions
// [x] Units documented: kg, %, kg CO2-eq
// [x] Assumptions referenced: #5 (null handling), #12 (material classification)
// [x] Dependencies verified: Depends on Silver_Clean_EmissionFactors
// [x] Edge cases handled: Zero emissions, missing factors, out-of-range values
// [x] Null handling: Required fields error, optional fields default per contract
// [x] Error handling: No silent failures, all errors surfaced
// [x] Formula source: Delegated Act Art. 7(2), ISO 22628:2002 §3.1
// [x] Output schema: Matches data-contracts.md
```

---

## When You Violate These Rules

If you find yourself about to violate any rule in this document:

1. **STOP** implementation
2. **FLAG** the specific pitfall
3. **EXPLAIN** why you think the rule doesn't apply
4. **WAIT** for user confirmation before proceeding

Example:
```
⚠️ PITFALL FLAGGED: Implicit Calculation Step

I'm about to implement the CFF formula but the source document
skips the normalization step between equations (3) and (4).

I believe the missing step is: Normalize by production volume

However, per pitfall #2, I should not implement implicit steps
without confirmation.

Please confirm: Should I add normalization step?
Source reference for confirmation: [cite document section]
```

---

## Project-Specific Pitfalls

[This section will be populated during Phase 0 based on specific calculation methods]

*After completing Phase 0 ambiguity resolution, add any calculation-specific pitfalls discovered here.*

---

## Remember

This document exists because these mistakes are **common and costly**. 

Taking 2 minutes to check this list before implementing can save hours of debugging and prevent compliance issues.

When in doubt: **FLAG, DON'T GUESS**.
