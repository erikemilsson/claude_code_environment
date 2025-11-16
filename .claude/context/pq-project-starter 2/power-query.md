# Power Query M Code Standards

## Purpose
Defines coding conventions for Power Query M code to ensure consistency, readability, and maintainability.

---

## Code Structure

### Query Template

Every query should follow this structure:

```m
// Query: [QueryName]
// Purpose: [Brief description from query-manifest.md]
// Dependencies: [List of upstream queries]
// Generated: [Date]
// Task: [task_id if applicable]

// SCHEMA INPUT
// Expected columns:
// - column_name: type (unit) - description

// SCHEMA OUTPUT
// Produced columns:
// - column_name: type (unit) - description

let
    // Step 1: [Description]
    Source = [implementation],
    
    // Step 2: [Description]
    StepName = [implementation],
    
    // Step N: Final output
    Output = StepName
in
    Output
```

---

## Naming Conventions

### Step Variables (in let...in block)

**Use PascalCase:**
- `Source`, `CleanData`, `ValidatedInput`, `FinalOutput`
- First letter uppercase, no underscores
- Descriptive, not abbreviated

**Good:**
```m
ValidatedEmissionFactors = ...
FilteredMaterials = ...
CalculatedCFF = ...
```

**Bad:**
```m
validated_emission_factors = ...  // Wrong case
vef = ...                         // Too abbreviated
x = ...                           // Non-descriptive
```

### Column Names (in tables)

**Use snake_case:**
- `emission_factor`, `total_emissions`, `company_id`
- Lowercase, underscores between words
- Must match glossary.md definitions

**Good:**
```m
#"Added Column" = Table.AddColumn(Source, "total_emissions_kg", ...)
```

**Bad:**
```m
#"Added Column" = Table.AddColumn(Source, "TotalEmissions", ...)  // Wrong case
```

### Custom Functions

**Use PascalCase with verb prefix:**
```m
CalculateCFF = (mass, factor) => ...
ValidateRange = (value, min, max) => ...
ConvertUnits = (value, from_unit, to_unit) => ...
```

---

## Commenting Standards

### Required Comments

1. **Every query** needs header block (see template above)
2. **Every transformation step** needs description comment
3. **Every calculation** needs unit comment if numeric
4. **Every assumption** needs reference to assumptions.md
5. **Every formula** needs source document reference

### Comment Format

**Step descriptions:**
```m
// Step 3: Convert mass from kg to tonnes
// Unit: Input in kg, output in tonnes (1000:1 ratio)
MassTonnes = MassKg / 1000,
```

**Assumption references:**
```m
// Null handling per assumptions.md #5: Required field, error if null
ValidatedValue = if Value = null then 
    error "Required field Value is null" 
else 
    Value,
```

**Formula sources:**
```m
// Carbon Footprint Formula per Delegated Act Art. 7(2)
// CFF = (PC × EFPC) + (RC × EFRC) + ...
CFF_Result = (PreConsumer * EF_PreConsumer) + (Recycled * EF_Recycled),
```

---

## Type Handling

### Explicit Type Conversions

**Always use explicit conversions:**

```m
// Good
MassKg = Number.From(Source[mass]),
CompanyName = Text.From(Source[company]),
ProcessDate = Date.From(Source[date]),

// Bad
MassKg = Source[mass],  // Implicit, may fail
```

### Type Annotations

**For calculated columns, add type:**

```m
// Good
#"Added Column" = Table.AddColumn(
    Source, 
    "total_emissions", 
    each [mass_kg] * [emission_factor],
    type number
),

// Acceptable (if type is obvious)
#"Added Column" = Table.AddColumn(
    Source, 
    "total_emissions", 
    each [mass_kg] * [emission_factor]
),
```

---

## Null Handling

### Default Strategy: Explicit Errors

**For required fields:**

```m
// Error on null
ValidatedField = if Value = null then 
    error Error.Record(
        "NullValue",
        "Required field 'Value' is null",
        Value
    )
else 
    Value,
```

**For optional fields (if specified in data contract):**

```m
// Default value
OptionalField = Value ?? 0,  // Only if contract says "default: 0"
```

### Never Use Silent Defaults

**Bad:**
```m
Result = Value ?? 0  // Why 0? What if null is an error?
```

**Good:**
```m
// Per data-contracts.md: OptionalValue defaults to 0 if null
Result = Value ?? 0,
```

---

## Error Handling

### Avoid Try/Otherwise

**Default: Let errors surface**

```m
// Good - Errors are visible
Result = Value1 / Value2,

// Bad - Masks divide-by-zero
Result = try Value1 / Value2 otherwise 0,
```

### When Try Is Acceptable

**Only for expected optional scenarios:**

```m
// Acceptable: Checking if column exists
HasColumn = List.Contains(Table.ColumnNames(Source), "optional_column"),

Value = if HasColumn then 
    Source[optional_column]
else 
    null,
```

**With justification comment:**

```m
// Try block justified: Different source systems may have different schemas
// If column missing, use null and handle downstream
Result = try Source[optional_field] otherwise null,
```

---

## Table Operations

### Prefer Query Folding

**Write operations that fold to source:**

```m
// Good - Folds to SQL
Filtered = Table.SelectRows(Source, each [Status] = "Active"),

// Avoid if possible - Doesn't fold
Filtered = Table.SelectRows(Source, each Text.Contains([Name], "test")),
```

### Never Buffer Without Reason

```m
// Bad - Unnecessary
BufferedTable = Table.Buffer(Source),

// Good - Only if justified
// Justification: This table is referenced 5+ times and source query is expensive
BufferedTable = Table.Buffer(ExpensiveQuery),
```

---

## Column Operations

### Column Addition

**Use descriptive step names:**

```m
// Good
AddEmissionsColumn = Table.AddColumn(
    Source,
    "total_emissions_kg",
    each [mass_kg] * [emission_factor],
    type number
),

// Bad - Generic name
#"Added Column" = Table.AddColumn(Source, "Column1", ...),
```

### Column Removal

**Document why removing:**

```m
// Remove temporary calculation columns
// These were only needed for intermediate steps
RemoveTemporaryColumns = Table.RemoveColumns(Source, {"temp_value1", "temp_value2"}),
```

---

## Conditional Logic

### Use Structured If-Then-Else

**Format for readability:**

```m
Result = 
    if MaterialType = "Primary" then
        PrimaryFormula
    else if MaterialType = "Secondary" then
        SecondaryFormula
    else if MaterialType = "Mixed" then
        MixedFormula
    else
        error "Invalid MaterialType: " & MaterialType,
```

**Not:**

```m
Result = if MaterialType = "Primary" then PrimaryFormula else if MaterialType = "Secondary" then SecondaryFormula else error "Invalid"
```

---

## Performance Considerations

### Column References

**Avoid repeated calculations:**

```m
// Bad - Calculates mass * factor twice
Result = if [mass_kg] * [emission_factor] > 100 then
    [mass_kg] * [emission_factor]
else
    0,

// Good - Calculate once
Emissions = [mass_kg] * [emission_factor],
Result = if Emissions > 100 then Emissions else 0,
```

### Table Scans

**Minimize table scans:**

```m
// Bad - Multiple scans
Count1 = Table.RowCount(Table.SelectRows(Source, each [Type] = "A")),
Count2 = Table.RowCount(Table.SelectRows(Source, each [Type] = "B")),

// Good - Single scan with grouping
Counts = Table.Group(Source, {"Type"}, {{"Count", Table.RowCount, type number}}),
```

---

## Documentation Headers

### Validation Checklist

**Add to every completed query:**

```m
// IMPLEMENTATION CHECKLIST
// [x] Variable names from glossary.md: [List key variables]
// [x] Units documented: [List units used]
// [x] Assumptions referenced: [List assumption IDs]
// [x] Dependencies verified: [List dependent queries]
// [x] Edge cases handled: [List edge cases]
// [x] Null handling: [Describe strategy]
// [x] Error handling: [Describe approach]
// [x] Formula source: [Document references]
// [x] Output schema: Matches data-contracts.md
```

---

## Code Review Checklist

Before completing a query task:

- [ ] Header block complete with all metadata
- [ ] All steps have description comments
- [ ] Variable names follow conventions (PascalCase/snake_case)
- [ ] Column names match glossary.md
- [ ] Units documented for all numeric values
- [ ] Null handling is explicit
- [ ] No unexplained try/otherwise blocks
- [ ] No Table.Buffer without justification
- [ ] Validation checklist at end
- [ ] Output schema matches data contract

---

## Examples

See `power-query/` directory for implemented queries following these standards.

---

**Last Updated:** [Template]
**See Also:**
- `.claude/context/naming.md` - Detailed naming rules
- `.claude/context/error-handling.md` - Error handling patterns
- `.claude/context/glossary.md` - Variable definitions
