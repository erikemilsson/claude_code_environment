# Power Query Standards

## M Code Conventions

### Naming Conventions
- **Functions**: `fnPascalCase` (e.g., `fnCalculatePension`)
- **Variables**: `camelCase` (e.g., `currentValue`)
- **Parameters**: `PascalCase` (e.g., `ContributionAmount`)
- **Tables**: `PascalCase` (e.g., `FactContributions`)
- **Columns**: `PascalCase` (e.g., `EmployeeName`)

### Code Structure
```powerquery
let
    // Step 1: Source definition
    Source = Excel.Workbook(File.Contents(FilePath)),

    // Step 2: Data selection
    Data = Source{[Name="Sheet1"]}[Data],

    // Step 3: Type conversion
    TypedData = Table.TransformColumnTypes(Data, {
        {"Date", type date},
        {"Amount", type number}
    }),

    // Step 4: Business logic
    Calculated = Table.AddColumn(TypedData, "Tax",
        each [Amount] * 0.2, type number)
in
    Calculated
```

## DAX Best Practices

### Measure Patterns
```dax
Total Contributions =
VAR Result =
    SUMX(
        FactContributions,
        FactContributions[Amount]
    )
RETURN
    Result

YTD Contributions =
CALCULATE(
    [Total Contributions],
    DATESYTD(DimDate[Date])
)
```

### Formatting Rules
- One calculation per line in complex measures
- Use VAR for intermediate calculations
- Always include RETURN statement
- Comment complex logic

## Query Folding Rules

### Preserve Folding
✓ Filter before other operations
✓ Use native database functions
✓ Avoid custom columns when possible
✓ Keep transformations simple

### Breaking Folding
✗ Custom M functions
✗ Index columns
✗ Pivoting operations
✗ Complex conditional columns

## Performance Guidelines

### Optimization Checklist
1. **Reduce data early**: Filter at source
2. **Use query folding**: Check folding indicators
3. **Minimize columns**: Remove unused fields
4. **Buffer tables**: For multiple references
5. **Incremental refresh**: For large datasets

### Anti-Patterns to Avoid
- Nested loops in M
- Row-by-row operations
- Unnecessary type conversions
- Redundant merges
- Complex calculated columns (use DAX)

## Error Handling

### M Code Error Handling
```powerquery
try
    [Calculation]
otherwise
    null
```

### DAX Error Handling
```dax
Safe Division =
DIVIDE(
    [Numerator],
    [Denominator],
    0  // Default value if error
)
```

## Common LLM Pitfalls

### Things AI Often Gets Wrong
1. **Confusing M and DAX syntax** - Different languages, different contexts
2. **Ignoring query folding** - Critical for performance
3. **Wrong context transitions** - CALCULATE changes context
4. **Inefficient iterators** - SUMX vs SUM
5. **Type confusion** - M is strongly typed
6. **Case sensitivity** - M is case-sensitive, DAX is not

### Validation Questions
Before accepting AI-generated code:
- Does it preserve query folding?
- Is the context transition correct?
- Are data types properly handled?
- Is the performance acceptable?
- Does it follow naming conventions?