# Data Analytics Template

## Overview

Template for **Microsoft Fabric, Power BI, DAX, and semantic modeling** projects with ATEF integration.

## When to Use This Template

Use data-analytics template when project spec mentions:
- Microsoft Fabric lakehouse/warehouse
- Power BI semantic models with DAX measures
- Medallion architecture (Bronze/Silver/Gold layers)
- Dimensional modeling (star/snowflake schema)
- Dataflow Gen2 pipelines

**Don't use** for pure ETL without semantic layer (use power-query template instead).

## Template Structure

```
templates/data-analytics/
├── README.md (this file)
├── components.json (template configuration)
└── customizations/
    ├── context/ (4 files - project context)
    ├── reference/ (3 files - technical reference)
    └── commands/ (3 files - template-specific commands)
```

## Included Components

### Required (ATEF Core)
- Task Management (with ATEF schema)
- Validation Gates (pre/post-execution)
- Pattern Library (Microsoft stack patterns)
- Checkpoint System (state snapshots)

### Optional
- Error Catalog (learn from Microsoft stack errors)

### Included Patterns
- `power-query-bronze.pattern.md` - Raw data loading
- `power-query-silver.pattern.md` - Data cleaning/standardization
- `dax-measure.pattern.md` - DAX calculations with VAR pattern
- `dataflow-gen2.pattern.md` - Multi-layer pipeline configuration

## Customizations

### Context Files
1. **medallion-architecture.md** - Bronze/Silver/Gold layer principles
2. **naming-conventions.md** - Table/column/measure naming standards
3. **llm-pitfalls-microsoft.md** - Common DAX and Power Query mistakes
4. **critical_rules.md** - ATEF-specific validation rules

### Reference Files
1. **dax-patterns.md** - Common DAX calculation patterns (time intelligence, aggregations, etc.)
2. **pq-patterns.md** - Power Query transformation patterns (type conversion, pivoting, etc.)
3. **fabric-best-practices.md** - Lakehouse, dataflow, and deployment best practices

### Commands
1. **validate-dax.md** - Validate DAX measure syntax and filter context
2. **validate-pq.md** - Validate Power Query M code syntax
3. **deploy-model.md** - Deploy semantic model to Fabric workspace

## Detection Rules

Template auto-selected when specification contains:

**High confidence** (score ≥3):
- "Microsoft Fabric"
- "Power BI + semantic model"
- "DAX measures"
- "medallion architecture"
- "bronze/silver/gold layer"

**Medium confidence** (score 2):
- "Power Query + data transformation"
- "semantic layer"
- "dimensional modeling"
- "star schema"

**File extensions**:
- `.dax`, `.pq`, `.m`, `.pbix`, `.bim`

## Technology Focus

### Primary
- Microsoft Fabric (lakehouses, warehouses)
- Power BI (reports, dashboards)
- DAX (measure calculations)
- Power Query / M language (data transformations)
- Semantic modeling (star schema, relationships)

### Secondary
- Azure Data Lake / OneLake
- Dataflow Gen2
- Notebooks (PySpark, SQL)

## Typical Project Structure

```
project/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── commands/
│   │   ├── complete-task.md
│   │   ├── validate-dax.md (template-specific)
│   │   ├── validate-pq.md (template-specific)
│   │   └── deploy-model.md (template-specific)
│   ├── context/
│   │   ├── overview.md
│   │   ├── medallion-architecture.md (template-specific)
│   │   ├── naming-conventions.md (template-specific)
│   │   ├── llm-pitfalls-microsoft.md (template-specific)
│   │   └── critical_rules.md (template-specific)
│   ├── reference/
│   │   ├── dax-patterns.md (template-specific)
│   │   ├── pq-patterns.md (template-specific)
│   │   └── fabric-best-practices.md (template-specific)
│   └── tasks/
├── queries/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── measures/
├── models/
├── dataflows/
└── notebooks/
```

## Common Errors Prevented

The template includes error catalog entries for:
- **ERR-PQ-001**: Type conversion at Bronze layer (violates medallion architecture)
- **ERR-PQ-002**: Silver query sources directly from file (should reference Bronze)
- **ERR-DAX-001**: Missing VAR pattern (performance and debugging issues)
- **ERR-DAX-002**: Measure in row context (context confusion)

## Key Patterns

### Power Query
- **Bronze layer**: Load raw data with `_LoadTimestamp` and `_SourceFile` metadata
- **Silver layer**: Clean, standardize, convert types, validate data
- **Gold layer**: Apply business logic, aggregations, KPIs
- **Dataflow Gen2**: Configure multi-layer pipelines with lakehouse destinations

### DAX
- **VAR pattern**: Store intermediate calculations for performance/debugging
- **CALCULATE**: Modify filter context for calculations
- **Time intelligence**: YTD, MTD, QTD, PY comparisons
- **Measure groups**: Organize related calculations

### Semantic Modeling
- **Star schema**: Fact tables + dimension tables
- **Relationships**: 1:* from dimension to fact
- **Row-level security**: Filter data by user
- **Calculation groups**: Reusable calculation patterns

## Integration

### Recommended Tools
- **Tabular Editor**: Semantic model development
- **DAX Studio**: Measure testing and optimization
- **Power Query SDK**: M language development
- **Azure Data Studio**: SQL/PySpark notebooks

### Deployment Targets
- Microsoft Fabric workspace
- Power BI Service
- Azure Synapse Analytics

## Bootstrap Process

When using `smart-bootstrap.md`, this template is automatically selected when the specification matches detection rules.

Manual bootstrap with this template:
```
/bootstrap
Select template: data-analytics
```

The bootstrap process will:
1. Copy all ATEF components (validation gates, patterns, checkpoints, error catalog)
2. Copy Microsoft stack patterns (power-query-*, dax-*, dataflow-*)
3. Copy customizations (context, reference, commands)
4. Populate files with content from specification
5. Create initial task breakdown

## Example Specifications

### High Confidence Match
```
Project: Build customer analytics semantic model in Microsoft Fabric

Requirements:
- Ingest customer data into bronze layer (raw)
- Transform to silver layer (cleaned, standardized)
- Create gold layer with aggregated KPIs
- Build star schema semantic model with dimensions and facts
- Implement DAX measures for customer lifetime value, churn rate
- Deploy to Fabric workspace

Technologies: Microsoft Fabric, Power BI, DAX, Power Query
```

### Medium Confidence Match
```
Project: Sales reporting with dimensional model

Requirements:
- Design star schema with sales facts and product/customer/time dimensions
- Build Power Query transformations for data cleaning
- Create calculated measures for revenue, profit margin, growth
- Power BI dashboard development

Technologies: Power BI, Power Query
```

## Notes

This template is part of the ATEF (Air-Tight Execution Framework) system and includes:
- Validation gates for pre/post-execution checks
- Pattern library for reusable Microsoft stack solutions
- Checkpoint system for safe experimentation and rollback
- Error catalog for learning from past mistakes

All ATEF features are designed to reduce LLM errors specifically for Microsoft Fabric, Power BI, DAX, and Power Query development.

## See Also

- **components.json**: Full template configuration
- **Pattern Library**: `components/pattern-library/patterns/microsoft-stack/`
- **Error Catalog**: `components/error-catalog/catalog/common-errors.json`
- **ATEF Documentation**: See main repository README.md
