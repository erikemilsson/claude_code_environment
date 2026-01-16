# Command: Validate Query (Phase 1)

## Purpose
Perform static schema validation of a Power Query .m file against its data contract.

## Usage
```
@.claude/commands/validate-query.md [QueryName]
```

## Prerequisites
- Query file exists: `power-query/[QueryName].m`
- Data contract exists: `.claude/reference/data-contracts.md`

## Process

### 1. Load Query File
Read `power-query/[QueryName].m`

### 2. Load Data Contract
Read `.claude/reference/data-contracts.md` and find section for [QueryName].

If query not found in data contract:
```
⚠️ Query "[QueryName]" not found in data-contracts.md

This might be normal if:
- Query is an intermediate/helper query
- Query was added after contract generation
- Query name mismatch

Proceeding with generic validation...
```

### 3. Parse Query Output Schema
Analyze .m code to determine output schema:

**Extract:**
- Final output column names
- Data types (from type conversions or annotations)
- Nullable status (explicit null handling)

**Analysis Method:**
- Look for final `in` statement
- Trace through transformations
- Identify column additions/removals
- Note type conversions

### 4. Compare Against Contract

**Expected Schema (from data contract):**
```
Column Name        | Type    | Nullable | Validation Rules
-------------------|---------|----------|------------------
RecycledContent    | decimal | No       | 0 ≤ value ≤ 1
TotalEmissions     | decimal | No       | value > 0
ComplianceFlag     | text    | No       | "Pass" or "Fail"
```

**Actual Schema (from .m file):**
```
Column Name        | Type    | Nullable | Found
-------------------|---------|----------|-------
RecycledContent    | decimal | No       | ✅
TotalEmissions     | decimal | No       | ✅
ComplianceFlag     | text    | No       | ✅
```

### 5. Validation Checks

#### A. Column Name Check
- All expected columns present?
- Any unexpected columns?
- Naming convention correct (snake_case)?

#### B. Data Type Check
- Types match contract?
- Appropriate type conversions?

#### C. Nullable Check
- Null handling matches contract?
- Explicit null checks present?

#### D. Validation Rules
- Are validation rules implemented?
- Error handling for invalid data?

### 6. Generate Validation Report

**Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Schema Validation: [QueryName]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: power-query/[QueryName].m
Contract: .claude/reference/data-contracts.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Column Validation

✅ RecycledContent: decimal, non-null
   - Type: ✅ Correct
   - Nullable: ✅ Correct
   - Rules: ✅ Range validation (0-1) implemented

✅ TotalEmissions: decimal, non-null
   - Type: ✅ Correct
   - Nullable: ✅ Correct
   - Rules: ✅ Positive validation implemented

⚠️ ComplianceFlag: text, non-null
   - Type: ✅ Correct
   - Nullable: ✅ Correct
   - Rules: ⚠️ Missing validation for "Pass"/"Fail" values

❌ MaterialID: text, non-null
   - Type: ❌ Expected text, found number
   - Nullable: ✅ Correct
   - Rules: N/A

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Issues Found: 2

1. ⚠️ WARNING: ComplianceFlag missing value validation
   - Expected: Check for "Pass" or "Fail" only
   - Fix: Add validation step before output

2. ❌ ERROR: MaterialID type mismatch
   - Expected: type text
   - Found: type number
   - Fix: Add type conversion: Text.From([MaterialID])

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Summary

Total Columns Checked: 4
✅ Passed: 2
⚠️ Warnings: 1
❌ Errors: 1

Result: VALIDATION FAILED

Please address issues before completing task.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 7. Additional Checks

#### Missing Columns
```
❌ Missing Expected Columns:
- TotalCO2: decimal, non-null

These columns are in the contract but not in query output.
```

#### Extra Columns
```
ℹ️ Unexpected Columns Found:
- DebugInfo: text, nullable

These columns are in query output but not in contract.
This might be intentional (intermediate data) or an error.
```

#### Naming Convention Issues
```
⚠️ Naming Convention Issues:
- "TotalCO2" → Should be "total_co2" (use snake_case)
- "CompanyID" → Should be "company_id" (use snake_case)

See .claude/context/glossary.md for naming rules.
```

## Validation Levels

### Strict Validation (Default)
- All columns must match contract exactly
- No extra columns allowed
- All validation rules must be implemented

### Lenient Validation
- Allow extra columns (helpers, debug)
- Warnings for missing validation rules
- Errors only for missing required columns

## Usage Examples

### Validate Single Query
```
@.claude/commands/validate-query.md Gold_Calculate_CFF
```

### Validate All Queries in Directory
```
@.claude/commands/validate-query.md --all
```

## Error Handling

### Query File Not Found
```
❌ Query file not found: power-query/[QueryName].m

Available queries:
- Bronze_Source_EmissionFactors.m
- Silver_Clean_EmissionFactors.m
...

Check query name spelling or run extraction first.
```

### Cannot Parse Output Schema
```
⚠️ Unable to determine output schema from query

The query structure is too complex for static analysis.

Recommendations:
1. Add explicit output schema comment in .m file
2. Test query manually in Excel/Power BI
3. Add schema documentation to query file
```

### No Data Contract Found
```
⚠️ No data contract found for "[QueryName]"

Proceeding with basic validation only:
- Column names follow naming convention?
- Data types explicitly defined?
- Null handling present?
```

## Integration with Task Workflow

This command is automatically called during `complete-task.md`.

Can also be run independently for:
- Quick verification during development
- Pre-commit checks
- Debugging schema issues

## Output

No files created - this is a read-only validation command.

Output goes to terminal/Claude's response only.

## Notes

- **Static analysis only** - no query execution
- **Schema-focused** - doesn't check logic correctness
- **Fast** - can run frequently during development
- **No data needed** - works with empty/dummy data
- Use Power BI/Excel for full testing with real data
- Validation rules are recommendations, not enforced at runtime
