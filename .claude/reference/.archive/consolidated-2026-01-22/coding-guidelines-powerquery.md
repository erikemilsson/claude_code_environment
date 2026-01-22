# Power Query (M Language) Coding Guidelines for Claude 4

## M Language Best Practices

### 1. Query Structure and Readability

```powerquery
// GOOD: Clear step names and structure
let
    // Data source
    Source = Excel.Workbook(File.Contents("C:\Data\Sales.xlsx"), null, true),

    // Select the Sales sheet
    SalesData = Source{[Item="Sales",Kind="Sheet"]}[Data],

    // Promote headers
    PromotedHeaders = Table.PromoteHeaders(SalesData, [PromoteAllScalars=true]),

    // Define column types explicitly
    TypedColumns = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"OrderID", Int64.Type},
            {"OrderDate", type datetime},
            {"ProductID", type text},
            {"Quantity", Int64.Type},
            {"UnitPrice", Currency.Type},
            {"CustomerID", type text}
        }
    ),

    // Add calculated columns
    AddedTotalPrice = Table.AddColumn(
        TypedColumns,
        "TotalPrice",
        each [Quantity] * [UnitPrice],
        Currency.Type
    ),

    // Filter for current year
    CurrentYearOnly = Table.SelectRows(
        AddedTotalPrice,
        each Date.Year([OrderDate]) = Date.Year(DateTime.LocalNow())
    )
in
    CurrentYearOnly

// BAD: Unclear step names, no structure
let
    a = Excel.Workbook(File.Contents("C:\Data\Sales.xlsx"), null, true),
    b = a{[Item="Sales",Kind="Sheet"]}[Data],
    c = Table.PromoteHeaders(b),
    d = Table.TransformColumnTypes(c,{{"OrderID", Int64.Type},{"OrderDate", type datetime}}),
    e = Table.AddColumn(d, "TotalPrice", each [Quantity] * [UnitPrice])
in e
```

### 2. Error Handling

```powerquery
// GOOD: Robust error handling
let
    SafeDataLoad =
        try
            Excel.Workbook(File.Contents(FilePath), null, true)
        otherwise
            error Error.Record(
                "DataSourceError",
                "Failed to load file: " & FilePath,
                FilePath
            ),

    // Check if load succeeded
    ValidatedSource =
        if SafeDataLoad[HasError]
        then error SafeDataLoad[Error]
        else SafeDataLoad[Value],

    // Safe column operations
    SafeColumnAdd =
        try
            Table.AddColumn(
                SourceTable,
                "Ratio",
                each if [Denominator] = 0 or [Denominator] = null
                     then null
                     else [Numerator] / [Denominator],
                type nullable number
            )
        otherwise
            Table.AddColumn(
                SourceTable,
                "Ratio",
                each null,
                type nullable number
            )
in
    SafeColumnAdd

// BAD: No error handling
let
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    AddRatio = Table.AddColumn(Source, "Ratio", each [Numerator]/[Denominator])
in AddRatio
```

### 3. Performance Optimization

```powerquery
// GOOD: Optimize for performance
let
    // Buffer tables that are referenced multiple times
    BufferedSource = Table.Buffer(Source),

    // Use Table.SelectColumns early to reduce data volume
    RequiredColumns = Table.SelectColumns(
        BufferedSource,
        {"OrderID", "ProductID", "Quantity", "UnitPrice", "OrderDate"}
    ),

    // Filter early before expensive operations
    FilteredData = Table.SelectRows(
        RequiredColumns,
        each [OrderDate] >= #date(2024, 1, 1)
    ),

    // Use List.Buffer for frequently accessed lists
    ProductList = List.Buffer(
        List.Distinct(FilteredData[ProductID])
    ),

    // Avoid repeated calculations
    AddCalculations = Table.AddColumn(
        FilteredData,
        "TotalWithTax",
        (row) =>
            let
                baseAmount = row[Quantity] * row[UnitPrice],
                taxRate = 0.08
            in
                baseAmount * (1 + taxRate),
        Currency.Type
    )
in
    AddCalculations

// BAD: Performance issues
let
    // No buffering, multiple references cause re-evaluation
    Source = Excel.CurrentWorkbook(){[Name="Data"]}[Content],

    // Late filtering after expensive operations
    AllCalculations = Table.AddColumn(Source, "Complex", each ComplexFunction([Value])),
    Filtered = Table.SelectRows(AllCalculations, each [Date] >= #date(2024, 1, 1))
in Filtered
```

### 4. Custom Functions

```powerquery
// GOOD: Well-structured custom function
let
    CleanTextFunction = (inputText as nullable text) as nullable text =>
        let
            // Handle null input
            CheckNull = if inputText = null then null else inputText,

            // Clean operations
            TrimmedText = Text.Trim(CheckNull),
            CleanedSpaces = Text.Replace(TrimmedText, "  ", " "),
            ProperCase = Text.Proper(CleanedSpaces),

            // Remove special characters
            RemoveSpecial = Text.Remove(ProperCase, {"#", "@", "!", "$"})
        in
            if CheckNull = null then null else RemoveSpecial,

    // Document the function
    FunctionType = type function (
        inputText as nullable text
    ) as nullable text meta [
        Documentation.Name = "CleanTextFunction",
        Documentation.Description = "Cleans and standardizes text input",
        Documentation.Examples = {[
            Description = "Clean a messy string",
            Code = "CleanTextFunction(""  HELLO world!  "")",
            Result = "Hello World"
        ]}
    ]
in
    Value.ReplaceType(CleanTextFunction, FunctionType)
```

### 5. Date Handling

```powerquery
// GOOD: Robust date handling
let
    // Create date table with proper typing
    StartDate = #date(2020, 1, 1),
    EndDate = Date.From(DateTime.LocalNow()),

    DateList = List.Dates(
        StartDate,
        Duration.Days(EndDate - StartDate) + 1,
        #duration(1, 0, 0, 0)
    ),

    DateTable = Table.FromList(
        DateList,
        Splitter.SplitByNothing(),
        type table [Date = date]
    ),

    // Add date dimensions
    AddedColumns = Table.AddColumn(DateTable, "Year", each Date.Year([Date]), Int64.Type),
    AddedQuarter = Table.AddColumn(AddedColumns, "Quarter", each Date.QuarterOfYear([Date]), Int64.Type),
    AddedMonth = Table.AddColumn(AddedQuarter, "Month", each Date.Month([Date]), Int64.Type),
    AddedMonthName = Table.AddColumn(AddedMonth, "MonthName", each Date.MonthName([Date]), type text),
    AddedWeekday = Table.AddColumn(AddedMonthName, "Weekday", each Date.DayOfWeekName([Date]), type text),

    // Add fiscal year (assuming July 1 start)
    AddedFiscalYear = Table.AddColumn(
        AddedWeekday,
        "FiscalYear",
        each if Date.Month([Date]) >= 7
             then Date.Year([Date]) + 1
             else Date.Year([Date]),
        Int64.Type
    )
in
    AddedFiscalYear
```

### 6. Dynamic Column References

```powerquery
// GOOD: Dynamic and maintainable
let
    Source = Table.FromRecords({[A=1,B=2,C=3],[A=4,B=5,C=6]}),

    // Define column mappings
    ColumnMappings = [
        OldName = {"A", "B", "C"},
        NewName = {"ProductID", "Quantity", "Price"}
    ],

    // Dynamic rename
    RenamedColumns = Table.RenameColumns(
        Source,
        List.Zip({ColumnMappings[OldName], ColumnMappings[NewName]})
    ),

    // Dynamic type assignment
    ColumnTypes = {
        {"ProductID", type text},
        {"Quantity", Int64.Type},
        {"Price", Currency.Type}
    },

    TypedTable = Table.TransformColumnTypes(RenamedColumns, ColumnTypes)
in
    TypedTable

// BAD: Hardcoded and brittle
let
    Source = Table.FromRecords({[A=1,B=2,C=3],[A=4,B=5,C=6]}),
    Renamed = Table.RenameColumns(Source,{{"A", "ProductID"}, {"B", "Quantity"}, {"C", "Price"}})
in Renamed
```

### 7. Merging and Joining

```powerquery
// GOOD: Efficient joining with error handling
let
    // Main data
    Orders = Table.Buffer(OrdersSource),
    Customers = Table.Buffer(CustomersSource),

    // Perform merge with null handling
    MergedData = Table.NestedJoin(
        Orders,
        {"CustomerID"},
        Customers,
        {"CustomerID"},
        "CustomerDetails",
        JoinKind.LeftOuter
    ),

    // Expand with specific columns
    ExpandedCustomer = Table.ExpandTableColumn(
        MergedData,
        "CustomerDetails",
        {"CustomerName", "Country", "Segment"},
        {"CustomerName", "Country", "Segment"}
    ),

    // Handle missing customer data
    CleanedData = Table.ReplaceValue(
        ExpandedCustomer,
        null,
        "Unknown",
        Replacer.ReplaceValue,
        {"CustomerName", "Country", "Segment"}
    )
in
    CleanedData
```

### 8. Grouping and Aggregation

```powerquery
// GOOD: Complex aggregations with multiple statistics
let
    GroupedData = Table.Group(
        Source,
        {"ProductCategory", "Region"},
        {
            {"TotalQuantity", each List.Sum([Quantity]), type number},
            {"AveragePrice", each List.Average([Price]), type number},
            {"MinPrice", each List.Min([Price]), type number},
            {"MaxPrice", each List.Max([Price]), type number},
            {"OrderCount", each Table.RowCount(_), Int64.Type},
            {"UniqueCustomers", each List.Count(List.Distinct([CustomerID])), Int64.Type},

            // Keep all rows for drill-down
            {"Details", each _, type table},

            // Custom aggregation
            {"PriceRange", each List.Max([Price]) - List.Min([Price]), type number}
        }
    ),

    // Add calculated metrics after grouping
    AddedMetrics = Table.AddColumn(
        GroupedData,
        "AvgOrderSize",
        each [TotalQuantity] / [OrderCount],
        type number
    )
in
    AddedMetrics
```

### 9. Parameters and Dynamic Queries

```powerquery
// GOOD: Parameterized query
let
    // Parameters (can be set from Excel)
    StartDateParam = #date(2024, 1, 1),
    EndDateParam = #date(2024, 12, 31),
    MinOrderValue = 1000,

    // Dynamic source path
    DataPath = Excel.CurrentWorkbook(){[Name="ConfigTable"]}[Content]{0}[FilePath],

    // Load and filter with parameters
    Source = Excel.Workbook(File.Contents(DataPath), null, true),
    FilteredData = Table.SelectRows(
        Source,
        each [OrderDate] >= StartDateParam
         and [OrderDate] <= EndDateParam
         and [TotalValue] >= MinOrderValue
    )
in
    FilteredData
```

### 10. Common Patterns and Solutions

#### Unpivoting Data
```powerquery
// GOOD: Flexible unpivot
let
    Source = SalesTable,

    // Keep identifier columns
    UnpivotedData = Table.UnpivotOtherColumns(
        Source,
        {"ProductID", "ProductName"},
        "Month",
        "Sales"
    ),

    // Parse month to date
    AddedDate = Table.AddColumn(
        UnpivotedData,
        "Date",
        each Date.FromText([Month] & "-01"),
        type date
    )
in
    AddedDate
```

#### Handling Multiple File Sources
```powerquery
// GOOD: Combine files from folder
let
    Source = Folder.Files("C:\Data\Monthly"),

    // Filter to Excel files only
    FilteredFiles = Table.SelectRows(Source, each [Extension] = ".xlsx"),

    // Add custom column with file contents
    AddedContent = Table.AddColumn(
        FilteredFiles,
        "FileContent",
        each Excel.Workbook([Content], null, true)
    ),

    // Expand and combine
    CombinedData = Table.Combine(
        Table.TransformColumns(
            AddedContent,
            {
                "FileContent",
                each _{[Item="Sheet1",Kind="Sheet"]}[Data]
            }
        )[FileContent]
    )
in
    CombinedData
```

## Anti-Patterns to Avoid

### 1. Type Confusion
```powerquery
// BAD: Implicit type conversions
Table.AddColumn(Source, "Total", each [Quantity] & [Price])

// GOOD: Explicit typing
Table.AddColumn(Source, "Total", each [Quantity] * [Price], Currency.Type)
```

### 2. Inefficient Filtering
```powerquery
// BAD: Multiple filter steps
let
    Filter1 = Table.SelectRows(Source, each [Year] = 2024),
    Filter2 = Table.SelectRows(Filter1, each [Month] = 1),
    Filter3 = Table.SelectRows(Filter2, each [Status] = "Active")
in Filter3

// GOOD: Combined filter
Table.SelectRows(Source, each [Year] = 2024 and [Month] = 1 and [Status] = "Active")
```

### 3. Not Using Query Folding
```powerquery
// BAD: Breaks query folding
let
    Source = Sql.Database("server", "database"),
    AllData = Source{[Schema="dbo",Item="LargeTable"]}[Data],
    // This custom function breaks folding
    Filtered = Table.SelectRows(AllData, each CustomFunction([Column]))
in Filtered

// GOOD: Maintain query folding
let
    Source = Sql.Database("server", "database"),
    FilteredAtSource = Table.SelectRows(
        Source{[Schema="dbo",Item="LargeTable"]}[Data],
        each [StandardColumn] = "Value"  // Native operations maintain folding
    )
in FilteredAtSource
```

## Performance Checklist

1. ✅ Filter data as early as possible
2. ✅ Use Table.Buffer for repeatedly accessed tables
3. ✅ Select only needed columns early
4. ✅ Maintain query folding when possible
5. ✅ Use native M functions over custom functions
6. ✅ Avoid unnecessary type conversions
7. ✅ Group operations to minimize steps
8. ✅ Use parameters for reusable queries
9. ✅ Handle errors explicitly
10. ✅ Document complex logic

## Quick Reference

| Operation | Use | Avoid |
|-----------|-----|-------|
| Multiple filters | Combined condition | Separate steps |
| Repeated table access | Table.Buffer | Direct reference |
| Column selection | Table.SelectColumns early | Keep all columns |
| Text operations | Text.* functions | Manual string building |
| Date calculations | Date.* functions | Text manipulation |
| Null handling | Explicit null checks | Assuming non-null |
| Type assignment | Explicit types | Implicit conversion |
| Error handling | try...otherwise | No error handling |