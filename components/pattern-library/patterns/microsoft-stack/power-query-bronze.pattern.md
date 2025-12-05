# Pattern: Power Query Bronze Layer

## Metadata
- **ID**: pattern-microsoft-pq-bronze
- **Version**: 1.0.0
- **Category**: microsoft-stack
- **Difficulty Range**: 3-5 (Bronze layer data loading tasks)

## Triggers
Keywords that suggest this pattern applies:
- bronze layer
- raw data load
- initial data load
- source connection
- power query extract
- data ingestion
- medallion bronze

File types: .m, .pq

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_name | string | yes | Descriptive name of data source |
| source_type | enum | yes | Excel/CSV/SQL/API/SharePoint/Web |
| source_path | string | yes | Path, connection string, or URL |
| output_table | string | yes | Target table name (must start with Bronze_) |
| error_strategy | enum | no | log_continue/fail_fast (default: log_continue) |

## Pre-Conditions
- [ ] Source file/connection accessible
- [ ] Output table name follows naming convention (Bronze_*)
- [ ] No transformations applied (Bronze = faithful copy)
- [ ] Error handling strategy defined

## Template

```powerquery-m
// Query: {{output_table}}
// Purpose: Bronze layer - {{source_name}}
// Source: {{source_type}} at {{source_path}}
// Generated: {{timestamp}}

// SCHEMA INPUT
// Raw source columns (all preserved)

// SCHEMA OUTPUT
// All source columns PLUS:
// - _LoadTimestamp: datetime - when record was loaded
// - _SourceFile: text - source file/connection identifier

let
    // Step 1: Connect to source
    {{#if source_type == 'Excel'}}
    Source = Excel.Workbook(File.Contents("{{source_path}}"), null, true),
    SourceData = Source{[Item="{{sheet_name}}",Kind="Sheet"]}[Data],
    {{/if}}
    {{#if source_type == 'CSV'}}
    Source = Csv.Document(File.Contents("{{source_path}}"),[Delimiter=",", Columns=null, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    {{/if}}
    {{#if source_type == 'SQL'}}
    Source = Sql.Database("{{server}}", "{{database}}"),
    SourceData = Source{[Schema="{{schema}}",Item="{{table}}"]}[Data],
    {{/if}}
    {{#if source_type == 'API'}}
    Source = Json.Document(Web.Contents("{{source_path}}")),
    SourceData = Table.FromRecords(Source),
    {{/if}}

    // Step 2: Preserve original column names
    // NO transformations applied at Bronze layer
    OriginalColumns = Table.ColumnNames({{#if source_type == 'CSV'}}Source{{else}}SourceData{{/if}}),

    // Step 3: Add metadata columns
    AddedLoadTimestamp = Table.AddColumn(
        {{#if source_type == 'CSV'}}Source{{else}}SourceData{{/if}},
        "_LoadTimestamp",
        each DateTime.LocalNow(),
        type datetime
    ),

    AddedSourceFile = Table.AddColumn(
        AddedLoadTimestamp,
        "_SourceFile",
        each "{{source_path}}",
        type text
    ),

    // Step 4: Type preservation
    // All columns remain as-is from source (no type changes at Bronze)

    // Step 5: Error handling
    {{#if error_strategy == 'log_continue'}}
    // Errors logged but don't stop load
    WithErrorColumn = Table.AddColumn(
        AddedSourceFile,
        "_LoadError",
        each try "" otherwise "Error loading row",
        type text
    ),
    {{/if}}

    // Step 6: Final output
    Output = {{#if error_strategy == 'log_continue'}}WithErrorColumn{{else}}AddedSourceFile{{/if}}
in
    Output
```

## Post-Conditions
- [ ] All source columns preserved exactly as-is
- [ ] _LoadTimestamp column added (datetime type)
- [ ] _SourceFile column added (text type)
- [ ] NO data transformations applied (clean data = Silver layer)
- [ ] NO rows filtered (filtering = Silver layer)
- [ ] Query refreshes without error
- [ ] Column names match source exactly

## Anti-Patterns
**DON'T do this:**
- Apply type conversions at Bronze layer
- Filter or remove rows
- Rename columns (except metadata additions)
- Clean or transform data
- Handle errors silently without logging
- Promote headers if CSV (do that in Silver)
- Change data types from source defaults

**WHY**: Bronze layer is about **faithful data capture**. The goal is exact replication of source data plus metadata. All transformations, cleaning, filtering, and type changes belong in Silver layer. This keeps Bronze as a reliable "source of truth" that can be reprocessed if Silver logic changes.

## Examples

### Example 1: Excel Source
**Input:**
```
source_name: Sales Data Q4 2024
source_type: Excel
source_path: C:\Data\Sales_Q4_2024.xlsx
sheet_name: Sales
output_table: Bronze_SalesData
error_strategy: log_continue
```

**Output:**
```powerquery-m
// Query: Bronze_SalesData
// Purpose: Bronze layer - Sales Data Q4 2024
// Source: Excel at C:\Data\Sales_Q4_2024.xlsx
// Generated: 2025-12-05

// SCHEMA INPUT
// Raw Excel columns (all preserved)

// SCHEMA OUTPUT
// All source columns PLUS:
// - _LoadTimestamp: datetime - when record was loaded
// - _SourceFile: text - source file identifier

let
    // Step 1: Connect to source
    Source = Excel.Workbook(File.Contents("C:\Data\Sales_Q4_2024.xlsx"), null, true),
    SourceData = Source{[Item="Sales",Kind="Sheet"]}[Data],

    // Step 2: Preserve original column names
    OriginalColumns = Table.ColumnNames(SourceData),

    // Step 3: Add metadata columns
    AddedLoadTimestamp = Table.AddColumn(
        SourceData,
        "_LoadTimestamp",
        each DateTime.LocalNow(),
        type datetime
    ),

    AddedSourceFile = Table.AddColumn(
        AddedLoadTimestamp,
        "_SourceFile",
        each "C:\Data\Sales_Q4_2024.xlsx",
        type text
    ),

    // Step 4: Type preservation
    // All columns remain as-is from source

    // Step 5: Error handling
    WithErrorColumn = Table.AddColumn(
        AddedSourceFile,
        "_LoadError",
        each try "" otherwise "Error loading row",
        type text
    ),

    // Step 6: Final output
    Output = WithErrorColumn
in
    Output
```

### Example 2: SQL Database Source
**Input:**
```
source_name: Customer Master Data
source_type: SQL
source_path: server=sql-server-01;database=ProductionDB
server: sql-server-01
database: ProductionDB
schema: dbo
table: Customers
output_table: Bronze_Customers
error_strategy: fail_fast
```

**Output:**
```powerquery-m
// Query: Bronze_Customers
// Purpose: Bronze layer - Customer Master Data
// Source: SQL at server=sql-server-01;database=ProductionDB
// Generated: 2025-12-05

// SCHEMA INPUT
// Raw SQL table columns (all preserved)

// SCHEMA OUTPUT
// All source columns PLUS:
// - _LoadTimestamp: datetime - when record was loaded
// - _SourceFile: text - source connection identifier

let
    // Step 1: Connect to source
    Source = Sql.Database("sql-server-01", "ProductionDB"),
    SourceData = Source{[Schema="dbo",Item="Customers"]}[Data],

    // Step 2: Preserve original column names
    OriginalColumns = Table.ColumnNames(SourceData),

    // Step 3: Add metadata columns
    AddedLoadTimestamp = Table.AddColumn(
        SourceData,
        "_LoadTimestamp",
        each DateTime.LocalNow(),
        type datetime
    ),

    AddedSourceFile = Table.AddColumn(
        AddedLoadTimestamp,
        "_SourceFile",
        each "sql-server-01.ProductionDB.dbo.Customers",
        type text
    ),

    // Step 4: Type preservation
    // All columns remain as-is from source

    // Step 5: Final output (fail_fast = no error column)
    Output = AddedSourceFile
in
    Output
```

### Example 3: CSV Source
**Input:**
```
source_name: Vendor Invoice Data
source_type: CSV
source_path: C:\Imports\vendors_2024.csv
output_table: Bronze_VendorInvoices
error_strategy: log_continue
```

**Output:**
```powerquery-m
// Query: Bronze_VendorInvoices
// Purpose: Bronze layer - Vendor Invoice Data
// Source: CSV at C:\Imports\vendors_2024.csv
// Generated: 2025-12-05

// SCHEMA INPUT
// Raw CSV columns (all preserved, headers NOT promoted)

// SCHEMA OUTPUT
// All source columns PLUS:
// - _LoadTimestamp: datetime - when record was loaded
// - _SourceFile: text - source file identifier

let
    // Step 1: Connect to source
    Source = Csv.Document(
        File.Contents("C:\Imports\vendors_2024.csv"),
        [Delimiter=",", Columns=null, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),

    // Step 2: Preserve original column names
    // Note: Headers NOT promoted at Bronze - keep as Column1, Column2, etc.
    OriginalColumns = Table.ColumnNames(Source),

    // Step 3: Add metadata columns
    AddedLoadTimestamp = Table.AddColumn(
        Source,
        "_LoadTimestamp",
        each DateTime.LocalNow(),
        type datetime
    ),

    AddedSourceFile = Table.AddColumn(
        AddedLoadTimestamp,
        "_SourceFile",
        each "C:\Imports\vendors_2024.csv",
        type text
    ),

    // Step 4: Error handling
    WithErrorColumn = Table.AddColumn(
        AddedSourceFile,
        "_LoadError",
        each try "" otherwise "Error loading row",
        type text
    ),

    // Step 5: Final output
    Output = WithErrorColumn
in
    Output
```

## Usage Notes

### Bronze Layer Principles
1. **Faithful Copy**: Exact replica of source data
2. **Metadata Addition**: Add tracking columns (_Load*, _Source*)
3. **No Transformations**: Save ALL transformations for Silver
4. **Error Logging**: Capture load errors without stopping
5. **Idempotent**: Same source = same Bronze output

### Metadata Columns Standard
- `_LoadTimestamp`: When this record was loaded (datetime)
- `_SourceFile`: Source identifier for traceability (text)
- `_LoadError`: Error message if row had issues (text, optional)

### Source Type Notes
- **Excel**: Specify sheet name, workbook path
- **CSV**: Keep headers as first row (promote in Silver)
- **SQL**: Use schema.table notation
- **API**: Parse JSON to table, preserve structure
- **SharePoint**: Similar to Excel but with SharePoint.Contents()

### When to Use This Pattern
- Initial data ingestion from any source
- Creating data lake bronze layer
- Establishing source of truth
- Need for full data lineage
- Reprocessing capability required

## Related Patterns
- `power-query-silver.pattern.md` - Next step: clean and transform
- `dataflow-gen2.pattern.md` - For Fabric implementation
- `excel-read.pattern.md` - For Python-based Excel reading

## Testing Checklist
After implementing Bronze layer:
- [ ] Query refreshes successfully
- [ ] All source columns present
- [ ] Metadata columns added correctly
- [ ] No transformations applied
- [ ] Error handling works (test with bad data)
- [ ] _LoadTimestamp updates on refresh
- [ ] Source path/connection correct
