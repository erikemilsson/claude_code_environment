# Power Query Multi-Dimensional Difficulty Scoring

## Overview

Power Query projects use a **5-dimension difficulty scoring system** instead of standard single-dimension LLM error probability scoring. This document explains why, when to use it, and how to calculate composite scores.

---

## Standard vs. Multi-Dimensional Difficulty Scoring

### Standard Difficulty Scoring (1-10)

Used in most software development projects:

- **Single dimension**: LLM error probability
- **Subjective judgment** based on overall complexity
- **Examples**:
  - 1: Single word/character change
  - 3: Basic CRUD following pattern
  - 5: API integration with docs
  - 7: Multi-provider auth setup
  - 8: Database migration with backfill
  - 10: Distributed system implementation

**Strengths:**
- Simple and quick to assign
- Works well for general software tasks
- Easy to explain to stakeholders

**Weaknesses:**
- Subjective (different evaluators may disagree)
- Doesn't capture multiple complexity factors
- Difficult to justify scores consistently
- Misses domain-specific requirements

### Power Query Multi-Dimensional Scoring

Used for regulatory/compliance and complex ETL projects:

- **Five separate dimensions** evaluated independently
- **Each dimension scored 1-10**
- **Final score = average of all dimensions**, rounded to nearest integer
- **More objective** and consistent across evaluators
- **Accounts for domain-specific complexities**

**Strengths:**
- Objective and reproducible
- Identifies which aspects make a task complex
- Documents rationale for difficulty assessment
- Helps target breakdown strategy
- Consistent across team members

**Weaknesses:**
- Takes longer to score (evaluate 5 dimensions)
- Requires understanding of all dimensions
- May be overkill for simple projects

---

## When to Use Multi-Dimensional Scoring

### Use Multi-Dimensional Scoring For:

✅ **Regulatory/compliance calculations**
- Different precision requirements per task
- Legal consequences for errors
- Audit trails needed

✅ **Complex data transformation pipelines**
- Dependency chains between queries
- Bronze-Silver-Gold medallion architectures
- Multiple data quality requirements

✅ **Projects with specialized domain requirements**
- Industry-specific formulas (emissions, financial calculations)
- Ambiguous source documentation
- Performance-critical transformations

✅ **Team environments**
- Need objective, reproducible scoring
- Multiple people estimating difficulty
- Consistency across evaluators important

### Use Standard 1-10 Scoring For:

❌ **Simple software development tasks**
- Basic CRUD operations
- UI updates
- Standard API integrations

❌ **Projects without specialized requirements**
- Internal tools
- Prototypes
- Learning projects

❌ **Solo work**
- Where consistency less critical
- Speed of estimation matters

---

## The 5 Dimensions Explained

Power Query projects have unique complexity factors not captured by simple LLM error probability.

### 1. Query Dependency Depth (1-10)

**What it measures**: How many upstream queries this task depends on

Unlike typical code, Power Query transformations form **dependency DAGs** (directed acyclic graphs). Implementation order matters, and understanding upstream transformations is required.

| Score | Dependencies | Impact |
|-------|-------------|---------|
| 1-2 | No dependencies or single dependency | Can implement in isolation |
| 3-4 | 2-3 dependencies | Need to understand a few queries |
| 5-6 | 4-5 dependencies | Must understand pipeline segment |
| 7-8 | 6+ dependencies or complex tree | Must understand architecture |
| 9-10 | Circular dependencies or unclear order | Requires dependency mapping |

**Why it matters**: High dependency depth requires loading multiple queries into context, increasing cognitive load and error probability.

### 2. Formula Complexity (1-10)

**What it measures**: Complexity of the M transformation logic

M language transformations range from trivial filters to recursive functions.

| Score | Formula Type | Example |
|-------|-------------|---------|
| 1-2 | Simple filter, rename, type conversion | `Table.SelectRows(Source, each [Status] = "Active")` |
| 3-4 | Basic calculations, single join | `Table.AddColumn(Source, "Total", each [Quantity] * [Price])` |
| 5-6 | Multiple calculations, conditional logic | `if [Type] = "A" then [Value] * 1.2 else [Value] * 0.8` |
| 7-8 | Nested conditionals, complex formulas | Multi-branch case statements, complex date logic |
| 9-10 | Recursive functions, iterative calculations | `List.Accumulate()`, custom recursive M functions |

**Why it matters**: Complex formulas have higher error probability and require more careful testing.

### 3. Error Surface (1-10)

**What it measures**: How many things can go wrong

Data quality issues and edge cases multiply in ETL contexts.

| Score | Error Surface | Considerations |
|-------|--------------|----------------|
| 1-2 | Simple operation, clear inputs | Minimal null checks needed |
| 3-4 | A few edge cases to handle | Some null checks, basic validation |
| 5-6 | Multiple null checks, validation rules | Various data quality issues possible |
| 7-8 | Complex validation, many edge cases | Type mismatches, missing data, outliers |
| 9-10 | Ambiguous requirements, unclear handling | Undefined error behavior, silent failures |

**Why it matters**: High error surface requires comprehensive validation and error handling, increasing implementation time and testing burden.

### 4. Regulatory Precision (1-10)

**What it measures**: How critical is correctness for compliance

Compliance calculations have **variable correctness requirements** not captured by standard scoring.

| Score | Regulatory Impact | Consequences of Error |
|-------|------------------|---------------------|
| 1-2 | Internal/exploratory work | No external impact |
| 3-4 | Important but not compliance-critical | Internal reporting affected |
| 5-6 | Feeds compliance reporting | Indirect compliance impact |
| 7-8 | Direct compliance calculation | Regulatory submission affected |
| 9-10 | Regulatory audit target | Legal liability, fines, sanctions |

**Why it matters**: Higher regulatory precision requires:
- More careful interpretation of source documents
- Comprehensive audit trails
- Multiple validation checks
- Documentation of assumptions
- Zero error tolerance

### 5. Performance Impact (1-10)

**What it measures**: Computational load and dataset size

Query folding and dataset size critically affect query viability.

| Score | Dataset Size | Performance Concern |
|-------|-------------|-------------------|
| 1-2 | <1K rows | Trivial performance |
| 3-4 | 1K-10K rows | Acceptable for most operations |
| 5-6 | 10K-100K rows | Need to consider query folding |
| 7-8 | 100K-1M rows | Query folding required |
| 9-10 | >1M rows or complex joins | Performance-critical, may need architecture changes |

**Why it matters**: Poor performance can make queries unusable. High scores require:
- Query folding verification
- Buffering strategy
- Potentially breaking into separate queries
- Performance testing

---

## How to Calculate Composite Scores

### Step-by-Step Process

**Example Task**: "Implement Carbon Footprint Formula (CFF) calculation per Article 7 of EU Battery Regulation"

#### Step 1: Score Each Dimension Independently

Evaluate the task across all 5 dimensions:

```
Query Dependency Depth:    7   (needs 4 upstream queries: materials, masses, factors, scrap)
Formula Complexity:        8   (nested conditionals for material types, multi-step calculation)
Error Surface:             8   (nulls, type validation, range checks, material mismatches)
Regulatory Precision:     10   (EU regulatory audit target, legal requirements)
Performance Impact:        5   (medium dataset, ~5K battery records)
```

**Scoring Rationale**:
- **Dependency Depth = 7**: Requires understanding Bronze queries for materials, emissions factors, pre-consumer scrap, and post-consumer scrap tables
- **Formula Complexity = 8**: Article 7 formula has material-type branching, percentage calculations, and component combination logic
- **Error Surface = 8**: Must validate material types exist, masses are positive, percentages in valid ranges, no division by zero
- **Regulatory Precision = 10**: EU Battery Regulation compliance required for market access, subject to regulatory audits
- **Performance Impact = 5**: 5,000 battery records is manageable but needs efficient joins

#### Step 2: Calculate Average

```
Average = (7 + 8 + 8 + 10 + 5) / 5
        = 38 / 5
        = 7.6
```

#### Step 3: Apply Context Multiplier (Optional)

For tasks with high dependency depth, apply context multiplier:

| Dependencies | Multiplier | Rationale |
|-------------|-----------|-----------|
| 0-2 queries | 1.0x | Isolated query |
| 3-4 queries | 1.3x | Medium context |
| 5+ queries | 1.5x | High context |

For this task: **4 dependencies → 1.3x multiplier**

```
Adjusted Score = 7.6 × 1.3
               = 9.88
```

#### Step 4: Round to Nearest Integer

```
Final Difficulty = round(9.88) = 10
```

#### Step 5: Apply Breakdown Rule

```
Difficulty ≥ 7 → BREAKDOWN REQUIRED
```

**Result**: This task gets difficulty **10**, requiring breakdown into 6-8 subtasks, each with difficulty ≤6.

### Breakdown Strategy Based on Dimension Analysis

The dimension scores help identify breakdown approach:

**High Regulatory Precision (10) suggests:**
- Separate validation subtask
- Documentation subtask for assumptions
- Audit trail creation

**High Formula Complexity (8) suggests:**
- Break formula into logical steps
- One subtask per calculation component
- Validate intermediate results

**High Error Surface (8) suggests:**
- Input validation subtask
- Edge case handling subtask
- Output validation subtask

**Recommended Breakdown** (7 subtasks):

1. **Extract and validate inputs** (diff 4)
   - Addresses: Dependency Depth, Error Surface
   - Load upstream queries, validate schemas

2. **Implement material classification logic** (diff 5)
   - Addresses: Formula Complexity
   - Route by material type per regulation

3. **Calculate pre-consumer scrap component** (diff 4)
   - Addresses: Formula Complexity, Regulatory Precision
   - One component of Article 7 formula

4. **Calculate post-consumer scrap component** (diff 4)
   - Addresses: Formula Complexity, Regulatory Precision
   - Second component of Article 7 formula

5. **Combine components per formula** (diff 5)
   - Addresses: Formula Complexity, Regulatory Precision
   - Final CFF calculation

6. **Add compliance flag logic** (diff 4)
   - Addresses: Regulatory Precision, Error Surface
   - Validate against thresholds

7. **Output validation and audit trail** (diff 3)
   - Addresses: Regulatory Precision, Error Surface
   - Schema validation, reasonableness checks

---

## Benefits of Multi-Dimensional Scoring

### 1. Objectivity

**Problem**: Two team members disagree on difficulty
- Person A: "This is a difficulty 5, it's just a formula"
- Person B: "No, it's a 9, it's regulatory-critical"

**Solution**: Score dimensions separately
- Formula Complexity: 5 (they agree)
- Regulatory Precision: 9 (they agree)
- Average other dimensions: (6+4+3)/3 = 4.3
- **Final: (5+9+6+4+3)/5 = 5.4 → rounds to 5**

Both evaluators reach same conclusion.

### 2. Breakdown Targeting

**Single-dimension scoring**: "It's an 8, break it down" (but how?)

**Multi-dimensional scoring**:
```
Dependency Depth:      3  (low - isolated query)
Formula Complexity:    9  (HIGH - complex nested logic)
Error Surface:         7  (medium-high)
Regulatory Precision:  4  (low - internal only)
Performance:           2  (low - small dataset)

Average: 5.0 (no breakdown needed by average)
BUT: Formula Complexity = 9 warrants breakdown focused on formula logic
```

**Insight**: Break down by logical formula steps, not by validation or performance.

### 3. Documentation

Multi-dimensional scores **document why a task is complex**:

```json
{
  "id": "23",
  "title": "Implement CFF calculation",
  "difficulty": 10,
  "difficulty_breakdown": {
    "query_dependency_depth": 7,
    "formula_complexity": 8,
    "error_surface": 8,
    "regulatory_precision": 10,
    "performance_impact": 5
  },
  "context_multiplier": 1.3,
  "rationale": "High regulatory precision (audit target) and complex formula logic with multiple dependencies"
}
```

Six months later, you understand **why** it was scored this way.

### 4. Continuous Improvement

Track actual vs. estimated difficulty per dimension:

```
Task 23 Retrospective:
- Estimated Formula Complexity: 8
- Actual Formula Complexity: 9 (took longer than expected due to edge case logic)
- Lesson: Article 7 formulas consistently score higher, adjust future estimates
```

Improves future scoring accuracy.

---

## Common Pitfalls

### Pitfall 1: Averaging Without Context Multiplier

**Wrong:**
```
Dependencies: 8, Formula: 6, Error: 5, Regulatory: 7, Performance: 4
Average: (8+6+5+7+4)/5 = 6.0 → Difficulty 6 ✅ (no breakdown)
```

**Right:**
```
Dependencies: 8 → Apply 1.5x multiplier (5+ dependencies)
Average: 6.0 × 1.5 = 9.0 → Difficulty 9 🔴 (BREAKDOWN REQUIRED)
```

**Lesson**: High dependency depth compounds other complexities.

### Pitfall 2: Ignoring Domain-Specific Dimensions

**Wrong** (using only Formula Complexity):
```
"It's just a simple calculation: recycled% = scrap / total"
Difficulty: 3 ✅ (complete directly)
```

**Right** (considering all dimensions):
```
Formula: 3 (simple division)
Regulatory: 10 (EU Battery Regulation audit target)
Error Surface: 7 (nulls, division by zero, negative values)
Dependencies: 5 (needs 2 upstream queries)
Performance: 3 (small dataset)

Average: (3+10+7+5+3)/5 = 5.6 → Difficulty 6
```

**Lesson**: Regulatory precision can elevate trivial formulas to moderate difficulty.

### Pitfall 3: Scoring After Starting Work

**Problem**: You start a task thinking it's difficulty 5, discover it's actually 8 halfway through.

**Solution**: Score all dimensions **before** starting work. Re-evaluate if task turns out harder than expected.

---

## Quick Reference

### When to Use Multi-Dimensional Scoring

| Project Type | Use Multi-Dimensional? | Why |
|-------------|---------------------|-----|
| Regulatory compliance calculations | ✅ Yes | Variable precision requirements |
| Complex ETL pipelines | ✅ Yes | Dependency chains matter |
| Financial calculations | ✅ Yes | Accuracy requirements vary |
| Standard web app | ❌ No | Standard scoring sufficient |
| Prototype/learning project | ❌ No | Speed over precision |

### The 5 Dimensions at a Glance

1. **Query Dependency Depth**: How many upstream queries? (1-10)
2. **Formula Complexity**: How complex is the M code? (1-10)
3. **Error Surface**: How many edge cases? (1-10)
4. **Regulatory Precision**: How critical is correctness? (1-10)
5. **Performance Impact**: How large is the dataset? (1-10)

### Calculation Formula

```
Base Score = (Dim1 + Dim2 + Dim3 + Dim4 + Dim5) / 5

Context Multiplier:
- 0-2 dependencies: 1.0x
- 3-4 dependencies: 1.3x
- 5+ dependencies: 1.5x

Final Difficulty = round(Base Score × Context Multiplier)

If Difficulty ≥ 7 → BREAKDOWN REQUIRED
```

---

## See Also

- **difficulty-guide-pq.md** - Detailed difficulty level descriptions and examples
- **breakdown-workflow.md** - How to break down high-difficulty tasks
- **../context/glossary.md** - Variable definitions
- **../context/assumptions.md** - Interpretation decisions
