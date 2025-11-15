# SQL Standards

## General Conventions
- Use uppercase for SQL keywords: `SELECT`, `FROM`, `WHERE`, `JOIN`
- Use snake_case for table and column names
- Always qualify columns with table aliases in joins
- Indent nested queries for readability

## Query Structure
```sql
-- Template for standard queries
SELECT
    f.facility_id,
    f.facility_name,
    SUM(e.emission_value) AS total_emissions,
    COUNT(DISTINCT e.reporting_date) AS reporting_days
FROM facilities AS f
INNER JOIN emissions AS e
    ON f.facility_id = e.facility_id
WHERE e.reporting_date >= '2024-01-01'
    AND e.emission_value > 0
GROUP BY
    f.facility_id,
    f.facility_name
HAVING SUM(e.emission_value) > 1000
ORDER BY total_emissions DESC;
```

## Table Design
- Every table should have a primary key
- Use appropriate data types (don't store dates as strings)
- Add NOT NULL constraints where applicable
- Include created_at and updated_at timestamps
- Use descriptive table and column names

### Naming Conventions
- Tables: plural nouns (`facilities`, `emissions`, `reports`)
- Columns: descriptive names (`facility_id`, `emission_value`, `reporting_date`)
- Indexes: `idx_{table}_{column(s)}` (e.g., `idx_emissions_facility_date`)
- Foreign keys: `fk_{table}_{referenced_table}` (e.g., `fk_emissions_facilities`)

## Joins
- Prefer explicit `INNER JOIN` over implicit joins in WHERE clause
- Use `LEFT JOIN` when you need all records from left table
- Always specify join conditions explicitly
- Consider join order for performance (smaller tables first)

```sql
-- Good: Explicit join
SELECT e.*, f.facility_name
FROM emissions AS e
INNER JOIN facilities AS f ON e.facility_id = f.facility_id;

-- Avoid: Implicit join
SELECT e.*, f.facility_name
FROM emissions e, facilities f
WHERE e.facility_id = f.facility_id;
```

## Performance
- Create indexes on frequently queried columns
- Avoid `SELECT *` - specify needed columns
- Use `EXISTS` instead of `IN` for subqueries with large result sets
- Analyze query execution plans for optimization
- Batch INSERT/UPDATE operations

```sql
-- Use EXISTS for better performance
SELECT f.facility_id
FROM facilities AS f
WHERE EXISTS (
    SELECT 1
    FROM emissions AS e
    WHERE e.facility_id = f.facility_id
        AND e.reporting_date > '2024-01-01'
);
```

## CTEs (Common Table Expressions)
- Use CTEs for complex queries to improve readability
- Name CTEs descriptively
- Break complex logic into multiple CTEs

```sql
WITH recent_emissions AS (
    SELECT
        facility_id,
        SUM(emission_value) AS total_value
    FROM emissions
    WHERE reporting_date >= '2024-01-01'
    GROUP BY facility_id
),
high_emitters AS (
    SELECT facility_id
    FROM recent_emissions
    WHERE total_value > 10000
)
SELECT
    f.facility_name,
    re.total_value
FROM facilities AS f
INNER JOIN high_emitters AS he ON f.facility_id = he.facility_id
INNER JOIN recent_emissions AS re ON f.facility_id = re.facility_id;
```

## Migrations
- All schema changes must have migration scripts
- Migrations must be reversible (include rollback)
- Test migrations on dev/staging before production
- Document breaking changes clearly
- Use version numbers in migration file names: `001_create_facilities.sql`

## Data Quality
- Add CHECK constraints for data validation
- Use FOREIGN KEY constraints to maintain referential integrity
- Consider UNIQUE constraints where appropriate
- Document business rules in comments

```sql
CREATE TABLE emissions (
    emission_id BIGINT PRIMARY KEY,
    facility_id BIGINT NOT NULL,
    emission_value DECIMAL(15,2) NOT NULL,
    reporting_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT fk_emissions_facilities
        FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
    CONSTRAINT chk_emission_value_positive
        CHECK (emission_value >= 0),
    CONSTRAINT chk_reporting_date_valid
        CHECK (reporting_date <= CURRENT_DATE)
);

-- Indexes
CREATE INDEX idx_emissions_facility_date
    ON emissions(facility_id, reporting_date);
```
