# Python Standards for Data Engineering

## Code Style
- Follow PEP 8 style guide
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use descriptive variable names (no single letters except loop counters)

## Data Processing with Polars
- Prefer Polars over Pandas for large datasets (>100MB)
- Use lazy evaluation (.lazy()) for complex transformations
- Chain operations for readability
- Use explicit schema definitions for data validation

### Example Pattern
```python
import polars as pl

def transform_emissions_data(df: pl.DataFrame) -> pl.DataFrame:
    """Transform emissions data with validation and cleaning."""
    return (
        df.lazy()
        .filter(pl.col("emission_value").is_not_null())
        .with_columns([
            pl.col("date").str.to_date("%Y-%m-%d"),
            pl.col("emission_value").cast(pl.Float64)
        ])
        .group_by("facility_id")
        .agg([
            pl.col("emission_value").sum().alias("total_emissions"),
            pl.col("date").max().alias("latest_date")
        ])
        .collect()
    )
```

## Error Handling
- Use specific exception types
- Log errors with context (use structured logging)
- Implement retry logic for external API calls
- Validate data at pipeline boundaries

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def fetch_api_data(endpoint: str, max_retries: int = 3) -> Optional[dict]:
    """Fetch data from API with retry logic."""
    for attempt in range(max_retries):
        try:
            response = requests.get(endpoint, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.warning(f"API call failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"All retries exhausted for {endpoint}")
                raise
    return None
```

## Data Validation
- Define schemas using Polars or Pydantic
- Validate early in the pipeline
- Log validation failures with row details
- Separate valid/invalid records for review

## File Organization
```
src/
├── etl/
│   ├── extractors/     # Data source connectors
│   ├── transformers/   # Data transformation logic
│   ├── loaders/        # Data destination writers
│   └── validators/     # Data quality checks
├── models/             # Data models and schemas
├── utils/              # Shared utilities
└── config/             # Configuration management
```

## Dependencies
- Use `pyproject.toml` for dependency management
- Pin major and minor versions for reproducibility
- Separate dev/test/prod dependencies
- Document why each dependency is needed

## Performance
- Profile code for bottlenecks (use `py-spy` or `cProfile`)
- Use generators for large datasets
- Batch database operations
- Cache expensive computations appropriately
