# Power Query (M Language) Guidelines

*Language-specific patterns - see core.md for shared principles.*

## Query Structure
```powerquery
let
    // Clear step names
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    SalesData = Source{[Item="Sales",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(SalesData),

    // Explicit types
    TypedColumns = Table.TransformColumnTypes(
        PromotedHeaders,
        {{"OrderID", Int64.Type}, {"OrderDate", type datetime}}
    )
in
    TypedColumns
```

## Error Handling
```powerquery
SafeLoad =
    try Excel.Workbook(File.Contents(FilePath))
    otherwise error Error.Record("DataSourceError", "Failed to load: " & FilePath),

SafeDivision =
    if [Denominator] = 0 or [Denominator] = null
    then null
    else [Numerator] / [Denominator]
```

## Performance Optimization
```powerquery
-- Buffer frequently accessed tables
BufferedSource = Table.Buffer(Source),

-- Filter and select columns early
FilteredData = Table.SelectRows(
    Table.SelectColumns(Source, {"ID", "Value"}),
    each [Date] >= #date(2024, 1, 1)
)
```

## Custom Functions
```powerquery
let
    CleanText = (input as nullable text) as nullable text =>
        if input = null then null
        else Text.Trim(Text.Proper(input)),

    // Document function
    FunctionType = type function (input as nullable text) as nullable text
        meta [Documentation.Name = "CleanText"]
in
    Value.ReplaceType(CleanText, FunctionType)
```

## Joining Tables
```powerquery
MergedData = Table.NestedJoin(
    Orders, {"CustomerID"},
    Customers, {"CustomerID"},
    "CustomerDetails",
    JoinKind.LeftOuter
),
ExpandedCustomer = Table.ExpandTableColumn(
    MergedData, "CustomerDetails",
    {"CustomerName", "Country"}
)
```

## Quick Reference

| Operation | Use | Avoid |
|-----------|-----|-------|
| Multiple filters | Combined condition | Separate steps |
| Repeated table access | Table.Buffer | Direct reference |
| Column selection | Table.SelectColumns early | Keep all columns |
| Text operations | Text.* functions | Manual string building |
| Type assignment | Explicit types | Implicit conversion |
| Query folding | Native operations | Custom functions (breaks folding) |
