# DAX Standards

## General Conventions
- Use UPPERCASE for DAX functions: `CALCULATE`, `FILTER`, `SUM`
- Use PascalCase for measure names: `TotalRevenue`, `YoYGrowth`
- Use descriptive names that indicate what is being measured
- Add measure descriptions in Properties pane

## Measure Organization
- Group related measures in dedicated tables (e.g., "_Measures")
- Use display folders to organize measures logically
- Prefix time intelligence measures: `YTD Sales`, `PY Revenue`
- Prefix KPIs with indicator: `KPI_SalesTarget`

## Formatting Standards

### Measures
```dax
-- Good: Multi-line format for complex measures
Total Sales =
CALCULATE (
    SUM ( Sales[SalesAmount] ),
    Sales[Status] = "Completed"
)

-- Good: Single line for simple measures
Total Quantity = SUM ( Sales[Quantity] )

-- Use variables for complex calculations
Sales YoY Growth % =
VAR CurrentYearSales =
    CALCULATE ( [Total Sales], DATESYTD ( 'Date'[Date] ) )
VAR PreviousYearSales =
    CALCULATE ( [Total Sales], DATESYTD ( DATEADD ( 'Date'[Date], -1, YEAR ) ) )
VAR GrowthRate =
    DIVIDE (
        CurrentYearSales - PreviousYearSales,
        PreviousYearSales
    )
RETURN
    GrowthRate
```

### Calculated Columns
```dax
-- Use calculated columns sparingly (they consume memory)
-- Prefer measures when possible

-- Calculated Column (when needed)
Profit Margin =
DIVIDE (
    Sales[Revenue] - Sales[Cost],
    Sales[Revenue],
    0  -- Alternate result if division by zero
)
```

## Variables (VAR)
- Use variables for repeated calculations
- Use descriptive variable names
- Calculate once, reference multiple times
- Improves performance and readability

```dax
Revenue vs Target % =
VAR ActualRevenue = [Total Revenue]
VAR TargetRevenue = [Revenue Target]
VAR VariancePercent =
    DIVIDE (
        ActualRevenue - TargetRevenue,
        TargetRevenue
    )
RETURN
    VariancePercent
```

## Time Intelligence
- Always use a proper Date table (contiguous dates, marked as Date Table)
- Use built-in time intelligence functions: `DATESYTD`, `DATEADD`, `SAMEPERIODLASTYEAR`
- Create standard time intelligence measures for consistency

### Standard Time Intelligence Patterns
```dax
-- Year To Date
YTD Sales =
CALCULATE (
    [Total Sales],
    DATESYTD ( 'Date'[Date] )
)

-- Previous Year
PY Sales =
CALCULATE (
    [Total Sales],
    SAMEPERIODLASTYEAR ( 'Date'[Date] )
)

-- Month To Date
MTD Sales =
CALCULATE (
    [Total Sales],
    DATESMTD ( 'Date'[Date] )
)

-- Rolling 12 Months
Rolling 12M Sales =
CALCULATE (
    [Total Sales],
    DATESINPERIOD (
        'Date'[Date],
        LASTDATE ( 'Date'[Date] ),
        -12,
        MONTH
    )
)
```

## CALCULATE Best Practices
- Use CALCULATE for context modification
- Place measure first, then filters
- Use clear, explicit filters
- Avoid ALL() when possible (use REMOVEFILTERS instead)

```dax
-- Good: Explicit and clear
Sales High Value =
CALCULATE (
    [Total Sales],
    Sales[OrderValue] > 1000
)

-- Better: Use REMOVEFILTERS instead of ALL
All Region Sales =
CALCULATE (
    [Total Sales],
    REMOVEFILTERS ( Region[RegionName] )
)
```

## Filter Context
- Understand row context vs filter context
- Use CALCULATE to create filter context
- Use FILTER for complex conditions
- Be mindful of circular dependencies

```dax
-- Using FILTER for complex conditions
High Value Customers Revenue =
CALCULATE (
    [Total Revenue],
    FILTER (
        Customers,
        [Customer Lifetime Value] > 10000
            && Customers[Status] = "Active"
    )
)
```

## Performance Optimization

### Do's
- Use variables to avoid recalculation
- Use SELECTEDVALUE instead of VALUES when expecting single value
- Minimize use of calculated columns (use measures)
- Use DIVIDE instead of dividing with / (handles division by zero)
- Filter on dimension tables, not fact tables when possible

### Don'ts
- Avoid iterators (SUMX, AVERAGEX) when simple aggregations work
- Don't use FILTER on large tables without need
- Avoid ALL() when REMOVEFILTERS is sufficient
- Don't create circular dependencies

```dax
-- Slow: Iterator on large table
Total Revenue Slow =
SUMX (
    Sales,
    Sales[Quantity] * Sales[Price]
)

-- Fast: Use calculated column or existing field
Total Revenue Fast =
SUM ( Sales[Revenue] )  -- Assuming Revenue column exists
```

## Error Handling
- Always handle division by zero with DIVIDE
- Use ISBLANK, IFERROR for null handling
- Provide meaningful alternate results

```dax
Profit Margin % =
DIVIDE (
    [Total Profit],
    [Total Revenue],
    0  -- Return 0 if revenue is 0
)

-- Handle blanks explicitly
Sales With Fallback =
VAR Sales = [Total Sales]
RETURN
    IF ( ISBLANK ( Sales ), 0, Sales )
```

## Naming Conventions

### Measures
- Descriptive and business-friendly: `Total Sales`, `Average Order Value`
- Include aggregation type if not obvious: `Count of Orders`, `Distinct Customers`
- Time-based prefix: `YTD Revenue`, `MTD Orders`, `PY Profit`

### Tables
- Plural nouns: `Sales`, `Customers`, `Products`
- Dimension prefix optional: `Dim_Customer`, `Fact_Sales`
- Measure tables: `_Measures` (underscore prefix hides from report view)

### Columns
- PascalCase: `OrderDate`, `CustomerName`, `ProductCategory`
- Avoid abbreviations unless industry standard
- Be specific: `OrderDate` not `Date`, `SalesAmount` not `Amount`

## Testing Measures
- Verify measures with known data samples
- Test edge cases (blanks, zeros, negative values)
- Compare with source system results
- Document expected behavior in descriptions

## Comments
```dax
-- Use comments to explain complex logic
-- Not needed for simple, obvious measures

Top 10 Customers Revenue =
// Calculate revenue for top 10 customers by total revenue
// Returns blank if fewer than 10 customers exist
VAR TopCustomers =
    TOPN (
        10,
        VALUES ( Customer[CustomerID] ),
        [Total Revenue],
        DESC
    )
VAR Revenue =
    CALCULATE (
        [Total Revenue],
        TopCustomers
    )
RETURN
    Revenue
```

## Common Patterns

### Conditional Formatting Helper
```dax
// Returns 1, 0, or -1 for conditional formatting
Revenue Indicator =
VAR Actual = [Total Revenue]
VAR Target = [Revenue Target]
VAR Result =
    SWITCH (
        TRUE (),
        Actual >= Target * 1.05, 1,      // Green: Exceeds by 5%+
        Actual >= Target * 0.95, 0,      // Yellow: Within 5%
        -1                                // Red: Below by 5%+
    )
RETURN
    Result
```

### Rank Calculation
```dax
Product Rank by Sales =
RANKX (
    ALL ( Product[ProductName] ),
    [Total Sales],
    ,
    DESC,
    DENSE
)
```

### Dynamic Top N
```dax
Top N Sales =
VAR TopNValue = SELECTEDVALUE ( 'Parameters'[TopN], 10 )
VAR Result =
    CALCULATE (
        [Total Sales],
        TOPN (
            TopNValue,
            ALL ( Product[ProductName] ),
            [Total Sales],
            DESC
        )
    )
RETURN
    Result
```
