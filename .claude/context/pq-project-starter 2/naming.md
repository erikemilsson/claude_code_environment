# Naming Standards

## Purpose
Enforces consistent naming conventions across all Power Query queries and variables.

## Query Naming Convention

**Pattern**: `[Stage]_[Action]_[Entity]`

### Stage Prefix (Required)
- `Bronze_` - Raw data ingestion, minimal transformation
- `Silver_` - Cleaned, validated, standardized data
- `Gold_` - Business logic, aggregations, final outputs

### Action (Required)
- `Source_` - Initial data load from source
- `Clean_` - Data cleaning operations
- `Validate_` - Data validation checks
- `Transform_` - Data transformations
- `Calculate_` - Calculations and derived values
- `Aggregate_` - Aggregations and summaries
- `Report_` - Final reporting outputs

### Entity (Required)
- Descriptive noun or noun phrase in PascalCase
- Examples: `EmissionFactors`, `InputTables`, `CFF`, `ComplianceReport`

### Examples
```
✅ Bronze_Source_EmissionFactors
✅ Silver_Clean_InputTables
✅ Silver_Validate_InputTables
✅ Gold_Calculate_CFF
✅ Gold_Report_Compliance

❌ emission_factors (no stage, no action)
❌ Bronze_EmissionFactors (no action)
❌ GetEmissionFactors (no stage prefix)
❌ bronze_source_emission_factors (wrong case)
```

## Variable Naming

### In M Code
**Use PascalCase for all variables**:
```m
// ✅ Correct
RecycledContentShare = 0.25
MaterialMassKg = 1000
EmissionFactorPrimary = 5.2

// ❌ Incorrect
recycled_content_share = 0.25
materialMass = 1000
ef_primary = 5.2
```

### Column Names
**Use snake_case for data columns**:
```m
// ✅ Correct
#"Renamed Columns" = Table.RenameColumns(
    Source,
    {
        {"Old Name", "recycled_content_share"},
        {"Another", "material_mass_kg"}
    }
)

// ❌ Incorrect - mixing cases
{{"Old", "RecycledContentShare"}, {"Another", "material_mass_kg"}}
```

## Units in Names

**Always include units in variable names when applicable**:

```m
// ✅ Explicit units
MaterialMassKg = 1000
MaterialMassTonnes = 1.0
DistanceKm = 50
TimeSeconds = 3600
TemperatureCelsius = 25

// ❌ Ambiguous
MaterialMass = 1000  // Kg? Tonnes? Pounds?
Distance = 50        // Km? Miles? Meters?
```

## Type Suffixes

**Use suffixes for clarity when type isn't obvious**:

```m
// ✅ Clear intent
CompanyNameList = {"Company_001", "Company_002"}
EmissionFactorTable = Table.FromRecords({...})
IsValidFlag = true
ErrorCount = 0

// Consider adding suffixes when:
// - Multiple variables of different types represent same concept
// - Code reviewer might misinterpret the type
```

## Constants

**Use SCREAMING_SNAKE_CASE for constants**:

```m
// ✅ Constants
MAX_EMISSION_THRESHOLD = 100
DEFAULT_RECYCLED_CONTENT = 0.0
VALIDATION_ERROR_MESSAGE = "Invalid data detected"

// Regular variables
CurrentEmission = 75
RecycledContent = 0.25
```

## Function Names

**Use descriptive verb + noun in PascalCase**:

```m
// ✅ Clear function names
CalculateEmissionFactor = (mass, factor) => mass * factor
ValidateInputRange = (value, min, max) => value >= min and value <= max
FormatComplianceReport = (data) => Table.TransformColumns(...)

// ❌ Unclear
Process = (x) => x * 2
DoIt = (data) => ...
Func1 = (a, b) => a + b
```

## Comments

**Always add unit comments for calculations**:

```m
// ✅ Good comments
MaterialMassKg = 1000,  // Value in kg, source: input table
MaterialMassTonnes = MaterialMassKg / 1000,  // Converted to tonnes for reporting

// ✅ Formula source comments
RecycledContentShare = PostConsumerScrap / TotalMaterial,  // Formula from Art. 7(2)

// ✅ Transformation explanation
#"Filtered Valid Rows" = Table.SelectRows(
    Source,
    each [emission_factor] <> null  // Remove rows without emission factors
)
```

## Forbidden Patterns

**Never use**:
- `x`, `y`, `temp`, `data` as variable names (too vague)
- Mixed naming conventions in same query
- Abbreviations without glossary definition (use glossary.md)
- Single-letter variables except in very short lambda expressions

**Exception for lambda expressions**:
```m
// ✅ Acceptable in short, obvious context
List.Transform({1, 2, 3}, each _ * 2)
Table.TransformColumns(Source, {"amount", each _ * 1.5})

// ❌ Not acceptable in complex logic
Calculate = (x, y, z) => 
    let
        a = x * y,
        b = a / z,
        c = if b > 10 then a else b
    in c
```

## Checklist

Before committing any query:
- [ ] Query name follows [Stage]_[Action]_[Entity] pattern
- [ ] Variables use PascalCase
- [ ] Column names use snake_case
- [ ] Units included in variable names where applicable
- [ ] Constants use SCREAMING_SNAKE_CASE
- [ ] Function names are descriptive verb + noun
- [ ] All calculations have unit/source comments
- [ ] No vague variable names (x, temp, data)
- [ ] Naming matches glossary.md definitions
