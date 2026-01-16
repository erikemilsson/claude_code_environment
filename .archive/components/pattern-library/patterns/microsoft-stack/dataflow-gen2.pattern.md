# Pattern: Dataflow Gen2

## Metadata
- **ID**: pattern-microsoft-dataflow-gen2
- **Version**: 1.0.0
- **Category**: microsoft-stack
- **Difficulty Range**: 5-7 (Fabric Dataflow Gen2 creation tasks)

## Triggers
Keywords that suggest this pattern applies:
- dataflow gen2
- fabric dataflow
- lakehouse dataflow
- power query dataflow
- fabric pipeline
- data orchestration
- lakehouse ingestion

File types: .json (dataflow definition), .m (Power Query)

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| dataflow_name | string | yes | Name of the dataflow |
| description | string | yes | Purpose of the dataflow |
| source_type | enum | yes | Source type (SQL/API/File/Lakehouse) |
| destination_lakehouse | string | yes | Target lakehouse name |
| destination_table | string | yes | Target table in lakehouse |
| load_mode | enum | no | Append/Replace (default: Replace) |
| partition_column | string | no | Column for partitioning (optional) |

## Pre-Conditions
- [ ] Microsoft Fabric workspace exists
- [ ] Source connection configured in workspace
- [ ] Destination lakehouse created
- [ ] Appropriate permissions for lakehouse write
- [ ] Source schema documented
- [ ] Transformation logic defined

## Template

### Dataflow Configuration (Conceptual)
```
Dataflow Gen2: {{dataflow_name}}
├── Source Configuration
│   ├── Connection: {{source_type}}
│   ├── Authentication: (configured in workspace)
│   └── Query: {{source_query_name}}
├── Transformation Queries
│   ├── Bronze Layer: {{bronze_query}}
│   ├── Silver Layer: {{silver_query}}
│   └── [Optional] Gold Layer: {{gold_query}}
└── Destination Configuration
    ├── Lakehouse: {{destination_lakehouse}}
    ├── Table: {{destination_table}}
    ├── Load Mode: {{load_mode}}
    └── Partition: {{partition_column}}
```

### Power Query for Dataflow Gen2
```powerquery-m
// Dataflow: {{dataflow_name}}
// Description: {{description}}
// Source: {{source_type}}
// Destination: {{destination_lakehouse}}.{{destination_table}}
// Load Mode: {{load_mode}}
// Created: {{timestamp}}

// ============================================
// BRONZE LAYER: Raw Data Extraction
// ============================================

let
    Bronze_{{table_name}} =
    let
        // Step 1: Connect to source
        {{source_connection_code}},

        // Step 2: Add metadata
        AddedMetadata = Table.AddColumn(
            Source,
            "_LoadTimestamp",
            each DateTime.LocalNow(),
            type datetime
        ),

        AddedSourceInfo = Table.AddColumn(
            AddedMetadata,
            "_SourceSystem",
            each "{{source_type}}",
            type text
        ),

        // Step 3: Output
        Output = AddedSourceInfo
    in
        Output
in
    Bronze_{{table_name}},

// ============================================
// SILVER LAYER: Cleaned and Standardized
// ============================================

let
    Silver_{{table_name}} =
    let
        // Step 1: Load from Bronze
        Source = Bronze_{{table_name}},

        // Step 2: Remove Bronze metadata
        RemovedBronzeMetadata = Table.RemoveColumns(
            Source,
            {"_LoadTimestamp", "_SourceSystem"}
        ),

        // Step 3: Standardize column names
        RenamedColumns = Table.RenameColumns(
            RemovedBronzeMetadata,
            {
                {{column_rename_list}}
            }
        ),

        // Step 4: Type conversions
        ChangedTypes = Table.TransformColumnTypes(
            RenamedColumns,
            {
                {{type_conversion_list}}
            }
        ),

        // Step 5: Data quality
        {{data_quality_steps}},

        // Step 6: Add Silver metadata
        AddedValidatedAt = Table.AddColumn(
            {{last_quality_step}},
            "_ValidatedAt",
            each DateTime.LocalNow(),
            type datetime
        ),

        // Step 7: Output
        Output = AddedValidatedAt
    in
        Output
in
    Silver_{{table_name}}

// ============================================
// DESTINATION CONFIGURATION
// ============================================
// This query will be configured to write to:
// Lakehouse: {{destination_lakehouse}}
// Table: {{destination_table}}
// Mode: {{load_mode}}
{{#if partition_column}}
// Partitioned by: {{partition_column}}
{{/if}}
```

## Post-Conditions
- [ ] Dataflow Gen2 created in Fabric workspace
- [ ] Source connection successful
- [ ] Transformations execute without error
- [ ] Data loads to lakehouse table
- [ ] Partitioning configured (if applicable)
- [ ] Refresh schedule set (if needed)
- [ ] Data quality validated
- [ ] Monitoring configured

## Anti-Patterns
**DON'T do this:**
- Connect directly to destination in Power Query (use Dataflow destination settings)
- Apply complex business logic in Dataflow (save for semantic model)
- Load to multiple lakehouses in one dataflow (use multiple dataflows)
- Skip Bronze layer (always preserve raw data)
- Hardcode credentials (use workspace connections)
- Ignore partition strategy for large tables
- Create too many queries in one dataflow (>10 = split)
- Skip error handling

**WHY**:
- Dataflow destination settings are optimized for Fabric
- Business logic belongs in semantic models (DAX)
- Multiple destinations increase failure points
- Bronze layer enables reprocessing
- Hardcoded credentials are security risk
- Large tables need partitioning for performance
- Complex dataflows are hard to debug
- Errors should be logged and handled

## Examples

### Example 1: SQL to Lakehouse
**Input:**
```
dataflow_name: Sales Data Ingestion
description: Ingest daily sales from SQL Server to lakehouse
source_type: SQL
destination_lakehouse: SalesLakehouse
destination_table: Sales
load_mode: Append
partition_column: sale_date
```

**Output:**
```powerquery-m
// Dataflow: Sales Data Ingestion
// Description: Ingest daily sales from SQL Server to lakehouse
// Source: SQL Server
// Destination: SalesLakehouse.Sales
// Load Mode: Append
// Created: 2025-12-05

// ============================================
// BRONZE LAYER: Raw Data Extraction
// ============================================

let
    Bronze_Sales =
    let
        // Step 1: Connect to SQL Server
        Source = Sql.Database("sql-server-prod", "SalesDB"),
        SourceTable = Source{[Schema="dbo",Item="Sales"]}[Data],

        // Step 2: Filter for today's data (incremental load)
        FilteredRows = Table.SelectRows(
            SourceTable,
            each [SaleDate] = Date.From(DateTime.LocalNow())
        ),

        // Step 3: Add metadata
        AddedMetadata = Table.AddColumn(
            FilteredRows,
            "_LoadTimestamp",
            each DateTime.LocalNow(),
            type datetime
        ),

        AddedSourceInfo = Table.AddColumn(
            AddedMetadata,
            "_SourceSystem",
            each "SQL Server - SalesDB",
            type text
        ),

        // Step 4: Output
        Output = AddedSourceInfo
    in
        Output
in
    Bronze_Sales,

// ============================================
// SILVER LAYER: Cleaned and Standardized
// ============================================

let
    Silver_Sales =
    let
        // Step 1: Load from Bronze
        Source = Bronze_Sales,

        // Step 2: Remove Bronze metadata
        RemovedBronzeMetadata = Table.RemoveColumns(
            Source,
            {"_LoadTimestamp", "_SourceSystem"}
        ),

        // Step 3: Standardize column names (snake_case)
        RenamedColumns = Table.RenameColumns(
            RemovedBronzeMetadata,
            {
                {"SaleID", "sale_id"},
                {"SaleDate", "sale_date"},
                {"CustomerID", "customer_id"},
                {"ProductID", "product_id"},
                {"Quantity", "quantity"},
                {"UnitPrice", "unit_price"},
                {"TotalAmount", "total_amount"}
            }
        ),

        // Step 4: Type conversions
        ChangedTypes = Table.TransformColumnTypes(
            RenamedColumns,
            {
                {"sale_id", type text},
                {"sale_date", type date},
                {"customer_id", type text},
                {"product_id", type text},
                {"quantity", Int64.Type},
                {"unit_price", type number},
                {"total_amount", type number}
            }
        ),

        // Step 5: Data quality - remove nulls
        RemovedNulls = Table.SelectRows(
            ChangedTypes,
            each [sale_id] <> null and [sale_date] <> null
        ),

        // Step 6: Add calculated columns
        AddedRevenue = Table.AddColumn(
            RemovedNulls,
            "revenue",
            each [quantity] * [unit_price],
            type number
        ),

        // Step 7: Add Silver metadata
        AddedValidatedAt = Table.AddColumn(
            AddedRevenue,
            "_ValidatedAt",
            each DateTime.LocalNow(),
            type datetime
        ),

        // Step 8: Output
        Output = AddedValidatedAt
    in
        Output
in
    Silver_Sales

// ============================================
// DESTINATION CONFIGURATION
// ============================================
// Configure in Dataflow Gen2 UI:
// - Data destination: Lakehouse
// - Lakehouse: SalesLakehouse
// - Table: Sales
// - Update method: Append
// - Partition column: sale_date (recommended for time-series data)
```

### Example 2: API to Lakehouse
**Input:**
```
dataflow_name: Customer API Sync
description: Sync customer data from REST API to lakehouse
source_type: API
destination_lakehouse: CustomerLakehouse
destination_table: Customers
load_mode: Replace
```

**Output:**
```powerquery-m
// Dataflow: Customer API Sync
// Description: Sync customer data from REST API to lakehouse
// Source: REST API
// Destination: CustomerLakehouse.Customers
// Load Mode: Replace
// Created: 2025-12-05

// ============================================
// BRONZE LAYER: Raw API Data
// ============================================

let
    Bronze_Customers =
    let
        // Step 1: Call API
        Source = Json.Document(
            Web.Contents(
                "https://api.company.com/customers",
                [
                    Headers=[
                        #"Content-Type"="application/json"
                    ],
                    Timeout=#duration(0, 0, 5, 0)  // 5 minute timeout
                ]
            )
        ),

        // Step 2: Convert JSON to table
        ConvertedToTable = Table.FromRecords(Source),

        // Step 3: Add metadata
        AddedMetadata = Table.AddColumn(
            ConvertedToTable,
            "_LoadTimestamp",
            each DateTime.LocalNow(),
            type datetime
        ),

        AddedSourceInfo = Table.AddColumn(
            AddedMetadata,
            "_SourceSystem",
            each "Customer API",
            type text
        ),

        // Step 4: Output
        Output = AddedSourceInfo
    in
        Output
in
    Bronze_Customers,

// ============================================
// SILVER LAYER: Validated Customers
// ============================================

let
    Silver_Customers =
    let
        // Step 1: Load from Bronze
        Source = Bronze_Customers,

        // Step 2: Remove Bronze metadata
        RemovedBronzeMetadata = Table.RemoveColumns(
            Source,
            {"_LoadTimestamp", "_SourceSystem"}
        ),

        // Step 3: Standardize column names
        RenamedColumns = Table.RenameColumns(
            RemovedBronzeMetadata,
            {
                {"id", "customer_id"},
                {"firstName", "first_name"},
                {"lastName", "last_name"},
                {"email", "email"},
                {"phone", "phone"},
                {"createdAt", "created_at"}
            }
        ),

        // Step 4: Type conversions
        ChangedTypes = Table.TransformColumnTypes(
            RenamedColumns,
            {
                {"customer_id", type text},
                {"first_name", type text},
                {"last_name", type text},
                {"email", type text},
                {"phone", type text},
                {"created_at", type datetime}
            }
        ),

        // Step 5: Validate email format
        FilteredValidEmail = Table.SelectRows(
            ChangedTypes,
            each Text.Contains([email], "@") and Text.Contains([email], ".")
        ),

        // Step 6: Clean phone numbers
        CleanedPhone = Table.TransformColumns(
            FilteredValidEmail,
            {
                {"phone", each Text.Select(_, {"0".."9"}), type text}
            }
        ),

        // Step 7: Add Silver metadata
        AddedValidatedAt = Table.AddColumn(
            CleanedPhone,
            "_ValidatedAt",
            each DateTime.LocalNow(),
            type datetime
        ),

        // Step 8: Output
        Output = AddedValidatedAt
    in
        Output
in
    Silver_Customers

// ============================================
// DESTINATION CONFIGURATION
// ============================================
// Configure in Dataflow Gen2 UI:
// - Data destination: Lakehouse
// - Lakehouse: CustomerLakehouse
// - Table: Customers
// - Update method: Replace (full refresh)
```

## Usage Notes

### Dataflow Gen2 vs Dataflow Gen1
**Gen2 Advantages:**
- **Lakehouse integration**: Direct write to lakehouse tables
- **Better performance**: Optimized for large-scale data
- **Partitioning support**: For better query performance
- **Fabric-native**: Integrated with Fabric workspace
- **Delta tables**: Leverages Delta Lake format

### Load Mode Selection
**Replace:**
- Full refresh of data
- Good for dimension tables
- Ensures data consistency
- Use when source is manageable size

**Append:**
- Incremental load
- Good for fact tables
- Requires deduplication logic
- Use for time-series data

### Partitioning Strategy
Partition by:
- **Date columns**: Most common (year, month, day)
- **Category**: For categorical data
- **Region**: For geographic data
- **Hash**: For even distribution

### Refresh Schedule
Configure in Dataflow settings:
- **Hourly**: For real-time requirements
- **Daily**: Most common pattern
- **Weekly**: For slower-changing data
- **Manual**: For ad-hoc loads

## Best Practices

### 1. Modular Design
- One dataflow per source system
- Separate Bronze/Silver/Gold layers
- Reusable queries across dataflows

### 2. Error Handling
```powerquery-m
ErrorHandledStep = try
    [transformation]
otherwise
    [fallback_value]
```

### 3. Performance Optimization
- Filter at source (SQL WHERE clause)
- Use query folding where possible
- Partition large tables
- Schedule during off-peak hours

### 4. Monitoring
- Enable refresh notifications
- Set up alerts for failures
- Monitor refresh duration
- Track data quality metrics

## Related Patterns
- `power-query-bronze.pattern.md` - Bronze layer logic
- `power-query-silver.pattern.md` - Silver layer transformations
- `dax-measure.pattern.md` - Semantic model on lakehouse tables

## Testing Checklist
After creating Dataflow Gen2:
- [ ] Test connection to source
- [ ] Verify transformations work
- [ ] Test refresh manually
- [ ] Check data in lakehouse table
- [ ] Verify partitioning (if used)
- [ ] Test incremental load (if Append mode)
- [ ] Set up refresh schedule
- [ ] Configure monitoring
- [ ] Document dependencies
- [ ] Test failure scenarios
