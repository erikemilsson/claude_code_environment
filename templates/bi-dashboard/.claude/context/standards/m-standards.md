# Power Query M Standards

## General Conventions
- Use camelCase for step names: `removedDuplicates`, `addedCustomColumn`
- Use descriptive step names that indicate the transformation
- Keep queries focused - one query per logical data source
- Use parameters for reusable values (file paths, API URLs)

## Code Formatting
```m
let
    // Source and initial transformation
    Source = Csv.Document(
        File.Contents("C:\Data\sales.csv"),
        [
            Delimiter = ",",
            Columns = 10,
            Encoding = 65001,
            QuoteStyle = QuoteStyle.None
        ]
    ),

    // Promote headers
    promotedHeaders = Table.PromoteHeaders(
        Source,
        [PromoteAllScalars = true]
    ),

    // Type conversion
    changedTypes = Table.TransformColumnTypes(
        promotedHeaders,
        {
            {"OrderDate", type date},
            {"SalesAmount", type number},
            {"Quantity", Int64.Type}
        }
    ),

    // Filter out null values
    removedNulls = Table.SelectRows(
        changedTypes,
        each [SalesAmount] <> null and [SalesAmount] > 0
    )
in
    removedNulls
```

## Step Naming Conventions

### Standard Prefixes
- `Source`: Initial data connection
- `promoted`: Headers promoted
- `changed`: Type changes
- `removed`: Rows or columns removed
- `filtered`: Data filtered
- `added`: Columns or rows added
- `renamed`: Columns renamed
- `merged`: Tables merged
- `expanded`: Expanded columns from related table
- `grouped`: Grouped/aggregated data
- `sorted`: Sorted data
- `replaced`: Values replaced

### Examples
```m
// Good step names
let
    Source = ...,
    promotedHeaders = Table.PromoteHeaders(Source),
    changedTypes = Table.TransformColumnTypes(...),
    removedDuplicates = Table.Distinct(...),
    filteredRows = Table.SelectRows(...),
    addedCustomColumn = Table.AddColumn(...),
    renamedColumns = Table.RenameColumns(...),
    mergedTables = Table.NestedJoin(...)
in
    mergedTables

// Avoid generic names like "Step1", "Custom1", "Table1"
```

## Data Type Conversion
Always specify explicit data types for all columns:

```m
changedTypes = Table.TransformColumnTypes(
    promotedHeaders,
    {
        {"OrderID", Int64.Type},
        {"OrderDate", type date},
        {"OrderDateTime", type datetime},
        {"CustomerName", type text},
        {"SalesAmount", type number},
        {"Quantity", Int64.Type},
        {"IsProcessed", type logical}
    }
)
```

## Error Handling
Use try-otherwise for graceful error handling:

```m
// Handle potential errors in data retrieval
safeSource = try
    Csv.Document(File.Contents(FilePath))
otherwise
    #table(
        {"Column1"},
        {{"Error loading file"}}
    ),

// Handle errors in transformations
addedSafeCalculation = Table.AddColumn(
    previousStep,
    "Profit",
    each try [Revenue] - [Cost] otherwise null,
    type number
)
```

## Parameters
Create parameters for reusable values:

```m
// Parameter examples (created via Manage Parameters)
FilePath = "C:\Data\sales.csv" meta [IsParameterQuery=true, Type="Text"],
EnvironmentURL = "https://api.prod.example.com" meta [IsParameterQuery=true, Type="Text"],
StartDate = #date(2024, 1, 1) meta [IsParameterQuery=true, Type="Date"]

// Using parameters in queries
let
    Source = Csv.Document(File.Contents(FilePath)),
    filteredDate = Table.SelectRows(
        Source,
        each [Date] >= StartDate
    )
in
    filteredDate
```

## Functions
Create custom functions for reusable transformations:

```m
// Function to clean text columns
fnCleanText = (input as text) as text =>
    let
        trimmed = Text.Trim(input),
        proper = Text.Proper(trimmed),
        result = proper
    in
        result,

// Function to transform date to fiscal period
fnDateToFiscalPeriod = (inputDate as date, fiscalYearStartMonth as number) as record =>
    let
        year = Date.Year(inputDate),
        month = Date.Month(inputDate),
        fiscalYear = if month >= fiscalYearStartMonth then year else year - 1,
        fiscalQuarter = Number.RoundUp(
            (month - fiscalYearStartMonth + 1) / 3
        ),
        result = [
            FiscalYear = fiscalYear,
            FiscalQuarter = fiscalQuarter
        ]
    in
        result
```

## Merging Tables
Use appropriate join types and always specify join columns explicitly:

```m
// Merge queries (left join)
mergedWithCustomers = Table.NestedJoin(
    orders,
    {"CustomerID"},
    customers,
    {"CustomerID"},
    "CustomerData",
    JoinKind.LeftOuter
),

// Expand columns from merged table
expandedCustomerData = Table.ExpandTableColumn(
    mergedWithCustomers,
    "CustomerData",
    {"CustomerName", "Country", "Segment"},
    {"CustomerName", "CustomerCountry", "CustomerSegment"}
)
```

## Filtering
```m
// Simple filter
filteredActive = Table.SelectRows(
    Source,
    each [Status] = "Active"
),

// Complex filter with multiple conditions
filteredComplex = Table.SelectRows(
    Source,
    each
        [Status] = "Active"
        and [Revenue] > 1000
        and [Date] >= #date(2024, 1, 1)
),

// Filter using List.Contains
filteredByList = Table.SelectRows(
    Source,
    each List.Contains({"USA", "Canada", "UK"}, [Country])
)
```

## Adding Custom Columns
```m
// Simple custom column
addedProfit = Table.AddColumn(
    Source,
    "Profit",
    each [Revenue] - [Cost],
    type number
),

// Custom column with conditional logic
addedCategory = Table.AddColumn(
    Source,
    "RevenueCategory",
    each
        if [Revenue] >= 10000 then "High"
        else if [Revenue] >= 5000 then "Medium"
        else "Low",
    type text
),

// Custom column using function
addedFiscalPeriod = Table.AddColumn(
    Source,
    "FiscalPeriod",
    each fnDateToFiscalPeriod([OrderDate], 7)  // Fiscal year starts in July
)
```

## Grouping and Aggregation
```m
groupedData = Table.Group(
    Source,
    {"CustomerID", "ProductCategory"},  // Group by columns
    {
        {"TotalRevenue", each List.Sum([Revenue]), type number},
        {"OrderCount", each Table.RowCount(_), Int64.Type},
        {"AvgOrderValue", each List.Average([Revenue]), type number},
        {"FirstOrderDate", each List.Min([OrderDate]), type date},
        {"LastOrderDate", each List.Max([OrderDate]), type date}
    }
)
```

## List Operations
```m
// Get distinct values
distinctCountries = List.Distinct(Source[Country]),

// Transform list
upperCaseNames = List.Transform(
    Source[CustomerName],
    each Text.Upper(_)
),

// Filter list
largeOrders = List.Select(
    Source[OrderValue],
    each _ > 1000
),

// Sum list
totalRevenue = List.Sum(Source[Revenue])
```

## API Connections
```m
// REST API call with error handling
let
    // API endpoint with parameters
    url = EnvironmentURL & "/api/emissions?startDate=" & Date.ToText(StartDate),

    // API call with headers
    Source = try
        Json.Document(
            Web.Contents(
                url,
                [
                    Headers = [
                        #"Content-Type" = "application/json",
                        #"Authorization" = "Bearer " & APIToken
                    ],
                    Timeout = #duration(0, 0, 2, 0)  // 2 minute timeout
                ]
            )
        )
    otherwise
        error "API call failed",

    // Convert to table
    convertedToTable = Table.FromRecords(Source[data])
in
    convertedToTable
```

## Performance Optimization

### Do's
- Use Table.Buffer() for small lookup tables that are referenced multiple times
- Filter early in the transformation process
- Remove unnecessary columns early with Table.SelectColumns
- Use native connectors when available (SQL.Database, not ODBC)
- Fold operations when possible (check "View Native Query")

### Don'ts
- Avoid adding calculated columns that could be measures in DAX
- Don't add custom columns for simple calculations (do in DAX)
- Minimize use of Table.Buffer on large tables
- Avoid multiple merges when one would suffice

```m
// Good: Buffer small lookup table
let
    Source = ...,
    lookupTable = Table.Buffer(SmallLookupTable),  // < 1000 rows
    merged = Table.NestedJoin(Source, {"ID"}, lookupTable, {"ID"}, ...)
in
    merged

// Good: Remove columns early
let
    Source = Sql.Database(...),
    selectedColumns = Table.SelectColumns(
        Source,
        {"OrderID", "OrderDate", "Revenue"}  // Only needed columns
    ),
    // ... rest of transformations
in
    selectedColumns
```

## Query Folding
Verify that operations fold back to source when possible:

```m
// These operations typically fold to SQL
let
    Source = Sql.Database("server", "database"),
    filteredRows = Table.SelectRows(Source, each [Date] >= StartDate),  // Folds
    selectedColumns = Table.SelectColumns(Source, {"ID", "Name"}),      // Folds
    sortedRows = Table.Sort(filteredRows, {{"Date", Order.Ascending}})  // Folds
in
    sortedRows

// Right-click step → View Native Query to verify folding
```

## Comments and Documentation
```m
let
    // ===== Data Source =====
    // Load sales data from CSV file
    Source = Csv.Document(File.Contents(FilePath)),

    // ===== Data Cleaning =====
    // Promote first row to headers
    promotedHeaders = Table.PromoteHeaders(Source),

    // Convert columns to appropriate data types
    changedTypes = Table.TransformColumnTypes(
        promotedHeaders,
        {{"OrderDate", type date}, {"Revenue", type number}}
    ),

    // ===== Business Logic =====
    // Filter out cancelled orders and test data
    filteredRows = Table.SelectRows(
        changedTypes,
        each
            [Status] <> "Cancelled"
            and not Text.StartsWith([OrderID], "TEST")
    )
in
    filteredRows
```

## Common Patterns

### Date Table Generation
```m
let
    StartDate = #date(2020, 1, 1),
    EndDate = #date(2025, 12, 31),
    DayCount = Duration.Days(EndDate - StartDate) + 1,

    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    ConvertedToTable = Table.FromList(DateList, Splitter.SplitByNothing()),
    RenamedColumn = Table.RenameColumns(ConvertedToTable, {{"Column1", "Date"}}),

    AddedYear = Table.AddColumn(RenamedColumn, "Year", each Date.Year([Date]), Int64.Type),
    AddedQuarter = Table.AddColumn(AddedYear, "Quarter", each Date.QuarterOfYear([Date]), Int64.Type),
    AddedMonth = Table.AddColumn(AddedQuarter, "Month", each Date.Month([Date]), Int64.Type),
    AddedMonthName = Table.AddColumn(AddedMonth, "MonthName", each Date.MonthName([Date]), type text)
in
    AddedMonthName
```

### Unpivot Pattern
```m
// Transform from wide to long format
let
    Source = ...,
    unpivotedData = Table.UnpivotOtherColumns(
        Source,
        {"ID", "Name"},           // Columns to keep
        "Attribute",               // Name for attribute column
        "Value"                    // Name for value column
    )
in
    unpivotedData
```
