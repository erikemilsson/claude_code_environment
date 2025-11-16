# Data Architecture

## Overview
This project follows a **Bronze → Silver → Gold** data pipeline architecture for data quality and traceability.

## Architecture Layers

### Bronze Layer (Raw Data)
**Purpose**: Ingest raw data with minimal transformation

**Characteristics**:
- Load data exactly as it appears in source
- No business logic or calculations
- No filtering (except structural issues)
- Preserve original column names initially
- Focus: Data availability

**Typical Queries**:
- `Bronze_Source_*` - Initial data loads

**Example Transformations**:
```m
// ✅ Acceptable in Bronze
- Load from Excel.CurrentWorkbook()
- Basic type detection (let Power Query infer)
- Structural fixes (unpivot if source is pivoted)

// ❌ Avoid in Bronze  
- Filtering rows based on business rules
- Calculating derived columns
- Complex data type enforcement
- Data validation
```

### Silver Layer (Cleaned & Validated)
**Purpose**: Clean, standardize, and validate data

**Characteristics**:
- Explicit data type enforcement
- Standardized column names (snake_case)
- Null handling and data quality checks
- Remove duplicates
- Basic transformations (trim, lowercase, etc.)
- Data validation with explicit errors
- Focus: Data quality

**Typical Queries**:
- `Silver_Clean_*` - Data cleaning
- `Silver_Validate_*` - Validation steps

**Example Transformations**:
```m
// ✅ Appropriate for Silver
- Rename columns to standard names
- Enforce data types explicitly
- Validate required fields (error if null)
- Remove duplicates
- Standardize text (trim, lowercase)
- Filter out invalid rows with logging
- Add data quality flags

// ❌ Avoid in Silver
- Business calculations (CFF formulas, etc.)
- Aggregations
- Complex joins for reporting
```

### Gold Layer (Business Logic)
**Purpose**: Implement business logic and create reporting outputs

**Characteristics**:
- Business calculations and formulas
- Aggregations and summaries
- Complex joins and lookups
- Derived metrics
- Reporting-ready format
- Focus: Business value

**Typical Queries**:
- `Gold_Calculate_*` - Business calculations
- `Gold_Aggregate_*` - Summaries
- `Gold_Report_*` - Final outputs

**Example Transformations**:
```m
// ✅ Appropriate for Gold
- Implement regulatory formulas (CFF, etc.)
- Calculate KPIs and metrics
- Join multiple silver tables
- Create aggregations for reporting
- Format for specific output requirements
- Add compliance flags and indicators

// ❌ Avoid in Gold
- Reading directly from source (always use Silver)
- Data cleaning (should be done in Silver)
- Schema validation (should be in Silver)
```

## Query Dependencies

**Strict Dependency Rules**:
1. Bronze queries depend ONLY on data sources (Excel, SQL, etc.)
2. Silver queries depend ONLY on Bronze queries
3. Gold queries depend ONLY on Silver queries
4. No "skipping" layers (Gold cannot reference Bronze directly)

**Rationale**: 
- Each layer can be tested independently
- Changes isolated to relevant layer
- Clear separation of concerns
- Easy to debug data quality issues

## Example Pipeline

### Project: Battery Regulation CFF Calculation

```
BRONZE LAYER:
├── Bronze_Source_EmissionFactors
│   └── Loads: emission_factors sheet from Excel
│   └── Outputs: Raw emission factor data
│
├── Bronze_Source_InputTables  
│   └── Loads: input_tables sheet from Excel
│   └── Outputs: Raw material input data
│
└── Bronze_Source_MaterialMaster
    └── Loads: material_master sheet from Excel
    └── Outputs: Raw material reference data

⬇️

SILVER LAYER:
├── Silver_Clean_EmissionFactors
│   └── Depends on: Bronze_Source_EmissionFactors
│   └── Actions: Rename columns, enforce types, validate ranges
│   └── Outputs: Clean emission factor data
│
├── Silver_Validate_InputTables
│   └── Depends on: Bronze_Source_InputTables
│   └── Actions: Validate required fields, check data quality
│   └── Outputs: Validated material inputs
│
└── Silver_Clean_MaterialMaster
    └── Depends on: Bronze_Source_MaterialMaster
    └── Actions: Standardize names, remove duplicates
    └── Outputs: Clean material reference

⬇️

GOLD LAYER:
├── Gold_Calculate_EmissionFactorRouting
│   └── Depends on: Silver_Clean_EmissionFactors, Silver_Clean_MaterialMaster
│   └── Actions: Route correct emission factor per material type
│   └── Outputs: Material with assigned emission factors
│
├── Gold_Calculate_CFF
│   └── Depends on: Silver_Validate_InputTables, Gold_Calculate_EmissionFactorRouting
│   └── Actions: Implement CFF formula per delegated act
│   └── Outputs: Calculated carbon footprint values
│
└── Gold_Report_Compliance
    └── Depends on: Gold_Calculate_CFF
    └── Actions: Format for regulatory reporting
    └── Outputs: Final compliance report
```

## Layer Transition Checklist

### Bronze → Silver Transition
- [ ] Are column names standardized to snake_case?
- [ ] Are data types explicitly enforced?
- [ ] Are required fields validated (error on null)?
- [ ] Are duplicates handled?
- [ ] Is invalid data filtered with logging?
- [ ] Are text fields trimmed/cleaned?

### Silver → Gold Transition  
- [ ] Are business rules/formulas implemented?
- [ ] Are calculations traceable to source documents?
- [ ] Are multiple silver tables joined correctly?
- [ ] Are aggregations appropriate for reporting?
- [ ] Is output format meeting requirements?

## Anti-Patterns to Avoid

### ❌ Bronze Directly to Gold
```m
// ❌ BAD - Skips validation layer
Gold_Calculate_CFF = 
    let
        Source = Bronze_Source_InputTables,  // Missing Silver validation!
        Calculation = ...
    in
        Result
```

### ❌ Business Logic in Bronze
```m
// ❌ BAD - Calculations should be in Gold
Bronze_Source_EmissionFactors = 
    let
        Source = Excel.CurrentWorkbook(){[Name="EmissionFactors"]}[Content],
        WithCalculation = Table.AddColumn(Source, "adjusted_ef", each [ef] * 1.2)  // No!
    in
        WithCalculation
```

### ❌ Data Cleaning in Gold
```m
// ❌ BAD - Cleaning should be in Silver  
Gold_Calculate_CFF = 
    let
        Source = Silver_Validate_InputTables,
        Cleaned = Table.TransformColumns(Source, {"text_field", Text.Trim})  // Too late!
    in
        ...
```

## Naming Alignment

Query names must match architecture layer:

**Bronze queries**:
- Prefix: `Bronze_`
- Action: `Source_`
- Example: `Bronze_Source_EmissionFactors`

**Silver queries**:
- Prefix: `Silver_`  
- Action: `Clean_`, `Validate_`, `Transform_`
- Example: `Silver_Clean_EmissionFactors`, `Silver_Validate_InputTables`

**Gold queries**:
- Prefix: `Gold_`
- Action: `Calculate_`, `Aggregate_`, `Report_`
- Example: `Gold_Calculate_CFF`, `Gold_Report_Compliance`

## Benefits of This Architecture

1. **Testability**: Each layer can be validated independently
2. **Debuggability**: Easy to isolate where issues occur
3. **Reusability**: Silver tables can feed multiple Gold calculations
4. **Performance**: Can optimize/buffer at layer boundaries
5. **Clarity**: Clear separation of data quality vs business logic
6. **Auditability**: Data lineage is explicit

## Template Instructions

**When starting a new project**:

1. Identify all data sources → Create Bronze queries
2. Define data quality requirements → Create Silver queries
3. Map business logic requirements → Create Gold queries
4. Document in `.claude/reference/dependency-graph.md`
5. Validate no layer-skipping in implementation

**Replace this section** with your project-specific architecture details once Phase 0 is complete.
