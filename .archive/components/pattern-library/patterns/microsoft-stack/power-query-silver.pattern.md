# Pattern: Power Query Silver Layer

## Metadata
- **ID**: pattern-microsoft-pq-silver
- **Version**: 1.0.0
- **Category**: microsoft-stack
- **Difficulty Range**: 4-6 (Silver layer transformation tasks)

## Triggers
Keywords that suggest this pattern applies:
- silver layer
- clean data
- transform data
- data quality
- data validation
- medallion silver
- curated data

File types: .m, .pq

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| bronze_source | string | yes | Name of Bronze layer query to source from |
| output_table | string | yes | Target table name (must start with Silver_) |
| transformations | string | yes | List of transformations to apply |
| data_quality_checks | boolean | no | Include validation steps (default: true) |
| deduplication | boolean | no | Remove duplicates (default: false) |
| dedup_columns | string | conditional | Columns for deduplication (required if deduplication=true) |

## Pre-Conditions
- [ ] Bronze layer query exists and is functional
- [ ] Output table name follows naming convention (Silver_*)
- [ ] Transformation logic is well-defined
- [ ] Data quality rules documented
- [ ] Column names follow snake_case convention

## Template

```powerquery-m
// Query: {{output_table}}
// Purpose: Silver layer - Clean and transform {{bronze_source}}
// Source: Bronze layer query {{bronze_source}}
// Generated: {{timestamp}}

// SCHEMA INPUT
// From Bronze layer (see {{bronze_source}})

// SCHEMA OUTPUT
// Transformed columns:
// {{transformed_columns_list}}

let
    // Step 1: Load from Bronze layer
    Source = {{bronze_source}},

    // Step 2: Remove metadata columns (Bronze-specific)
    RemovedMetadata = Table.RemoveColumns(
        Source,
        {"_LoadTimestamp", "_SourceFile", "_LoadError"}
    ),

    // Step 3: Promote headers (if CSV from Bronze)
    {{#if promote_headers}}
    PromotedHeaders = Table.PromoteHeaders(RemovedMetadata, [PromoteAllScalars=true]),
    {{/if}}

    // Step 4: Rename columns to snake_case
    RenamedColumns = Table.RenameColumns(
        {{#if promote_headers}}PromotedHeaders{{else}}RemovedMetadata{{/if}},
        {
            {{column_renames}}
        }
    ),

    // Step 5: Type conversions
    ChangedTypes = Table.TransformColumnTypes(
        RenamedColumns,
        {
            {{type_conversions}}
        }
    ),

    // Step 6: Data cleaning
    {{#if data_quality_checks}}
    // Remove rows with null in critical columns
    RemovedNulls = Table.SelectRows(
        ChangedTypes,
        each {{null_check_conditions}}
    ),

    // Trim text columns
    TrimmedText = Table.TransformColumns(
        RemovedNulls,
        {
            {{trim_operations}}
        }
    ),
    {{/if}}

    // Step 7: Apply business transformations
    {{transformations_code}}

    {{#if deduplication}}
    // Step 8: Remove duplicates
    RemovedDuplicates = Table.Distinct(
        {{last_transformation_step}},
        {{{dedup_columns}}}
    ),
    {{/if}}

    // Step 9: Add Silver metadata
    AddedValidationTimestamp = Table.AddColumn(
        {{#if deduplication}}RemovedDuplicates{{else}}{{last_transformation_step}}{{/if}},
        "_ValidatedAt",
        each DateTime.LocalNow(),
        type datetime
    ),

    // Step 10: Final output
    Output = AddedValidationTimestamp
in
    Output
```

## Post-Conditions
- [ ] All columns follow naming conventions (snake_case)
- [ ] Data types correctly assigned
- [ ] Null values handled appropriately
- [ ] Business rules applied correctly
- [ ] Duplicates removed (if specified)
- [ ] Data quality validated
- [ ] Query refreshes without error
- [ ] _ValidatedAt timestamp added

## Anti-Patterns
**DON'T do this:**
- Connect directly to source (always use Bronze layer)
- Apply transformations without Bronze layer
- Keep original column names without standardizing
- Skip type conversions (rely on Bronze types)
- Remove rows without documenting logic
- Apply complex business logic (that's Gold layer)
- Forget error handling in try...otherwise
- Hardcode values (use parameters)

**WHY**: Silver layer is about **clean, standardized data**. It should always source from Bronze (for lineage), apply consistent naming/typing, and handle data quality. Complex business logic and aggregations belong in Gold layer. This separation allows reprocessing and debugging.

## Examples

### Example 1: Clean Sales Data
**Input:**
```
bronze_source: Bronze_SalesData
output_table: Silver_SalesData
transformations: |
  - Standardize date format
  - Convert amounts to decimal
  - Clean product names
  - Add calculated revenue column
data_quality_checks: true
deduplication: true
dedup_columns: transaction_id
```

**Output:**
```powerquery-m
// Query: Silver_SalesData
// Purpose: Silver layer - Clean and transform Bronze_SalesData
// Source: Bronze layer query Bronze_SalesData
// Generated: 2025-12-05

// SCHEMA INPUT
// From Bronze layer (see Bronze_SalesData)

// SCHEMA OUTPUT
// Transformed columns:
// - transaction_id: text - unique transaction identifier
// - transaction_date: date - sale date
// - product_name: text - cleaned product name
// - quantity: number - units sold
// - unit_price: number - price per unit (decimal)
// - revenue: number - calculated (quantity * unit_price)
// - _ValidatedAt: datetime - validation timestamp

let
    // Step 1: Load from Bronze layer
    Source = Bronze_SalesData,

    // Step 2: Remove Bronze metadata columns
    RemovedMetadata = Table.RemoveColumns(
        Source,
        {"_LoadTimestamp", "_SourceFile", "_LoadError"}
    ),

    // Step 3: Rename columns to snake_case
    RenamedColumns = Table.RenameColumns(
        RemovedMetadata,
        {
            {"Transaction ID", "transaction_id"},
            {"Date", "transaction_date"},
            {"Product", "product_name"},
            {"Qty", "quantity"},
            {"Price", "unit_price"}
        }
    ),

    // Step 4: Type conversions
    ChangedTypes = Table.TransformColumnTypes(
        RenamedColumns,
        {
            {"transaction_id", type text},
            {"transaction_date", type date},
            {"product_name", type text},
            {"quantity", Int64.Type},
            {"unit_price", type number}
        }
    ),

    // Step 5: Data cleaning
    // Remove rows with null in critical columns
    RemovedNulls = Table.SelectRows(
        ChangedTypes,
        each [transaction_id] <> null
            and [transaction_date] <> null
            and [quantity] <> null
    ),

    // Trim text columns
    TrimmedText = Table.TransformColumns(
        RemovedNulls,
        {
            {"transaction_id", Text.Trim, type text},
            {"product_name", Text.Trim, type text}
        }
    ),

    // Step 6: Clean product names (uppercase, remove extra spaces)
    CleanedProducts = Table.TransformColumns(
        TrimmedText,
        {
            {"product_name", each Text.Upper(Text.Clean(_)), type text}
        }
    ),

    // Step 7: Add calculated revenue column
    AddedRevenue = Table.AddColumn(
        CleanedProducts,
        "revenue",
        each [quantity] * [unit_price],
        type number
    ),

    // Step 8: Remove duplicates by transaction_id
    RemovedDuplicates = Table.Distinct(
        AddedRevenue,
        {"transaction_id"}
    ),

    // Step 9: Add Silver metadata
    AddedValidationTimestamp = Table.AddColumn(
        RemovedDuplicates,
        "_ValidatedAt",
        each DateTime.LocalNow(),
        type datetime
    ),

    // Step 10: Final output
    Output = AddedValidationTimestamp
in
    Output
```

### Example 2: Customer Data with Validation
**Input:**
```
bronze_source: Bronze_Customers
output_table: Silver_Customers
transformations: |
  - Validate email format
  - Standardize phone numbers
  - Parse full address
  - Calculate customer age
data_quality_checks: true
deduplication: true
dedup_columns: customer_id
```

**Output:**
```powerquery-m
// Query: Silver_Customers
// Purpose: Silver layer - Clean and transform Bronze_Customers
// Source: Bronze layer query Bronze_Customers
// Generated: 2025-12-05

// SCHEMA INPUT
// From Bronze layer (see Bronze_Customers)

// SCHEMA OUTPUT
// Transformed columns:
// - customer_id: text - unique customer identifier
// - first_name: text - customer first name
// - last_name: text - customer last name
// - email: text - validated email address
// - phone: text - standardized phone number
// - birth_date: date - date of birth
// - age: number - calculated age in years
// - _ValidatedAt: datetime - validation timestamp

let
    // Step 1: Load from Bronze layer
    Source = Bronze_Customers,

    // Step 2: Remove Bronze metadata
    RemovedMetadata = Table.RemoveColumns(
        Source,
        {"_LoadTimestamp", "_SourceFile"}
    ),

    // Step 3: Rename columns to snake_case
    RenamedColumns = Table.RenameColumns(
        RemovedMetadata,
        {
            {"CustomerID", "customer_id"},
            {"FirstName", "first_name"},
            {"LastName", "last_name"},
            {"Email", "email"},
            {"Phone", "phone"},
            {"BirthDate", "birth_date"}
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
            {"birth_date", type date}
        }
    ),

    // Step 5: Data quality - remove nulls
    RemovedNulls = Table.SelectRows(
        ChangedTypes,
        each [customer_id] <> null
            and [email] <> null
    ),

    // Trim text columns
    TrimmedText = Table.TransformColumns(
        RemovedNulls,
        {
            {"customer_id", Text.Trim, type text},
            {"first_name", Text.Trim, type text},
            {"last_name", Text.Trim, type text},
            {"email", each Text.Lower(Text.Trim(_)), type text}
        }
    ),

    // Step 6: Validate email format
    ValidatedEmail = Table.SelectRows(
        TrimmedText,
        each Text.Contains([email], "@") and Text.Contains([email], ".")
    ),

    // Step 7: Standardize phone numbers (remove non-digits)
    CleanedPhone = Table.TransformColumns(
        ValidatedEmail,
        {
            {"phone", each Text.Select(_, {"0".."9"}), type text}
        }
    ),

    // Step 8: Calculate age
    AddedAge = Table.AddColumn(
        CleanedPhone,
        "age",
        each Duration.Days(DateTime.LocalNow() - DateTime.From([birth_date])) / 365.25,
        type number
    ),

    // Round age to whole number
    RoundedAge = Table.TransformColumns(
        AddedAge,
        {{"age", Number.Round, Int64.Type}}
    ),

    // Step 9: Remove duplicates
    RemovedDuplicates = Table.Distinct(
        RoundedAge,
        {"customer_id"}
    ),

    // Step 10: Add validation timestamp
    AddedValidationTimestamp = Table.AddColumn(
        RemovedDuplicates,
        "_ValidatedAt",
        each DateTime.LocalNow(),
        type datetime
    ),

    // Step 11: Final output
    Output = AddedValidationTimestamp
in
    Output
```

### Example 3: CSV with Header Promotion
**Input:**
```
bronze_source: Bronze_VendorInvoices
output_table: Silver_VendorInvoices
promote_headers: true
transformations: |
  - Convert invoice amounts
  - Parse dates
  - Categorize vendors
data_quality_checks: true
deduplication: false
```

**Output:**
```powerquery-m
// Query: Silver_VendorInvoices
// Purpose: Silver layer - Clean and transform Bronze_VendorInvoices
// Source: Bronze layer query Bronze_VendorInvoices
// Generated: 2025-12-05

let
    // Step 1: Load from Bronze layer
    Source = Bronze_VendorInvoices,

    // Step 2: Remove Bronze metadata
    RemovedMetadata = Table.RemoveColumns(
        Source,
        {"_LoadTimestamp", "_SourceFile", "_LoadError"}
    ),

    // Step 3: Promote first row to headers (CSV source)
    PromotedHeaders = Table.PromoteHeaders(
        RemovedMetadata,
        [PromoteAllScalars=true]
    ),

    // Step 4: Rename columns to snake_case
    RenamedColumns = Table.RenameColumns(
        PromotedHeaders,
        {
            {"Invoice Number", "invoice_number"},
            {"Vendor Name", "vendor_name"},
            {"Invoice Date", "invoice_date"},
            {"Due Date", "due_date"},
            {"Amount", "invoice_amount"},
            {"Status", "payment_status"}
        }
    ),

    // Step 5: Type conversions
    ChangedTypes = Table.TransformColumnTypes(
        RenamedColumns,
        {
            {"invoice_number", type text},
            {"vendor_name", type text},
            {"invoice_date", type date},
            {"due_date", type date},
            {"invoice_amount", type number},
            {"payment_status", type text}
        }
    ),

    // Step 6: Data quality checks
    RemovedNulls = Table.SelectRows(
        ChangedTypes,
        each [invoice_number] <> null
            and [vendor_name] <> null
            and [invoice_amount] <> null
    ),

    TrimmedText = Table.TransformColumns(
        RemovedNulls,
        {
            {"invoice_number", Text.Trim, type text},
            {"vendor_name", Text.Trim, type text},
            {"payment_status", Text.Trim, type text}
        }
    ),

    // Step 7: Add vendor category based on name
    AddedCategory = Table.AddColumn(
        TrimmedText,
        "vendor_category",
        each if Text.Contains([vendor_name], "Tech") then "Technology"
            else if Text.Contains([vendor_name], "Supply") then "Supplies"
            else "Other",
        type text
    ),

    // Step 8: Add validation timestamp
    AddedValidationTimestamp = Table.AddColumn(
        AddedCategory,
        "_ValidatedAt",
        each DateTime.LocalNow(),
        type datetime
    ),

    // Step 9: Final output
    Output = AddedValidationTimestamp
in
    Output
```

## Usage Notes

### Silver Layer Principles
1. **Source from Bronze**: Always load from Bronze layer (never direct source)
2. **Standardize Schema**: Consistent column names (snake_case), types
3. **Clean Data**: Remove nulls, trim text, validate formats
4. **Apply Business Rules**: Simple transformations (complex = Gold)
5. **Add Validation Metadata**: Track when data was validated

### Common Transformations
- **Type conversions**: Text.From(), Number.From(), Date.From()
- **Text cleaning**: Text.Trim(), Text.Clean(), Text.Upper/Lower()
- **Null handling**: Table.SelectRows(), try...otherwise
- **Deduplication**: Table.Distinct()
- **Column operations**: Table.AddColumn(), Table.RemoveColumns()

### Error Handling Pattern
```powerquery-m
SafeConversion = Table.TransformColumns(
    Source,
    {
        {"column_name", each try Number.From(_) otherwise null, type number}
    }
)
```

### When to Use This Pattern
- Cleaning raw data from Bronze
- Standardizing column names and types
- Applying data quality rules
- Preparing data for Gold layer
- Creating reusable curated datasets

## Related Patterns
- `power-query-bronze.pattern.md` - Prerequisite: load raw data
- `dax-measure.pattern.md` - Next step: create metrics on Silver data
- `dataflow-gen2.pattern.md` - For Fabric implementation

## Testing Checklist
After implementing Silver layer:
- [ ] Sources from Bronze layer (not direct source)
- [ ] All columns follow snake_case convention
- [ ] Data types correctly assigned
- [ ] Null handling works correctly
- [ ] Business rules applied as expected
- [ ] Duplicates removed (if specified)
- [ ] _ValidatedAt timestamp added
- [ ] Query refreshes without error
- [ ] Data quality improved from Bronze
