# Pattern: Python Function

## Metadata
- **ID**: pattern-code-python-function
- **Version**: 1.0.0
- **Category**: code-generation
- **Difficulty Range**: 3-5 (function implementation tasks)

## Triggers
Keywords that suggest this pattern applies:
- python function
- create function
- implement function
- add function
- def
- method

File types: .py

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| function_name | string | yes | Name of function (snake_case) |
| description | string | yes | What the function does |
| parameters | string | yes | Function parameters with type hints |
| return_type | string | yes | Return type annotation |
| docstring_style | enum | no | google/numpy/sphinx (default: google) |
| include_examples | boolean | no | Include usage examples in docstring (default: false) |
| error_handling | boolean | no | Include try/except blocks (default: true) |

## Pre-Conditions
- [ ] Function name follows snake_case convention
- [ ] Type hints are valid Python 3.9+ syntax
- [ ] Return type is appropriate for function purpose
- [ ] Target file exists (or will be created)

## Template

```python
def {{function_name}}({{parameters}}) -> {{return_type}}:
    """{{description}}

    {{#if docstring_style == 'google'}}
    Args:
        {{parameter_docs}}

    Returns:
        {{return_docs}}

    Raises:
        {{exception_docs}}
    {{/if}}
    {{#if include_examples}}

    Examples:
        >>> {{function_name}}({{example_input}})
        {{example_output}}
    {{/if}}
    """
    {{#if error_handling}}
    try:
        {{function_body}}
    except {{expected_exception}} as e:
        raise {{custom_exception}}(f"{{error_message}}: {e}")
    {{else}}
    {{function_body}}
    {{/if}}
```

## Post-Conditions
- [ ] Function has complete docstring
- [ ] All parameters have type hints
- [ ] Return type specified
- [ ] Error handling appropriate for use case
- [ ] Function follows single responsibility principle
- [ ] Unit tests exist or planned

## Anti-Patterns
**DON'T do this:**
- Missing type hints (makes code harder to maintain)
- No docstring or incomplete docstring
- Too many parameters (>5 suggests refactoring needed)
- Mixed responsibilities (do one thing well)
- Swallowing exceptions without logging
- Returning None when empty list/dict more appropriate
- Mutable default arguments (def func(x=[]):)

**WHY**:
- Type hints enable IDE support and catch bugs early
- Docstrings are essential documentation
- Many parameters indicate poor design
- Mixed responsibilities hard to test and maintain
- Silent failures hide bugs
- None vs empty collection has different semantics
- Mutable defaults share state between calls (common Python gotcha)

## Examples

### Example 1: Simple Calculation Function
**Input:**
```
function_name: calculate_total
description: Calculate total sum from list of numbers with validation
parameters: numbers: list[float]
return_type: float
docstring_style: google
include_examples: false
error_handling: true
```

**Output:**
```python
def calculate_total(numbers: list[float]) -> float:
    """Calculate total sum from list of numbers with validation.

    Args:
        numbers: List of floating point numbers to sum

    Returns:
        Total sum of all numbers

    Raises:
        ValueError: If numbers list is empty
        TypeError: If list contains non-numeric values
    """
    try:
        if not numbers:
            raise ValueError("Cannot calculate total of empty list")
        return sum(numbers)
    except TypeError as e:
        raise TypeError(f"List contains non-numeric values: {e}")
```

### Example 2: Data Processing Function with Examples
**Input:**
```
function_name: parse_user_data
description: Parse and validate user data from JSON string
parameters: json_string: str
return_type: dict[str, Any]
docstring_style: google
include_examples: true
error_handling: true
```

**Output:**
```python
def parse_user_data(json_string: str) -> dict[str, Any]:
    """Parse and validate user data from JSON string.

    Args:
        json_string: JSON formatted string containing user data

    Returns:
        Dictionary with parsed and validated user data

    Raises:
        ValueError: If JSON is invalid or missing required fields
        TypeError: If input is not a string

    Examples:
        >>> parse_user_data('{"name": "John", "age": 30}')
        {'name': 'John', 'age': 30}
    """
    try:
        if not isinstance(json_string, str):
            raise TypeError("Input must be a string")

        data = json.loads(json_string)

        # Validate required fields
        required_fields = ['name', 'age']
        if not all(field in data for field in required_fields):
            raise ValueError(f"Missing required fields: {required_fields}")

        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
```

### Example 3: No Error Handling (Simple Utility)
**Input:**
```
function_name: format_currency
description: Format number as currency string
parameters: amount: float, currency: str = "USD"
return_type: str
docstring_style: google
include_examples: true
error_handling: false
```

**Output:**
```python
def format_currency(amount: float, currency: str = "USD") -> str:
    """Format number as currency string.

    Args:
        amount: Numeric amount to format
        currency: Currency code (default: USD)

    Returns:
        Formatted currency string

    Examples:
        >>> format_currency(1234.56)
        '$1,234.56'
        >>> format_currency(1234.56, 'EUR')
        '€1,234.56'
    """
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"
```

## Usage Notes

### Type Hints Best Practices
- Use `list[T]`, `dict[K, V]` (Python 3.9+)
- For older Python: `from typing import List, Dict`
- Use `Optional[T]` for nullable values
- Use `Union[T1, T2]` for multiple types
- Use `Any` sparingly (defeats purpose of type hints)

### Docstring Guidelines
- First line: Brief description (imperative mood)
- Args: Describe each parameter
- Returns: Describe return value
- Raises: List exceptions that can be raised
- Examples: Show realistic usage

### When to Include Error Handling
- **Include**: File I/O, network calls, user input, external APIs
- **Skip**: Pure functions, simple utilities, internal helpers
- **Consider**: Validation functions, data processing

### Function Complexity
- **Simple (3-4)**: <10 lines, 1-3 parameters, straightforward logic
- **Moderate (4-5)**: 10-30 lines, 3-5 parameters, some branching
- **Complex (5-6)**: >30 lines, >5 parameters → Consider refactoring

## Related Patterns
- `python-class.pattern.md` - For class methods
- `test-file.pattern.md` - For writing tests for this function
- `modify-file.pattern.md` - For adding function to existing file

## Testing Checklist
After creating function, ensure:
- [ ] Unit tests cover happy path
- [ ] Unit tests cover error cases
- [ ] Edge cases tested (empty input, None, etc.)
- [ ] Type hints verified with mypy/pyright
- [ ] Docstring examples are accurate
