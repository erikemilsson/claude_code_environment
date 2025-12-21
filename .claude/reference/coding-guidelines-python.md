# Python Coding Guidelines for Claude 4

## Python-Specific Best Practices

### 1. Import Management

```python
# GOOD: Organized, explicit imports
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd
import numpy as np

from myapp.core import utils
from myapp.models import User

# BAD: Star imports, mixed organization
from pandas import *
import os, sys, json
from myapp.core import *
```

### 2. Type Hints and Documentation

```python
# GOOD: Clear types and documentation
def process_data(
    input_file: Path,
    output_format: str = "json",
    validate: bool = True
) -> Dict[str, Any]:
    """
    Process input data and return formatted results.

    Args:
        input_file: Path to input data file
        output_format: Output format (json, csv, parquet)
        validate: Whether to validate input data

    Returns:
        Dictionary containing processed results

    Raises:
        ValidationError: If validation fails
        FileNotFoundError: If input file doesn't exist
    """

# BAD: No types, minimal docs
def process_data(input_file, output_format="json", validate=True):
    # Process the data
    pass
```

### 3. Error Handling Patterns

```python
# GOOD: Specific exceptions with context
class DataValidationError(Exception):
    """Custom exception for data validation failures"""
    pass

def validate_dataframe(df: pd.DataFrame) -> None:
    """Validate dataframe meets requirements"""
    if df.empty:
        raise DataValidationError(
            f"Empty dataframe provided. Expected at least 1 row."
        )

    missing_cols = {"id", "timestamp", "value"} - set(df.columns)
    if missing_cols:
        raise DataValidationError(
            f"Missing required columns: {missing_cols}"
        )

# BAD: Generic exceptions
def validate_dataframe(df):
    if not len(df):
        raise Exception("Bad data")
```

### 4. Pythonic Patterns

#### List Comprehensions vs Loops
```python
# GOOD: Clear comprehensions for simple transforms
squared = [x**2 for x in numbers if x > 0]

# GOOD: Loops for complex logic
results = []
for item in items:
    processed = complex_processing(item)
    if validate(processed):
        results.append(processed)
        log_success(item)

# BAD: Over-complex comprehensions
results = [log_success(item) or processed
          for item in items
          if (processed := complex_processing(item))
          and validate(processed)]
```

#### Context Managers
```python
# GOOD: Always use context managers for resources
with open("data.txt") as f:
    content = f.read()

with database.connection() as conn:
    results = conn.execute(query)

# BAD: Manual resource management
f = open("data.txt")
content = f.read()
f.close()
```

### 5. Pandas Best Practices

```python
# GOOD: Vectorized operations
df["total"] = df["price"] * df["quantity"]
df_filtered = df[df["status"] == "active"]

# BAD: Iterating over rows
for idx, row in df.iterrows():
    df.at[idx, "total"] = row["price"] * row["quantity"]

# GOOD: Method chaining
result = (df
    .dropna(subset=["key_column"])
    .groupby("category")
    .agg({"value": "sum", "count": "mean"})
    .reset_index()
    .sort_values("value", ascending=False))

# BAD: Repeated assignments
df = df.dropna(subset=["key_column"])
df = df.groupby("category").agg({"value": "sum", "count": "mean"})
df = df.reset_index()
df = df.sort_values("value", ascending=False)
```

### 6. Testing Patterns

```python
# GOOD: Comprehensive test with fixtures
import pytest
from pathlib import Path

@pytest.fixture
def sample_data():
    """Provide sample data for tests"""
    return pd.DataFrame({
        "id": [1, 2, 3],
        "value": [10.5, 20.3, 15.7]
    })

def test_process_data(sample_data, tmp_path):
    """Test data processing with various inputs"""
    # Arrange
    input_file = tmp_path / "test_input.csv"
    sample_data.to_csv(input_file, index=False)

    # Act
    result = process_data(input_file, output_format="dict")

    # Assert
    assert "summary" in result
    assert result["row_count"] == 3
    assert abs(result["mean_value"] - 15.5) < 0.1

# BAD: No structure, magic numbers
def test_process():
    result = process_data("test.csv")
    assert result["value"] == 15.5
```

### 7. Performance Optimization

```python
# GOOD: Profile before optimizing
import cProfile
import pstats

def profile_function(func):
    """Decorator to profile function performance"""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)

        return result
    return wrapper

# GOOD: Use appropriate data structures
# For membership testing
valid_ids = {1, 2, 3, 4, 5}  # Set O(1) lookup
if user_id in valid_ids:
    process()

# BAD: List for membership testing
valid_ids = [1, 2, 3, 4, 5]  # List O(n) lookup
if user_id in valid_ids:
    process()
```

### 8. Async Patterns

```python
# GOOD: Proper async/await usage
import asyncio
import aiohttp

async def fetch_data(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch data from URL asynchronously"""
    async with session.get(url) as response:
        return await response.json()

async def fetch_multiple(urls: List[str]) -> List[dict]:
    """Fetch multiple URLs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# BAD: Blocking in async context
async def fetch_data_bad(url):
    import requests  # Blocking library
    return requests.get(url).json()  # Blocks event loop
```

### 9. Configuration Management

```python
# GOOD: Centralized configuration
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Config:
    """Application configuration"""
    database_url: str
    api_key: str
    debug: bool = False
    max_retries: int = 3

    @classmethod
    def from_env(cls):
        """Load configuration from environment"""
        return cls(
            database_url=os.environ["DATABASE_URL"],
            api_key=os.environ["API_KEY"],
            debug=os.environ.get("DEBUG", "").lower() == "true",
            max_retries=int(os.environ.get("MAX_RETRIES", 3))
        )

# BAD: Scattered configuration
database_url = os.environ["DATABASE_URL"]
api_key = os.environ["API_KEY"]
debug = True  # Hardcoded
```

### 10. Common Pitfalls to Avoid

#### Mutable Default Arguments
```python
# BAD: Mutable default
def append_to_list(item, target=[]):
    target.append(item)
    return target

# GOOD: None default with check
def append_to_list(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

#### Late Binding in Loops
```python
# BAD: Late binding issue
funcs = []
for i in range(5):
    funcs.append(lambda: i)
# All functions return 4

# GOOD: Capture value
funcs = []
for i in range(5):
    funcs.append(lambda i=i: i)
# Functions return 0, 1, 2, 3, 4
```

## Python Anti-Patterns

### 1. Using `exec()` or `eval()`
```python
# NEVER DO THIS
user_input = input("Enter calculation: ")
result = eval(user_input)  # Security vulnerability!

# GOOD: Parse and validate
import ast
import operator

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}

def safe_eval(expr):
    """Safely evaluate mathematical expression"""
    node = ast.parse(expr, mode='eval')
    # Validate and evaluate safely
```

### 2. Ignoring PEP 8
```python
# BAD: Non-PEP 8
def MyFunction(MyParameter,AnotherOne):
    MyVariable=MyParameter+AnotherOne
    return MyVariable

# GOOD: PEP 8 compliant
def calculate_sum(first_value, second_value):
    """Calculate sum of two values"""
    total = first_value + second_value
    return total
```

## Quick Reference

| Task | Use | Avoid |
|------|-----|-------|
| File paths | pathlib.Path | os.path strings |
| JSON | json.dumps/loads | eval/str |
| HTTP requests | aiohttp (async), requests (sync) | urllib |
| Data analysis | pandas, numpy | Pure Python loops |
| Testing | pytest | unittest (unless required) |
| Formatting | black | Manual formatting |
| Type checking | mypy | No typing |
| Environment | python-dotenv | Hardcoded values |