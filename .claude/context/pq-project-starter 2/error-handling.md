# Error Handling Standards

## Purpose
Defines consistent error handling patterns for Power Query to ensure data quality issues are caught, not hidden.

## Core Principle

**❌ NEVER silently handle errors**
```m
// ❌ BAD - Hides data quality issues
try Source otherwise #table({}, {})
try [column] otherwise 0
try Table.TransformColumns(...) otherwise Source
```

**✅ ALWAYS make errors explicit**
```m
// ✅ GOOD - Errors are visible and logged
if Source = null then 
    error "Source data not found"
else 
    Source

if [column] = null then
    error "Required column 'column' contains null value"
else
    [column]
```

## When to Use `try`

Use `try ... otherwise` **ONLY** for expected, documented failure modes:

### ✅ Acceptable Use Cases

**1. Optional Data Sources**
```m
// When a data source might legitimately not exist
OptionalTable = 
    try Excel.CurrentWorkbook(){[Name="OptionalData"]}[Content]
    otherwise 
        #table(
            type table [id = Int64.Type, value = number],
            {}  // Empty table with correct schema
        )  // DOCUMENTED: OptionalData table may not exist in all environments
```

**2. Type Conversions with Validation**
```m
// When converting user input that might be invalid format
SafeNumberConversion = (value as any) =>
    let
        Converted = try Number.From(value) otherwise null,
        Result = if Converted = null then
            error Error.Record(
                "Type.Conversion.Failed",
                "Cannot convert '" & Text.From(value) & "' to number",
                [Value = value]
            )
        else
            Converted
    in
        Result
```

**3. Missing Optional Columns**
```m
// When a column is optional per specification
OptionalColumn = 
    if Table.HasColumns(Source, "optional_field") then
        Source
    else
        Table.AddColumn(Source, "optional_field", each null, type nullable number)
```

## Error Pattern Templates

### Pattern 1: Null Validation
```m
// Check for required values
ValidatedValue = 
    if Value = null then
        error Error.Record(
            "Validation.NullValue",
            "Required field contains null",
            [Field = "FieldName", Row = RowIndex]
        )
    else
        Value
```

### Pattern 2: Range Validation
```m
// Validate numeric ranges
ValidatedEmissionFactor = 
    if EmissionFactor < 0 then
        error Error.Record(
            "Validation.OutOfRange",
            "Emission factor cannot be negative",
            [Value = EmissionFactor, Expected = ">= 0"]
        )
    else if EmissionFactor > 1000 then
        error Error.Record(
            "Validation.OutOfRange",
            "Emission factor suspiciously high, verify data",
            [Value = EmissionFactor, Expected = "<= 1000"]
        )
    else
        EmissionFactor
```

### Pattern 3: Schema Validation
```m
// Verify expected columns exist
ValidateSchema = (table as table, requiredColumns as list) =>
    let
        ActualColumns = Table.ColumnNames(table),
        MissingColumns = List.Difference(requiredColumns, ActualColumns),
        Result = if List.Count(MissingColumns) > 0 then
            error Error.Record(
                "Schema.MissingColumns",
                "Required columns not found in table",
                [
                    Required = requiredColumns,
                    Actual = ActualColumns,
                    Missing = MissingColumns
                ]
            )
        else
            table
    in
        Result

// Usage:
ValidatedTable = ValidateSchema(Source, {"id", "emission_factor", "material_type"})
```

### Pattern 4: Conditional Logic with Error States
```m
// Explicit error for unexpected conditions
RoutedValue = 
    if MaterialType = "Primary" then
        PrimaryEmissionFactor
    else if MaterialType = "Secondary" then
        SecondaryEmissionFactor
    else if MaterialType = "Recycled" then
        RecycledEmissionFactor
    else
        error Error.Record(
            "Logic.UnexpectedValue",
            "Material type not recognized",
            [
                Value = MaterialType,
                Expected = {"Primary", "Secondary", "Recycled"}
            ]
        )
```

### Pattern 5: Data Quality Flags (Non-Blocking)
```m
// When you want to flag issues but continue processing
#"Add Quality Flag" = Table.AddColumn(
    Source,
    "data_quality_flag",
    each 
        if [emission_factor] = null then "MISSING_EF"
        else if [emission_factor] < 0 then "NEGATIVE_EF"
        else if [emission_factor] > 1000 then "SUSPICIOUS_EF"
        else "OK",
    type text
)

// Then filter or report on flagged rows
QualityReport = Table.SelectRows(
    #"Add Quality Flag",
    each [data_quality_flag] <> "OK"
)
```

## Error Records Structure

**Always use structured error records**:
```m
error Error.Record(
    "Category.Subcategory",       // Machine-readable error code
    "Human readable message",      // Clear description
    [                             // Diagnostic details
        Field = "field_name",
        Value = actualValue,
        Expected = expectedValue,
        Row = rowNumber
    ]
)
```

### Standard Error Categories
- `Validation.*` - Data validation failures
- `Schema.*` - Schema/structure mismatches  
- `Logic.*` - Unexpected logical conditions
- `Type.*` - Type conversion issues
- `Source.*` - Data source problems
- `Calculation.*` - Mathematical errors (division by zero, etc.)

## Table-Level Error Handling

### Pattern: Validate Entire Table
```m
ValidateTable = (source as table) =>
    let
        // Check row count
        RowCount = Table.RowCount(source),
        _ = if RowCount = 0 then
            error "Validation.EmptyTable: Source table contains no rows"
        else
            null,
        
        // Check for required columns
        RequiredColumns = {"id", "emission_factor", "material_type"},
        ActualColumns = Table.ColumnNames(source),
        MissingColumns = List.Difference(RequiredColumns, ActualColumns),
        _ = if List.Count(MissingColumns) > 0 then
            error Error.Record(
                "Schema.MissingColumns",
                "Required columns missing",
                [Missing = MissingColumns]
            )
        else
            null,
        
        // Check for null values in required fields
        NullCheckId = Table.SelectRows(source, each [id] = null),
        _ = if Table.RowCount(NullCheckId) > 0 then
            error "Validation.NullValue: 'id' column contains null values"
        else
            null,
        
        Result = source
    in
        Result
```

## Forbidden Patterns

### ❌ Never Do This

**1. Silent Null Replacement**
```m
// ❌ BAD - Hides missing data
Value = [column] ?? 0
```

**2. Catch-All Try Blocks**
```m
// ❌ BAD - Masks all errors
Result = try ComplexTransformation otherwise Source
```

**3. Generic Error Messages**
```m
// ❌ BAD - Not actionable
if Condition then Value else error "Something went wrong"
```

**4. Ignoring Validation Results**
```m
// ❌ BAD - Validates but doesn't act on result
ValidationFlag = if [value] < 0 then "INVALID" else "VALID",
// ... continues without checking ValidationFlag
```

## Best Practices

### 1. Fail Fast
Place validation steps early in the query:
```m
let
    Source = Excel.CurrentWorkbook(){[Name="InputTable"]}[Content],
    
    // Validate immediately
    ValidatedSchema = ValidateSchema(Source, {"id", "emission_factor"}),
    
    // Only then proceed with transformations
    #"Changed Type" = Table.TransformColumnTypes(ValidatedSchema, ...),
    ...
```

### 2. Provide Diagnostic Context
```m
// ✅ GOOD - Provides actionable information
error Error.Record(
    "Validation.OutOfRange",
    "Emission factor out of acceptable range",
    [
        RowNumber = 42,
        Field = "emission_factor",
        Value = 1500,
        Expected = "0-1000",
        MaterialType = "Primary",
        Suggestion = "Verify data source or check unit conversion"
    ]
)
```

### 3. Document Expected Failures
```m
// When using try, ALWAYS add comment explaining why
OptionalData = 
    try Excel.CurrentWorkbook(){[Name="OptionalSheet"]}[Content]
    otherwise #table({}, {})
    // DOCUMENTED: OptionalSheet may not exist in template files,
    // this is expected behavior per specification
```

### 4. Use Error Boundaries
Isolate error-prone transformations:
```m
SafelyTransformedTable = 
    let
        TransformAttempt = try Table.TransformColumns(
            Source,
            {"amount", each Number.From(_)}
        ),
        Result = if TransformAttempt[HasError] then
            error Error.Record(
                "Transformation.Failed",
                "Failed to convert 'amount' column to numbers",
                [
                    Error = TransformAttempt[Error],
                    Suggestion = "Check for non-numeric values in source data"
                ]
            )
        else
            TransformAttempt[Value]
    in
        Result
```

## Logging Errors

For non-blocking errors that should be logged but not stop execution:

```m
#"Add Error Log" = Table.AddColumn(
    Source,
    "error_log",
    each 
        let
            Errors = {}
                & (if [emission_factor] = null then {"Missing emission factor"} else {})
                & (if [material_type] = null then {"Missing material type"} else {})
                & (if [emission_factor] <> null and [emission_factor] < 0 
                   then {"Negative emission factor"} else {})
        in
            if List.Count(Errors) = 0 then null else Text.Combine(Errors, "; "),
    type nullable text
)
```

## Checklist

Before committing a query with error handling:
- [ ] No silent `try ... otherwise` without documentation
- [ ] All error messages include diagnostic context
- [ ] Validation happens early in query (fail fast)
- [ ] Error records use structured format with category
- [ ] Required fields checked for null values
- [ ] Numeric ranges validated against specifications
- [ ] Unexpected conditions result in errors, not default values
- [ ] Optional failures are explicitly documented
- [ ] Error messages are actionable (tell user what to fix)
