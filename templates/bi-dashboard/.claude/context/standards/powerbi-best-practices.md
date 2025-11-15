# Power BI Best Practices

## Data Model Design

### Star Schema
- Use star schema design: fact tables in center, dimension tables around
- Fact tables contain measures/metrics (sales, quantities, counts)
- Dimension tables contain descriptive attributes (products, customers, dates)
- Minimize snowflaking (dimension tables connecting to other dimension tables)

```
    Customers
        |
    Products --- Sales --- Time
        |
    Regions
```

### Relationships
- Establish proper relationships between tables
- Use single-direction filtering when possible (better performance)
- Minimize bi-directional relationships (only when necessary)
- Always have one active relationship between tables
- Use inactive relationships sparingly, activated via USERELATIONSHIP()

### Date Table
- ALWAYS create a dedicated Date table
- Mark Date table as Date Table in model settings
- Include: Date, Year, Quarter, Month, Week, Day columns
- Add fiscal period columns if applicable
- Ensure continuous date range covering all data

## Data Model Optimization

### Reduce Model Size
- Remove unnecessary columns (especially from fact tables)
- Use integer columns instead of text for relationships
- Disable "Load to Model" for staging queries
- Use appropriate data types (smallest that fits the data)
- Consider import vs DirectQuery based on use case

### Column Data Types
- Use whole numbers instead of decimals when possible
- Use date instead of datetime if time is not needed
- Avoid text columns in fact tables (use surrogate keys)
- Use Boolean instead of text for Yes/No values

### Calculated Columns vs Measures
- **Prefer Measures** - They calculate at query time and don't bloat model
- **Use Calculated Columns** only when:
  - Needed for slicing/filtering (row context)
  - Value doesn't change with filters
  - Complex calculations that don't work in DAX measures

## Report Design

### Visual Best Practices
- Limit visuals per page (5-8 maximum for performance)
- Use appropriate visual types for data:
  - Line charts for trends over time
  - Bar/column for comparisons
  - Pie charts only for 2-4 categories
  - Tables for detailed data (minimize rows shown)
  - Cards for single KPI values
- Enable "Reduce data" options for large datasets
- Use visual-level filters instead of report-level when possible

### Page Layout
- Design for target screen resolution (1920x1080 common)
- Use consistent visual sizing and alignment
- Group related visuals using visual containers
- Provide clear titles and labels
- Use bookmarks for different views of same data

### Formatting Standards
- Use consistent color scheme across entire report
- Apply conditional formatting to highlight insights
- Use data labels sparingly (when they add value)
- Set appropriate number formats (%, $, decimals)
- Use tooltips for additional context

### Navigation
- Create home page with navigation to other pages
- Use buttons with page navigation actions
- Implement drill-through where appropriate
- Add back buttons on detail pages
- Use bookmarks for story-telling

## Performance Optimization

### Data Refresh
- Schedule refreshes during off-peak hours
- Incremental refresh for large datasets (Premium)
- Use parameters for dynamic data source connections
- Monitor refresh history for failures
- Set appropriate refresh frequency (not more often than data updates)

### Query Performance
- Use aggregations for large datasets (Premium)
- Minimize use of calculated tables
- Avoid complex DAX in visuals (pre-calculate if possible)
- Use SUMMARIZE carefully (can be slow)
- Monitor query performance with Performance Analyzer

### Report Performance
- Reduce number of visuals per page
- Limit rows returned in tables/matrices
- Use "Show items with no data" sparingly
- Avoid high cardinality fields in slicers
- Use visual interactions appropriately (disable when not needed)

## Security

### Row-Level Security (RLS)
- Define roles in Power BI Desktop
- Test RLS using "View as" feature
- Use dynamic RLS with USERNAME() or USERPRINCIPALNAME()
- Document RLS logic clearly
- Minimize number of roles for manageability

```dax
// RLS Filter Example
// Apply to Region table
[Region] = USERPRINCIPALNAME()

// Or use mapping table
[UserEmail] = LOOKUPVALUE(
    UserAccess[Email],
    UserAccess[Email],
    USERPRINCIPALNAME()
)
```

### Data Sensitivity
- Apply sensitivity labels to reports and datasets
- Restrict access using workspaces and apps
- Use Microsoft Information Protection integration
- Don't hardcode credentials in queries
- Use service principal for automated deployments

## Development Workflow

### Version Control
- Use Power BI Desktop files (.pbix) in version control
- Save separate .pbit (template) files without data
- Document major changes in commit messages
- Use development/test/production workspaces
- Tag releases for deployment tracking

### Testing
- Test with realistic data volumes
- Verify calculations against source systems
- Test all slicers and filter combinations
- Validate RLS for all roles
- Check cross-browser compatibility
- Performance test with concurrent users

### Documentation
- Document data model (tables, relationships, business logic)
- Add descriptions to measures (show in tooltips)
- Create data dictionary for business users
- Document refresh schedules and dependencies
- Maintain change log for report versions

## Naming Conventions

### Objects
- Tables: Plural nouns (`Sales`, `Customers`, `Products`)
- Measures: Descriptive with aggregation (`Total Revenue`, `Distinct Customers`)
- Columns: PascalCase (`OrderDate`, `ProductName`, `CustomerID`)
- Hidden tables: Underscore prefix (`_Measures`, `_Parameters`)

### Measures
```dax
// Good measure names
Total Sales
Average Order Value
Customer Count
YTD Revenue
Sales vs PY %
Customer Lifetime Value

// Avoid vague names
Measure1
Calculation
Sum
Total
```

## Workspace Organization

### Workspace Structure
- Separate workspaces for Dev, Test, Prod environments
- Use workspace names that indicate purpose
- Apply appropriate roles:
  - Admin: IT/BI team
  - Member: Report developers
  - Contributor: Content creators
  - Viewer: Business users
- Use Apps for distributing content to end users

### Content Organization
- Group related reports in same workspace
- Use consistent naming for reports and datasets
- Separate datasets from reports (shared datasets)
- Archive old reports (don't delete immediately)
- Use deployment pipelines for automation (Premium)

## Data Sources

### Connection Best Practices
- Use parameters for connection strings
- Store credentials securely (use gateway)
- Prefer native connectors over generic (ODBC/OLEDB)
- Use DirectQuery only when necessary
- Consider composite models (import + DirectQuery)

### Gateway Configuration
- Install gateway close to data source
- Use dedicated machine for gateway
- Keep gateway updated
- Monitor gateway performance
- Set appropriate privacy levels

## Monitoring and Maintenance

### Usage Metrics
- Enable usage metrics for workspaces
- Monitor report views and unique users
- Track query performance trends
- Identify unused reports for archival
- Review refresh failure patterns

### Capacity Management (Premium)
- Monitor capacity usage via metrics app
- Identify resource-intensive reports/datasets
- Set autoscale rules if available
- Plan capacity upgrades based on growth
- Use reserved capacity for production

## Common Anti-Patterns to Avoid

### Data Model
- ❌ Many-to-many relationships (use bridge table instead)
- ❌ Circular dependencies in relationships
- ❌ Using DirectQuery for all tables (mix with import)
- ❌ Not using a Date table
- ❌ Storing aggregated and detailed data in same table

### DAX
- ❌ Using FILTER on large tables without need
- ❌ Nested CALCULATE statements (use CALCULATETABLE)
- ❌ Using ALL() when REMOVEFILTERS is better
- ❌ Overly complex measures (break into smaller measures)
- ❌ Hardcoding values instead of using parameters

### Reports
- ❌ Too many visuals on one page (>10)
- ❌ Using pie charts for >5 categories
- ❌ No filters or slicers for exploration
- ❌ Inconsistent color schemes across pages
- ❌ Missing titles or context for visuals

## Collaboration

### Sharing Content
- Use Apps for end-user distribution
- Embed reports in Teams/SharePoint when appropriate
- Use Power BI Mobile for on-the-go access
- Configure email subscriptions for stakeholders
- Set up alerts for important metrics

### Change Management
- Communicate changes to report users
- Provide training for new features
- Document breaking changes
- Plan upgrades during low-usage periods
- Maintain backwards compatibility when possible

## Accessibility

### Report Accessibility
- Add alt text to all visuals
- Use tab order for keyboard navigation
- Ensure sufficient color contrast
- Support screen readers
- Provide text alternatives for visual-only insights
- Use accessible color palettes (colorblind-friendly)

### Best Practices
- Test reports with accessibility checker
- Use clear, descriptive titles
- Avoid relying solely on color to convey information
- Enable "Show data table" for visuals
- Provide report documentation/help
