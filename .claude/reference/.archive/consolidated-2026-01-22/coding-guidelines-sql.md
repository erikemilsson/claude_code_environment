# SQL Coding Guidelines for Claude 4

## SQL-Specific Best Practices

### 1. Query Structure and Formatting

```sql
-- GOOD: Clear, readable structure
WITH customer_orders AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COUNT(o.order_id) AS order_count,
        SUM(o.total_amount) AS total_spent
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        AND o.order_date >= '2024-01-01'
    WHERE c.is_active = TRUE
    GROUP BY c.customer_id, c.customer_name
)
SELECT
    customer_name,
    order_count,
    total_spent,
    CASE
        WHEN total_spent > 10000 THEN 'Premium'
        WHEN total_spent > 5000 THEN 'Gold'
        ELSE 'Standard'
    END AS customer_tier
FROM customer_orders
ORDER BY total_spent DESC;

-- BAD: Poor formatting, unclear
select c.customer_name,count(o.order_id),sum(o.total_amount),
case when sum(o.total_amount)>10000 then 'Premium' when sum(o.total_amount)>5000 then 'Gold' else 'Standard' end
from customers c left join orders o on c.customer_id=o.customer_id
where c.is_active=true and o.order_date>='2024-01-01'
group by c.customer_id,c.customer_name order by 3 desc;
```

### 2. CTEs vs Subqueries

```sql
-- GOOD: CTEs for readability
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', sale_date) AS month,
        product_id,
        SUM(quantity) AS units_sold,
        SUM(revenue) AS total_revenue
    FROM sales
    WHERE sale_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY 1, 2
),
product_rankings AS (
    SELECT
        month,
        product_id,
        units_sold,
        total_revenue,
        RANK() OVER (PARTITION BY month ORDER BY total_revenue DESC) AS revenue_rank
    FROM monthly_sales
)
SELECT *
FROM product_rankings
WHERE revenue_rank <= 10;

-- BAD: Nested subqueries
SELECT * FROM (
    SELECT month, product_id, units_sold, total_revenue,
    RANK() OVER (PARTITION BY month ORDER BY total_revenue DESC) AS revenue_rank
    FROM (
        SELECT DATE_TRUNC('month', sale_date) AS month,
        product_id, SUM(quantity) AS units_sold, SUM(revenue) AS total_revenue
        FROM sales WHERE sale_date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY 1, 2
    ) monthly_sales
) ranked WHERE revenue_rank <= 10;
```

### 3. Join Optimization

```sql
-- GOOD: Explicit join conditions, appropriate join types
SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
INNER JOIN products p
    ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
    AND c.country = 'USA';

-- BAD: Cartesian products, missing join conditions
SELECT *
FROM orders, customers, order_items, products
WHERE orders.customer_id = customers.customer_id
    AND orders.order_id = order_items.order_id
    AND products.product_id = order_items.product_id;
```

### 4. Index-Aware Queries

```sql
-- GOOD: Leverage indexes
-- Assuming index on (customer_id, order_date)
SELECT *
FROM orders
WHERE customer_id = 12345
    AND order_date BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY order_date DESC;

-- BAD: Function on indexed column prevents index use
SELECT *
FROM orders
WHERE YEAR(order_date) = 2024
    AND MONTH(order_date) = 12;

-- GOOD: Rewrite to use index
SELECT *
FROM orders
WHERE order_date >= '2024-12-01'
    AND order_date < '2025-01-01';
```

### 5. Window Functions

```sql
-- GOOD: Efficient use of window functions
WITH sales_analysis AS (
    SELECT
        salesperson_id,
        sale_date,
        sale_amount,
        -- Running total
        SUM(sale_amount) OVER (
            PARTITION BY salesperson_id
            ORDER BY sale_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total,
        -- Moving average (last 7 days)
        AVG(sale_amount) OVER (
            PARTITION BY salesperson_id
            ORDER BY sale_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS moving_avg_7day,
        -- Rank within month
        RANK() OVER (
            PARTITION BY salesperson_id, DATE_TRUNC('month', sale_date)
            ORDER BY sale_amount DESC
        ) AS monthly_rank
    FROM sales
)
SELECT *
FROM sales_analysis
WHERE monthly_rank <= 5;
```

### 6. Data Modification Best Practices

```sql
-- GOOD: Use transactions for multi-statement operations
BEGIN TRANSACTION;

-- Update with explicit conditions
UPDATE inventory
SET quantity = quantity - ordered.total_quantity
FROM (
    SELECT product_id, SUM(quantity) as total_quantity
    FROM order_items
    WHERE order_id = 12345
    GROUP BY product_id
) ordered
WHERE inventory.product_id = ordered.product_id
    AND inventory.quantity >= ordered.total_quantity;

-- Check affected rows
GET DIAGNOSTICS row_count = ROW_COUNT;

IF row_count != expected_count THEN
    ROLLBACK;
    RAISE EXCEPTION 'Inventory update failed';
ELSE
    COMMIT;
END IF;

-- GOOD: Soft deletes for audit trail
UPDATE customers
SET
    is_deleted = TRUE,
    deleted_at = CURRENT_TIMESTAMP,
    deleted_by = CURRENT_USER
WHERE customer_id = 12345
    AND is_deleted = FALSE;
```

### 7. Performance Optimization Patterns

```sql
-- GOOD: EXISTS for existence checks
SELECT c.*
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
        AND o.order_date >= CURRENT_DATE - INTERVAL '30 days'
);

-- BAD: IN with subquery returning many rows
SELECT *
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
);

-- GOOD: Materialized CTE for reused subqueries
WITH MATERIALIZED recent_orders AS (
    SELECT customer_id, COUNT(*) as order_count
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    ro1.order_count as recent_orders,
    ro2.order_count as comparison_orders
FROM customers c
LEFT JOIN recent_orders ro1 ON c.customer_id = ro1.customer_id
LEFT JOIN recent_orders ro2 ON c.referrer_id = ro2.customer_id;
```

### 8. Error Handling and Validation

```sql
-- GOOD: Validate data before operations
DO $$
DECLARE
    v_count INTEGER;
BEGIN
    -- Check for duplicates before insert
    SELECT COUNT(*)
    INTO v_count
    FROM customers
    WHERE email = 'new@email.com';

    IF v_count > 0 THEN
        RAISE EXCEPTION 'Customer with email % already exists', 'new@email.com';
    END IF;

    -- Proceed with insert
    INSERT INTO customers (name, email)
    VALUES ('New Customer', 'new@email.com');

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error: %', SQLERRM;
        RAISE;
END $$;
```

### 9. Common Table Patterns

```sql
-- Hierarchical data (recursive CTE)
WITH RECURSIVE org_hierarchy AS (
    -- Anchor: top-level employees
    SELECT
        employee_id,
        name,
        manager_id,
        1 AS level,
        name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: employees under managers
    SELECT
        e.employee_id,
        e.name,
        e.manager_id,
        oh.level + 1,
        oh.path || ' > ' || e.name
    FROM employees e
    INNER JOIN org_hierarchy oh
        ON e.manager_id = oh.employee_id
)
SELECT * FROM org_hierarchy
ORDER BY path;

-- Pivot data
SELECT
    product_id,
    MAX(CASE WHEN month = '2024-01' THEN revenue END) AS jan_2024,
    MAX(CASE WHEN month = '2024-02' THEN revenue END) AS feb_2024,
    MAX(CASE WHEN month = '2024-03' THEN revenue END) AS mar_2024
FROM (
    SELECT
        product_id,
        TO_CHAR(sale_date, 'YYYY-MM') AS month,
        SUM(revenue) AS revenue
    FROM sales
    WHERE sale_date >= '2024-01-01'
        AND sale_date < '2024-04-01'
    GROUP BY product_id, TO_CHAR(sale_date, 'YYYY-MM')
) monthly_sales
GROUP BY product_id;
```

### 10. Database-Specific Optimizations

#### PostgreSQL
```sql
-- Use EXPLAIN ANALYZE for query planning
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM large_table WHERE conditions;

-- Array operations
SELECT *
FROM products
WHERE tags @> ARRAY['electronics', 'wireless'];

-- JSONB operations
SELECT
    id,
    data->>'name' AS name,
    data->'address'->>'city' AS city
FROM users
WHERE data @> '{"status": "active"}'::jsonb;
```

#### SQL Server
```sql
-- Use execution plan
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Table hints (use sparingly)
SELECT *
FROM large_table WITH (NOLOCK)
WHERE conditions;

-- Indexed views
CREATE VIEW sales_summary
WITH SCHEMABINDING
AS
SELECT
    product_id,
    COUNT_BIG(*) AS sale_count,
    SUM(amount) AS total_amount
FROM dbo.sales
GROUP BY product_id;

CREATE UNIQUE CLUSTERED INDEX IX_sales_summary
ON sales_summary(product_id);
```

## Anti-Patterns to Avoid

### 1. SELECT * in Production
```sql
-- BAD: Fetches unnecessary columns
SELECT * FROM customers;

-- GOOD: Explicit column list
SELECT customer_id, customer_name, email, phone
FROM customers;
```

### 2. Implicit Type Conversions
```sql
-- BAD: String comparison on numeric field
SELECT * FROM orders
WHERE order_id = '12345';

-- GOOD: Correct type
SELECT * FROM orders
WHERE order_id = 12345;
```

### 3. Not Using Bind Variables
```sql
-- BAD: SQL injection risk
query = f"SELECT * FROM users WHERE id = {user_input}"

-- GOOD: Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_input,))
```

## Query Optimization Checklist

1. ✅ Use appropriate indexes
2. ✅ Avoid functions on indexed columns
3. ✅ Use EXISTS instead of IN for large datasets
4. ✅ Leverage CTEs for readability
5. ✅ Use window functions instead of self-joins
6. ✅ Filter early in JOINs
7. ✅ Avoid SELECT *
8. ✅ Use EXPLAIN/execution plans
9. ✅ Consider materialized views for complex aggregations
10. ✅ Use appropriate isolation levels

## Quick Reference

| Operation | Prefer | Avoid |
|-----------|--------|-------|
| Existence check | EXISTS | IN (subquery) |
| String matching | LIKE with index | Functions on column |
| Date filtering | Range comparison | Date functions |
| Aggregation reuse | CTE | Repeated subqueries |
| Large updates | Batch processing | Single massive UPDATE |
| Complex logic | Stored procedures | Application loops |
| Temporary data | Temp tables | Multiple CTEs |