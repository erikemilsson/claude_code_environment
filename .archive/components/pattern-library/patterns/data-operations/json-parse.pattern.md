# Pattern: JSON Parse

## Metadata
- **ID**: pattern-data-json-parse
- **Version**: 1.0.0
- **Category**: data-operations
- **Difficulty Range**: 2-4 (JSON processing tasks)

## Triggers
Keywords that suggest this pattern applies:
- json
- parse json
- read json
- json file
- json config
- json api
- validate json

File types: .json, .py (for processing scripts)

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_type | enum | yes | file/string/url |
| source_path | string | conditional | Required for file/url types |
| json_string | string | conditional | Required for string type |
| validation_schema | string | no | JSON schema for validation |
| encoding | string | no | File encoding (default: utf-8) |
| handle_errors | enum | no | raise/default/none (default: raise) |

## Pre-Conditions
- [ ] JSON source is accessible (file exists, URL reachable, or string provided)
- [ ] JSON is well-formed
- [ ] Schema file exists (if validation specified)
- [ ] Required libraries installed (json standard lib, jsonschema if validating)

## Template

### Basic JSON File Reading
```python
import json
from pathlib import Path
from typing import Any, Dict


def parse_json(
    file_path: str,
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """Parse JSON file and return as dictionary.

    Args:
        file_path: Path to JSON file
        encoding: File encoding

    Returns:
        Parsed JSON as dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        JSONDecodeError: If JSON is malformed
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {file_path}: {e.msg}",
            e.doc,
            e.pos
        )
```

### JSON String Parsing
```python
import json
from typing import Any, Dict, Optional


def parse_json_string(
    json_string: str,
    default: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Parse JSON string with error handling.

    Args:
        json_string: JSON formatted string
        default: Default value if parsing fails (if None, raises error)

    Returns:
        Parsed JSON as dictionary

    Raises:
        JSONDecodeError: If JSON is malformed and no default provided
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        if default is not None:
            return default
        raise ValueError(f"Invalid JSON string: {e.msg}") from e
```

### JSON with Schema Validation
```python
import json
from pathlib import Path
from typing import Any, Dict

try:
    from jsonschema import validate, ValidationError
except ImportError:
    raise ImportError("jsonschema required: pip install jsonschema")


def parse_and_validate_json(
    file_path: str,
    schema_path: str,
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """Parse JSON file and validate against schema.

    Args:
        file_path: Path to JSON data file
        schema_path: Path to JSON schema file
        encoding: File encoding

    Returns:
        Validated JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        JSONDecodeError: If JSON is malformed
        ValidationError: If data doesn't match schema
    """
    # Load JSON data
    with open(file_path, 'r', encoding=encoding) as f:
        data = json.load(f)

    # Load schema
    with open(schema_path, 'r', encoding=encoding) as f:
        schema = json.load(f)

    # Validate
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValidationError(f"JSON validation failed: {e.message}")

    return data
```

### JSON from URL
```python
import json
from typing import Any, Dict
import urllib.request


def parse_json_from_url(
    url: str,
    timeout: int = 10
) -> Dict[str, Any]:
    """Fetch and parse JSON from URL.

    Args:
        url: URL to JSON endpoint
        timeout: Request timeout in seconds

    Returns:
        Parsed JSON data

    Raises:
        urllib.error.URLError: If URL is unreachable
        JSONDecodeError: If response is not valid JSON
    """
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data
    except urllib.error.URLError as e:
        raise urllib.error.URLError(f"Failed to fetch JSON from {url}: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from {url}: {e.msg}")
```

## Post-Conditions
- [ ] JSON successfully parsed into Python data structure
- [ ] Data validated against schema (if validation enabled)
- [ ] Errors handled gracefully
- [ ] Data types correctly preserved (str, int, float, bool, list, dict, null)

## Anti-Patterns
**DON'T do this:**
- Use eval() to parse JSON (security risk!)
- Assume JSON is always valid (always handle errors)
- Load huge JSON files into memory (use streaming for large files)
- Modify JSON without validation
- Hardcode field names without checking existence
- Ignore encoding (can corrupt special characters)
- Return None on error without logging
- Parse JSON repeatedly (cache if possible)

**WHY**:
- eval() executes arbitrary code (major security hole)
- Invalid JSON breaks application
- Large files cause memory errors
- Invalid modifications corrupt data
- Hardcoded fields break when schema changes
- Encoding issues corrupt data silently
- None masks problems, makes debugging hard
- Repeated parsing wastes resources

## Examples

### Example 1: Configuration File
**Input:**
```
source_type: file
source_path: config/settings.json
validation_schema: config/settings.schema.json
encoding: utf-8
handle_errors: raise
```

**Output:**
```python
import json
from pathlib import Path
from typing import Any, Dict
from jsonschema import validate, ValidationError


def load_config(
    config_path: str = "config/settings.json",
    schema_path: str = "config/settings.schema.json"
) -> Dict[str, Any]:
    """Load and validate application configuration.

    Args:
        config_path: Path to configuration JSON file
        schema_path: Path to JSON schema for validation

    Returns:
        Validated configuration dictionary

    Raises:
        FileNotFoundError: If configuration file doesn't exist
        ValidationError: If configuration is invalid
    """
    # Load configuration
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Load schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    # Validate
    validate(instance=config, schema=schema)

    return config


# Usage
try:
    config = load_config()
    print(f"Loaded config for environment: {config.get('environment')}")
except ValidationError as e:
    print(f"Configuration error: {e.message}")
    raise
```

### Example 2: API Response Parsing
**Input:**
```
source_type: string
json_string: from API response
handle_errors: default
```

**Output:**
```python
import json
from typing import Any, Dict, List, Optional


def parse_api_response(
    response_text: str,
    expected_structure: Optional[str] = None
) -> Dict[str, Any]:
    """Parse JSON API response with robust error handling.

    Args:
        response_text: JSON string from API
        expected_structure: Expected top-level key (e.g., 'data', 'results')

    Returns:
        Parsed response data

    Raises:
        ValueError: If JSON is invalid or structure unexpected
    """
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e.msg}")

    # Verify expected structure
    if expected_structure and expected_structure not in data:
        raise ValueError(f"Expected key '{expected_structure}' not found in response")

    return data


# Example usage
response_text = '''
{
    "status": "success",
    "data": {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }
}
'''

data = parse_api_response(response_text, expected_structure="data")
users = data["data"]["users"]
print(f"Found {len(users)} users")
```

### Example 3: Nested JSON Extraction
**Input:**
```
source_type: file
source_path: data/complex.json
```

**Output:**
```python
import json
from typing import Any, Dict, List


def extract_nested_data(
    file_path: str,
    path: List[str]
) -> Any:
    """Extract nested data from JSON using dot notation path.

    Args:
        file_path: Path to JSON file
        path: List of keys to navigate (e.g., ['data', 'users', 0, 'name'])

    Returns:
        Value at specified path

    Raises:
        FileNotFoundError: If file doesn't exist
        KeyError: If path doesn't exist in JSON
        IndexError: If array index out of range
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Navigate through path
    current = data
    for key in path:
        if isinstance(current, dict):
            current = current[key]
        elif isinstance(current, list):
            current = current[int(key)]
        else:
            raise TypeError(f"Cannot navigate through {type(current)}")

    return current


# Example usage
# JSON: {"data": {"users": [{"name": "Alice", "age": 30}]}}
name = extract_nested_data(
    "data/complex.json",
    ["data", "users", "0", "name"]
)
print(f"Extracted name: {name}")  # "Alice"
```

### Example 4: JSON Array Processing
**Input:**
```
source_type: file
source_path: data/items.json
```

**Output:**
```python
import json
from typing import Any, Dict, List, Callable


def process_json_array(
    file_path: str,
    filter_func: Callable[[Dict[str, Any]], bool] = None,
    transform_func: Callable[[Dict[str, Any]], Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Process JSON array with filtering and transformation.

    Args:
        file_path: Path to JSON file containing array
        filter_func: Optional function to filter items
        transform_func: Optional function to transform items

    Returns:
        Processed array

    Raises:
        ValueError: If JSON doesn't contain an array
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure data is array
    if not isinstance(data, list):
        raise ValueError("JSON file must contain an array at root level")

    # Apply filter
    if filter_func:
        data = [item for item in data if filter_func(item)]

    # Apply transformation
    if transform_func:
        data = [transform_func(item) for item in data]

    return data


# Example usage
def is_active(item: Dict[str, Any]) -> bool:
    return item.get('status') == 'active'

def add_full_name(item: Dict[str, Any]) -> Dict[str, Any]:
    item['full_name'] = f"{item['first_name']} {item['last_name']}"
    return item

items = process_json_array(
    "data/users.json",
    filter_func=is_active,
    transform_func=add_full_name
)
print(f"Processed {len(items)} active users")
```

## Usage Notes

### Pretty Printing
```python
print(json.dumps(data, indent=2, sort_keys=True))
```

### Writing JSON
```python
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

### Handling Special Types
```python
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps(data, cls=DateTimeEncoder)
```

### Streaming Large JSON
For large JSON files:
```python
import ijson  # pip install ijson

with open('large.json', 'rb') as f:
    parser = ijson.items(f, 'items.item')
    for item in parser:
        process(item)  # Process one at a time
```

## Common Validations
```python
# Check required fields
required = ['id', 'name', 'email']
if not all(k in data for k in required):
    raise ValueError(f"Missing required fields: {required}")

# Type checking
if not isinstance(data.get('age'), int):
    raise TypeError("age must be integer")

# Value constraints
if data.get('age', 0) < 0:
    raise ValueError("age must be non-negative")
```

## Related Patterns
- `csv-transform.pattern.md` - For CSV to JSON conversion
- `python-function.pattern.md` - For JSON processing functions
- API integration patterns
