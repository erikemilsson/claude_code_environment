# SQL Guidelines

*Language-specific patterns - see core.md for shared principles.*

## Query Structure
```sql
-- Use CTEs for readability
WITH customer_orders AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COUNT(o.order_id) AS order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.is_active = TRUE
    GROUP BY c.customer_id, c.customer_name
)
SELECT * FROM customer_orders
ORDER BY order_count DESC;
```

## Join Optimization
- Use explicit JOIN syntax (not comma-separated)
- Filter early in JOINs
- Ensure join columns are indexed

## Index-Aware Queries
```sql
-- BAD: Function on indexed column
WHERE YEAR(order_date) = 2024

-- GOOD: Range comparison uses index
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'
```

## Window Functions
```sql
-- Running total, moving average, rank
SUM(amount) OVER (PARTITION BY customer_id ORDER BY date) AS running_total,
AVG(amount) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg,
RANK() OVER (PARTITION BY category ORDER BY value DESC) AS rank
```

## Performance Patterns
```sql
-- EXISTS over IN for subqueries
WHERE EXISTS (SELECT 1 FROM orders WHERE customer_id = c.id)

-- Use EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM table WHERE conditions;
```

## Quick Reference

| Operation | Prefer | Avoid |
|-----------|--------|-------|
| Existence check | EXISTS | IN (subquery) |
| String matching | LIKE with index | Functions on column |
| Date filtering | Range comparison | Date functions |
| Aggregation reuse | CTE | Repeated subqueries |
| Large updates | Batch processing | Single massive UPDATE |
| Column selection | Explicit list | SELECT * |
