# Pattern: DAX Measure

## Metadata
- **ID**: pattern-microsoft-dax-measure
- **Version**: 1.0.0
- **Category**: microsoft-stack
- **Difficulty Range**: 4-6 (DAX measure creation tasks)

## Triggers
Keywords that suggest this pattern applies:
- dax measure
- create measure
- power bi measure
- semantic model measure
- calculated measure
- aggregation
- kpi

File types: .dax

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| measure_name | string | yes | Name following conventions (e.g., Total Sales) |
| description | string | yes | What the measure calculates |
| formula | string | yes | DAX formula expression |
| format_string | string | no | Display format (e.g., "#,##0.00", "0.0%") |
| display_folder | string | no | Folder for organizing measures |
| use_variables | boolean | no | Use VAR pattern (default: true) |

## Pre-Conditions
- [ ] All referenced columns/tables exist in model
- [ ] Measure name is unique in model
- [ ] Formula syntax is valid DAX
- [ ] Understanding of filter context
- [ ] Format string matches data type

## Template

### Standard Measure Pattern
```dax
{{measure_name}} =
-- Description: {{description}}
-- Created: {{timestamp}}
-- Display Folder: {{display_folder}}
{{#if use_variables}}
VAR {{variable_definitions}}
RETURN
    {{return_expression}}
{{else}}
{{formula}}
{{/if}}
```

### With Error Handling
```dax
{{measure_name}} =
-- Description: {{description}}
-- Created: {{timestamp}}
VAR _Result =
    {{formula}}
VAR _ErrorCheck =
    IF(
        ISBLANK(_Result) || ISERROR(_Result),
        BLANK(),
        _Result
    )
RETURN
    _ErrorCheck
```

## Post-Conditions
- [ ] Measure evaluates without error
- [ ] Format string applied correctly
- [ ] Appears in correct display folder
- [ ] Returns expected values for test cases
- [ ] Performance is acceptable (<1s for typical queries)
- [ ] Filter context behaves correctly

## Anti-Patterns
**DON'T do this:**
- Use CALCULATE without understanding filter context
- Reference measures within iterator functions (SUMX, AVERAGEX) row context
- Hardcode filter values (use parameters or slicers)
- Skip error handling for DIVIDE operations
- Create circular references between measures
- Use FILTER instead of CALCULATETABLE for table filters
- Nest too many CALCULATE calls (>3 levels)
- Forget to use VAR for complex calculations

**WHY**:
- CALCULATE context errors produce incorrect results silently
- Measures in row context don't work as expected (use columns)
- Hardcoded filters aren't dynamic and break reports
- Division by zero crashes reports
- Circular references prevent model refresh
- FILTER is slower than CALCULATETABLE for most scenarios
- Deep nesting is hard to debug and slow
- Repeated calculations waste performance

## Examples

### Example 1: Simple Aggregation
**Input:**
```
measure_name: Total Sales
description: Sum of all sales amounts
formula: SUM('Sales'[Amount])
format_string: $#,##0.00
display_folder: Sales Metrics
use_variables: true
```

**Output:**
```dax
Total Sales =
-- Description: Sum of all sales amounts
-- Created: 2025-12-05
-- Display Folder: Sales Metrics
VAR _TotalSales =
    SUM('Sales'[Amount])
RETURN
    _TotalSales

-- Format: $#,##0.00
```

### Example 2: Year-over-Year Comparison
**Input:**
```
measure_name: Sales YoY %
description: Year-over-year sales growth percentage
formula: DIVIDE([Total Sales] - [Total Sales PY], [Total Sales PY])
format_string: 0.0%
display_folder: Sales Metrics
use_variables: true
```

**Output:**
```dax
Sales YoY % =
-- Description: Year-over-year sales growth percentage
-- Created: 2025-12-05
-- Display Folder: Sales Metrics
VAR _CurrentSales = [Total Sales]
VAR _PriorYearSales = [Total Sales PY]
VAR _YoYGrowth =
    DIVIDE(
        _CurrentSales - _PriorYearSales,
        _PriorYearSales,
        BLANK()  -- Return BLANK() if division by zero
    )
RETURN
    _YoYGrowth

-- Format: 0.0%
```

### Example 3: Complex Calculation with Multiple Filters
**Input:**
```
measure_name: Premium Product Sales
description: Total sales for premium products in active regions
formula: CALCULATE([Total Sales], Products[Category] = "Premium", Regions[Status] = "Active")
format_string: $#,##0.00
display_folder: Advanced Metrics
use_variables: true
```

**Output:**
```dax
Premium Product Sales =
-- Description: Total sales for premium products in active regions
-- Created: 2025-12-05
-- Display Folder: Advanced Metrics
VAR _PremiumSales =
    CALCULATE(
        [Total Sales],
        Products[Category] = "Premium",
        Regions[Status] = "Active"
    )
VAR _ErrorCheck =
    IF(
        ISBLANK(_PremiumSales),
        0,  -- Return 0 instead of BLANK for this business requirement
        _PremiumSales
    )
RETURN
    _ErrorCheck

-- Format: $#,##0.00
```

### Example 4: Time Intelligence
**Input:**
```
measure_name: Sales MTD
description: Month-to-date sales
formula: TOTALMTD([Total Sales], 'Calendar'[Date])
format_string: $#,##0.00
display_folder: Time Intelligence
use_variables: true
```

**Output:**
```dax
Sales MTD =
-- Description: Month-to-date sales
-- Created: 2025-12-05
-- Display Folder: Time Intelligence
VAR _MTDSales =
    TOTALMTD(
        [Total Sales],
        'Calendar'[Date]
    )
RETURN
    _MTDSales

-- Format: $#,##0.00
```

### Example 5: Ranking Measure
**Input:**
```
measure_name: Product Sales Rank
description: Rank products by sales amount
formula: RANKX(ALL(Products[ProductName]), [Total Sales], , DESC, DENSE)
format_string: #,##0
display_folder: Rankings
use_variables: true
```

**Output:**
```dax
Product Sales Rank =
-- Description: Rank products by sales amount
-- Created: 2025-12-05
-- Display Folder: Rankings
VAR _ProductSales = [Total Sales]
VAR _Rank =
    RANKX(
        ALL(Products[ProductName]),
        [Total Sales],
        ,  -- No value parameter (uses current context)
        DESC,  -- Highest sales = Rank 1
        DENSE  -- No gaps in ranking
    )
RETURN
    IF(
        ISBLANK(_ProductSales),
        BLANK(),  -- Don't rank products with no sales
        _Rank
    )

-- Format: #,##0
```

### Example 6: Ratio Calculation
**Input:**
```
measure_name: Profit Margin %
description: Profit as percentage of sales
formula: DIVIDE([Total Profit], [Total Sales])
format_string: 0.00%
display_folder: Profitability
use_variables: true
```

**Output:**
```dax
Profit Margin % =
-- Description: Profit as percentage of sales
-- Created: 2025-12-05
-- Display Folder: Profitability
VAR _Profit = [Total Profit]
VAR _Sales = [Total Sales]
VAR _Margin =
    DIVIDE(
        _Profit,
        _Sales,
        BLANK()  -- Return BLANK() if no sales (avoid division by zero)
    )
RETURN
    _Margin

-- Format: 0.00%
```

## Usage Notes

### VAR Pattern Benefits
Using variables in DAX:
1. **Performance**: Calculation happens once, referenced multiple times
2. **Readability**: Complex formulas broken into logical steps
3. **Debugging**: Each step can be tested independently
4. **Maintainability**: Changes easier to make

### Filter Context vs Row Context
- **Filter Context**: Created by slicers, filters, rows/columns in visual
- **Row Context**: Created by iterators (SUMX, FILTER, etc.)
- **Key Rule**: Measures work in filter context, columns in row context

### Common DAX Functions
**Aggregations:**
- `SUM()`, `AVERAGE()`, `MIN()`, `MAX()`, `COUNT()`, `DISTINCTCOUNT()`

**Filter Modification:**
- `CALCULATE()` - Modify filter context
- `CALCULATETABLE()` - Return filtered table
- `ALL()`, `ALLEXCEPT()`, `ALLSELECTED()` - Remove filters

**Time Intelligence:**
- `TOTALMTD()`, `TOTALQTD()`, `TOTALYTD()` - Period-to-date
- `SAMEPERIODLASTYEAR()`, `DATEADD()` - Time comparisons

**Logical:**
- `IF()`, `SWITCH()` - Conditional logic
- `ISBLANK()`, `ISERROR()` - Error checking
- `AND()`, `OR()`, `NOT()` - Boolean operations

**Math:**
- `DIVIDE()` - Safe division (handles divide-by-zero)
- `ROUND()`, `CEILING()`, `FLOOR()` - Rounding
- `ABS()`, `SIGN()` - Absolute value, sign

### Format Strings
Common format patterns:
- Currency: `$#,##0.00` or `"$"#,##0.00`
- Percentage: `0.00%` or `0.0%`
- Integer: `#,##0`
- Decimal: `#,##0.00`
- Custom: `"▲"#,##0;"▼"#,##0` (up/down arrows)

### Performance Best Practices
1. **Use variables** to avoid recalculation
2. **Filter early** (narrow context before calculation)
3. **Use DIVIDE()** instead of manual IF(x=0) checks
4. **Avoid FILTER()** on large tables (use CALCULATE instead)
5. **Use SELECTEDVALUE()** for single-value contexts
6. **Avoid nesting CALCULATE** more than 3 levels deep

## Testing Checklist
After creating measure:
- [ ] Test with different filter contexts (slicers, visuals)
- [ ] Verify totals are correct (not sum of detail)
- [ ] Test with empty/blank filters
- [ ] Check performance with large datasets
- [ ] Validate format string displays correctly
- [ ] Test edge cases (zeros, nulls, extremes)
- [ ] Verify measure appears in correct folder
- [ ] Document dependencies on other measures

## Common Patterns

### Prior Period Comparison
```dax
Sales PY =
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR('Calendar'[Date])
)
```

### Conditional Aggregation
```dax
Large Orders =
CALCULATE(
    [Total Sales],
    Sales[Amount] > 1000
)
```

### Running Total
```dax
Sales Running Total =
CALCULATE(
    [Total Sales],
    FILTER(
        ALL('Calendar'[Date]),
        'Calendar'[Date] <= MAX('Calendar'[Date])
    )
)
```

### Parent-Child Hierarchy
```dax
Sales with Parent =
VAR _CurrentSales = [Total Sales]
VAR _ParentSales =
    CALCULATE(
        [Total Sales],
        RELATEDTABLE(ChildTable)
    )
RETURN
    _CurrentSales + _ParentSales
```

## Related Patterns
- `power-query-silver.pattern.md` - Data preparation for measures
- `dataflow-gen2.pattern.md` - For Fabric semantic models
- Power BI report patterns

## Debugging Tips
1. **Use DAX Studio** for testing and optimization
2. **Check measure dependencies** with model view
3. **Use CONCATENATEX()** to see filter context
4. **Add temporary measures** to debug intermediate steps
5. **Use Performance Analyzer** in Power BI to find slow measures
