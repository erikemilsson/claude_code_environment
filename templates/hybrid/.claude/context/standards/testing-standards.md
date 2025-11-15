# Testing Standards for Data Engineering

## Testing Philosophy
- All data transformations must have unit tests
- Integration tests for external dependencies (APIs, databases)
- Data quality tests for pipeline outputs
- Minimum 80% code coverage for business logic

## Test Structure
Use pytest framework with clear test organization:

```
tests/
├── unit/
│   ├── test_extractors.py
│   ├── test_transformers.py
│   └── test_validators.py
├── integration/
│   ├── test_api_clients.py
│   └── test_database_loaders.py
├── data_quality/
│   ├── test_schema_validation.py
│   └── test_business_rules.py
└── fixtures/
    ├── sample_data/
    └── conftest.py
```

## Unit Tests

### Naming Convention
- Test files: `test_{module_name}.py`
- Test functions: `test_{function_name}_{scenario}_{expected_result}`

### Example
```python
import polars as pl
import pytest
from src.etl.transformers import transform_emissions_data

def test_transform_emissions_data_filters_null_values():
    """Test that null emission values are filtered out."""
    # Arrange
    input_df = pl.DataFrame({
        "facility_id": [1, 2, 3],
        "emission_value": [100.0, None, 200.0],
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"]
    })

    # Act
    result = transform_emissions_data(input_df)

    # Assert
    assert result.height == 2
    assert result.filter(pl.col("emission_value").is_null()).height == 0

def test_transform_emissions_data_aggregates_by_facility():
    """Test that emissions are correctly summed by facility."""
    # Arrange
    input_df = pl.DataFrame({
        "facility_id": [1, 1, 2],
        "emission_value": [100.0, 150.0, 200.0],
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"]
    })

    # Act
    result = transform_emissions_data(input_df)

    # Assert
    assert result.height == 2
    facility_1 = result.filter(pl.col("facility_id") == 1)
    assert facility_1["total_emissions"][0] == 250.0
```

## Integration Tests

### Database Testing
Use fixtures for database setup/teardown:

```python
import pytest
import psycopg2
from src.etl.loaders import load_to_azure_sql

@pytest.fixture
def test_db_connection():
    """Provide test database connection."""
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="test_user",
        password="test_pass"
    )
    yield conn
    conn.rollback()  # Rollback after test
    conn.close()

def test_load_to_azure_sql_inserts_records(test_db_connection):
    """Test that records are successfully inserted."""
    # Arrange
    test_data = pl.DataFrame({
        "facility_id": [1],
        "emission_value": [100.0],
        "reporting_date": ["2024-01-01"]
    })

    # Act
    load_to_azure_sql(test_data, test_db_connection)

    # Assert
    cursor = test_db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM emissions")
    count = cursor.fetchone()[0]
    assert count == 1
```

### API Testing
Mock external APIs for reliable tests:

```python
import pytest
from unittest.mock import patch, Mock
from src.etl.extractors import fetch_emissions_data

@patch('src.etl.extractors.requests.get')
def test_fetch_emissions_data_handles_api_success(mock_get):
    """Test successful API response handling."""
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"emissions": [{"value": 100}]}
    mock_get.return_value = mock_response

    # Act
    result = fetch_emissions_data("https://api.example.com/emissions")

    # Assert
    assert result["emissions"][0]["value"] == 100
    mock_get.assert_called_once()

@patch('src.etl.extractors.requests.get')
def test_fetch_emissions_data_retries_on_failure(mock_get):
    """Test that API failures trigger retry logic."""
    # Arrange
    mock_get.side_effect = [
        Exception("Network error"),
        Mock(status_code=200, json=lambda: {"emissions": []})
    ]

    # Act
    result = fetch_emissions_data("https://api.example.com/emissions")

    # Assert
    assert result is not None
    assert mock_get.call_count == 2
```

## Data Quality Tests

### Schema Validation
```python
import polars as pl
from src.etl.validators import validate_emissions_schema

def test_validate_emissions_schema_accepts_valid_data():
    """Test schema validation passes for valid data."""
    # Arrange
    valid_df = pl.DataFrame({
        "facility_id": [1],
        "emission_value": [100.0],
        "reporting_date": ["2024-01-01"]
    })

    # Act & Assert
    assert validate_emissions_schema(valid_df) is True

def test_validate_emissions_schema_rejects_missing_columns():
    """Test schema validation fails for missing required columns."""
    # Arrange
    invalid_df = pl.DataFrame({
        "facility_id": [1],
        "emission_value": [100.0]
        # missing reporting_date
    })

    # Act & Assert
    with pytest.raises(ValueError, match="Missing required column: reporting_date"):
        validate_emissions_schema(invalid_df)
```

### Business Rule Validation
```python
def test_emission_values_are_non_negative():
    """Test that all emission values are >= 0."""
    # This would run against actual pipeline output
    df = pl.read_csv("output/emissions.csv")

    negative_values = df.filter(pl.col("emission_value") < 0)
    assert negative_values.height == 0, "Found negative emission values"

def test_reporting_dates_are_not_future():
    """Test that reporting dates are not in the future."""
    from datetime import date

    df = pl.read_csv("output/emissions.csv")
    today = date.today()

    future_dates = df.filter(pl.col("reporting_date") > today.isoformat())
    assert future_dates.height == 0, "Found future reporting dates"
```

## Test Fixtures
Create reusable test data:

```python
# tests/fixtures/conftest.py
import pytest
import polars as pl

@pytest.fixture
def sample_emissions_data():
    """Provide sample emissions data for tests."""
    return pl.DataFrame({
        "facility_id": [1, 1, 2, 2],
        "emission_value": [100.0, 150.0, 200.0, 250.0],
        "reporting_date": [
            "2024-01-01", "2024-01-02",
            "2024-01-01", "2024-01-02"
        ]
    })

@pytest.fixture
def empty_emissions_data():
    """Provide empty DataFrame with correct schema."""
    return pl.DataFrame({
        "facility_id": [],
        "emission_value": [],
        "reporting_date": []
    })
```

## Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_transformers.py

# Run tests matching pattern
pytest -k "test_transform"

# Run with verbose output
pytest -v
```

## Continuous Integration
- All tests must pass before merging to main
- Coverage reports should be generated
- Integration tests run in isolated environment
- Data quality tests run on sample production data
