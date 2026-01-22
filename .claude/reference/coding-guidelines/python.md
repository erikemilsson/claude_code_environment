# Python Guidelines

*Language-specific patterns - see core.md for shared principles.*

## Import Organization
```python
# Standard library
import os
from pathlib import Path
from typing import List, Dict, Optional

# Third-party
import pandas as pd

# Local
from myapp.core import utils
```

## Type Hints
```python
def process_data(
    input_file: Path,
    output_format: str = "json",
    validate: bool = True
) -> Dict[str, Any]:
    """Process input data and return formatted results."""
```

## Pythonic Patterns
```python
# List comprehensions for simple transforms
squared = [x**2 for x in numbers if x > 0]

# Context managers for resources
with open("data.txt") as f:
    content = f.read()

# Dataclasses for configuration
@dataclass
class Config:
    database_url: str
    debug: bool = False
```

## Pandas Best Practices
```python
# Vectorized operations (not iterrows)
df["total"] = df["price"] * df["quantity"]

# Method chaining
result = (df
    .dropna(subset=["key_column"])
    .groupby("category")
    .agg({"value": "sum"})
    .reset_index())
```

## Common Pitfalls
```python
# BAD: Mutable default argument
def append(item, target=[]):  # Creates shared list!

# GOOD: None with check
def append(item, target=None):
    if target is None:
        target = []
```

## Quick Reference

| Task | Use | Avoid |
|------|-----|-------|
| File paths | pathlib.Path | os.path strings |
| JSON | json.dumps/loads | eval/str |
| HTTP | aiohttp (async), requests (sync) | urllib |
| Testing | pytest | unittest (unless required) |
| Formatting | black | Manual formatting |
