# Power Query Task Difficulty Guide

## Purpose
Provides scoring criteria for Power Query tasks to determine complexity and whether breakdown is needed.

**Rule:** Tasks with difficulty ≥7 should be broken down into subtasks ≤6 difficulty.

---

## Difficulty Scale (1-10)

### Scoring Dimensions

Evaluate each task across these dimensions, then average:

1. **Query Dependency Depth** (1-10)
   - How many upstream queries does this depend on?
   - 1-2: No dependencies or single dependency
   - 3-4: 2-3 dependencies
   - 5-6: 4-5 dependencies  
   - 7-8: 6+ dependencies or complex dependency tree
   - 9-10: Circular dependencies or unclear execution order

2. **Formula Complexity** (1-10)
   - How complex is the transformation logic?
   - 1-2: Simple filter, rename, type conversion
   - 3-4: Basic calculations, single join
   - 5-6: Multiple calculations, conditional logic (2-3 branches)
   - 7-8: Nested conditionals (4+ branches), complex formulas
   - 9-10: Recursive functions, iterative calculations

3. **Error Surface** (1-10)
   - How many things can go wrong?
   - 1-2: Simple operation, clear inputs
   - 3-4: A few edge cases to handle
   - 5-6: Multiple null checks, validation rules
   - 7-8: Complex validation, many edge cases
   - 9-10: Ambiguous requirements, unclear error handling

4. **Regulatory Precision** (1-10)
   - How critical is correctness for compliance?
   - 1-2: Internal/exploratory work
   - 3-4: Important but not compliance-critical
   - 5-6: Feeds compliance reporting
   - 7-8: Direct compliance calculation
   - 9-10: Regulatory audit target, legal consequences if wrong

5. **Performance Impact** (1-10)
   - What's the computational load?
   - 1-2: Small dataset (<1K rows)
   - 3-4: Medium dataset (1K-10K rows)
   - 5-6: Large dataset (10K-100K rows)
   - 7-8: Very large dataset (100K-1M rows)
   - 9-10: Massive dataset (>1M rows) or complex joins

**Final Score = Average of 5 dimensions, rounded to nearest integer**

---

## Difficulty Levels

### 1-2: Trivial (No Breakdown)

**Characteristics:**
- Single-step transformation
- No dependencies
- No edge cases
- No regulatory requirements
- Small dataset

**Examples:**
- Rename column from "old_name" to "new_name"
- Filter rows where Status = "Active"
- Change data type from text to number
- Add simple comment/documentation

**Typical Implementation Time:** <15 minutes

---

### 3-4: Simple (No Breakdown)

**Characteristics:**
- 2-3 transformation steps
- Single dependency
- Basic error handling
- Low regulatory impact
- Clear requirements

**Examples:**
- Add calculated column: Mass in tonnes = Mass in kg / 1000
- Merge two queries with clear join keys
- Replace values from lookup table
- Basic data type conversions with validation

**Typical Implementation Time:** 15-30 minutes

---

### 5-6: Moderate (No Breakdown)

**Characteristics:**
- 4-6 transformation steps
- 2-3 dependencies
- Some conditional logic (2-3 branches)
- Medium regulatory importance
- Some edge cases to handle

**Examples:**
- Calculate emission factors with material type routing
- Unpivot/pivot operations with validation
- Multi-step data cleaning pipeline
- Conditional calculations based on multiple criteria

**Typical Implementation Time:** 30-60 minutes

---

### 7-8: Complex (BREAKDOWN REQUIRED)

**Characteristics:**
- 7+ transformation steps
- 4+ dependencies or complex tree
- Complex conditional logic (4+ branches)
- High regulatory importance
- Many edge cases
- Performance considerations

**Examples:**
- Implement multi-step regulatory formula (CFF calculation)
- Create custom M functions with parameters
- Complex query orchestration
- Performance-critical transformations
- Data quality validation with multiple rules

**Recommended Breakdown:** 4-6 subtasks of difficulty 3-5

**Typical Implementation Time:** 1-3 hours (if attempted without breakdown)

---

### 9-10: Critical (BREAKDOWN REQUIRED)

**Characteristics:**
- Highly complex logic
- Extensive dependencies
- Regulatory audit target
- Unclear or ambiguous requirements
- Significant performance concerns
- Multiple failure modes

**Examples:**
- Recursive functions or iterative calculations
- Cross-query validation logic
- End-to-end compliance reporting pipeline
- Complex data reconciliation
- Integration of multiple data sources with conflict resolution

**Recommended Breakdown:** 5-8 subtasks of difficulty 3-6

**Typical Implementation Time:** 3-8 hours (if attempted without breakdown)

---

## Adjustment Factors

### Add +1 to +2 Difficulty If:

- **Source document has ambiguities** requiring interpretation
- **No existing similar query** to reference (first of its kind)
- **Involves sensitive/obfuscated data** complicating testing
- **Output feeds critical reporting** with zero error tolerance
- **Tight deadline** pressure
- **Multiple stakeholders** with conflicting requirements
- **Legacy system integration** with poor documentation

### Subtract -1 Difficulty If:

- **Have clear, validated specification** with examples
- **Similar pattern exists** in codebase to reference
- **Low impact if wrong** (development/testing only)
- **Well-documented source** with clear formulas
- **Simple, clean data** with few edge cases

---

## Breakdown Strategies by Difficulty

### Difficulty 7 → 4-6 Subtasks

**Standard Pattern:**
1. **Input Validation** (difficulty 3)
   - Validate data contract compliance
   - Check for nulls, types, ranges
   - Error on invalid data

2. **Core Calculation** (difficulty 5)
   - Implement main formula logic
   - Break into explicit steps
   - Document each transformation

3. **Error Handling** (difficulty 4)
   - Add edge case handling
   - Implement fallback logic
   - Ensure no silent failures

4. **Output Validation** (difficulty 3)
   - Verify output schema
   - Check calculation reasonableness
   - Add validation flags

**Optional 5th subtask:**
5. **Performance Optimization** (difficulty 4)
   - Query folding verification
   - Indexing improvements
   - Buffering if justified

---

### Difficulty 8 → 5-7 Subtasks

Add to standard pattern:
- **Ambiguity Documentation** (difficulty 3)
  - Document all interpretation decisions
  - Reference assumptions.md entries
  - Create examples

- **Unit Testing** (difficulty 4)
  - Create sample test data
  - Define expected outputs
  - Document test cases

---

### Difficulty 9-10 → 6-8 Subtasks

Add to difficulty 8 pattern:
- **Dependency Mapping** (difficulty 3)
  - Document query dependencies
  - Create execution order diagram
  - Identify circular refs

- **Regulatory Review** (difficulty 4)
  - Cross-reference source documents
  - Verify compliance requirements
  - Document audit trail

- **Integration Testing** (difficulty 5)
  - End-to-end pipeline test
  - Cross-query validation
  - Performance under load

---

## Context Dependency Multiplier

Some tasks are harder because they require understanding multiple queries:

**Isolated Query (1.0x):**
- Standalone transformation
- Self-contained logic
- Clear inputs/outputs

**Low Context (1.1x):**
- Depends on 1-2 upstream queries
- Simple relationships
- Clear interfaces

**Medium Context (1.3x):**
- Depends on 3-4 upstream queries
- Some shared logic
- Need to understand pipeline

**High Context (1.5x):**
- Depends on 5+ upstream queries
- Complex relationships
- Must understand entire architecture

**Formula:**
`Adjusted Difficulty = Base Difficulty × Context Multiplier`
Round to nearest integer.

---

## Regulatory Precision Scoring

For compliance-related tasks, increase difficulty based on consequences:

| Consequence Level | Difficulty Modifier |
|-------------------|---------------------|
| Internal use only | +0 |
| Customer reporting | +1 |
| Regulatory submission | +2 |
| Audit target | +3 |
| Legal liability | +4 |

---

## Examples with Scoring

### Example 1: "Add column for material mass in tonnes"

**Dimension Scores:**
- Dependencies: 1 (no dependencies)
- Formula: 2 (simple division)
- Error Surface: 2 (just null check)
- Regulatory: 3 (feeds compliance calc)
- Performance: 2 (small dataset)

**Average:** (1+2+2+3+2)/5 = 2.0

**Final Difficulty:** 2 ✅ Can complete directly

---

### Example 2: "Implement CFF calculation per Article 7"

**Dimension Scores:**
- Dependencies: 7 (needs 4 upstream queries)
- Formula: 8 (multi-step, conditional logic)
- Error Surface: 8 (many edge cases)
- Regulatory: 10 (audit target, legal requirement)
- Performance: 5 (medium dataset)

**Average:** (7+8+8+10+5)/5 = 7.6

**Context Multiplier:** 1.3x (depends on 4 queries)
**Adjusted:** 7.6 × 1.3 = 9.9

**Final Difficulty:** 10 🔴 MUST breakdown

**Recommended Breakdown:**
1. Extract and validate inputs (diff 4)
2. Implement material classification logic (diff 5)
3. Calculate pre-consumer scrap component (diff 4)
4. Calculate post-consumer scrap component (diff 4)
5. Combine components per formula (diff 5)
6. Add compliance flag logic (diff 4)
7. Output validation (diff 3)

---

### Example 3: "Merge emission factors with material data"

**Dimension Scores:**
- Dependencies: 4 (2 source queries)
- Formula: 4 (basic merge with lookups)
- Error Surface: 5 (unmatched records to handle)
- Regulatory: 6 (important for compliance)
- Performance: 6 (10K rows)

**Average:** (4+4+5+6+6)/5 = 5.0

**Final Difficulty:** 5 ✅ Can complete directly (but close to threshold)

---

## Quick Reference Decision Tree

```
Is difficulty ≥ 7?
├─ Yes → BREAKDOWN REQUIRED
│   └─ Use breakdown.md command
│
└─ No → Can complete directly
    ├─ Difficulty 5-6: Review carefully, consider breakdown if uncertain
    ├─ Difficulty 3-4: Standard task, proceed
    └─ Difficulty 1-2: Trivial, quick completion
```

---

## When in Doubt

**If unsure about difficulty:**
1. Score each dimension independently
2. Average the scores
3. Apply context multiplier if applicable
4. Round to nearest integer
5. If score is 6-7 (borderline), err on side of breakdown

**General Principle:**
Better to break down unnecessarily than to struggle with an overly complex task.

Breakdown adds ~10 minutes of planning but can save hours of debugging.

---

## Notes

- Difficulty is estimated BEFORE starting work
- Re-evaluate if task turns out harder than expected
- Subtasks should not exceed difficulty 6
- Use this guide consistently for comparable difficulty scores
- Update estimates based on actual experience over time
