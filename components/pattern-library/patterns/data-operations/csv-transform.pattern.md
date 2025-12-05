# Pattern: CSV Transform

## Metadata
- **ID**: pattern-data-csv-transform
- **Version**: 1.0.0
- **Category**: data-operations
- **Difficulty Range**: 3-5 (CSV processing tasks)

## Triggers
Keywords that suggest this pattern applies:
- csv
- transform csv
- process csv
- read csv
- parse csv
- csv to json
- clean csv data

File types: .csv, .py (for processing scripts)

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| input_file | string | yes | Path to input CSV file |
| output_file | string | no | Path to output file (default: processed_{input}) |
| transformations | string | yes | List of transformations to apply |
| encoding | string | no | File encoding (default: utf-8) |
| delimiter | string | no | CSV delimiter (default: ,) |
| has_header | boolean | no | First row is header (default: true) |
| handle_missing | enum | no | skip/fill/error (default: skip) |

## Pre-Conditions
- [ ] Input CSV file exists and is accessible
- [ ] CSV is well-formed (consistent columns)
- [ ] Output directory exists
- [ ] pandas library installed (if using pandas)
- [ ] Sufficient memory for file size

## Template

### Using Pandas (Recommended for Large Files)
```python
import pandas as pd
from pathlib import Path


def transform_csv(
    input_file: str,
    output_file: str = None,
    encoding: str = "utf-8",
    delimiter: str = ","
) -> pd.DataFrame:
    """Transform CSV file with specified operations.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output file (default: processed_{input})
        encoding: File encoding
        delimiter: CSV delimiter character

    Returns:
        Transformed DataFrame

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If CSV is malformed
    """
    try:
        # Read CSV
        df = pd.read_csv(
            input_file,
            encoding=encoding,
            delimiter=delimiter,
            {{#if !has_header}}
            header=None,
            {{/if}}
        )

        # Validate
        if df.empty:
            raise ValueError("CSV file is empty")

        # Apply transformations
        {{transformations_code}}

        # Save if output specified
        if output_file:
            df.to_csv(output_file, index=False, encoding=encoding)

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing error: {e}")
```

### Using CSV Module (For Simple Cases)
```python
import csv
from typing import List, Dict


def transform_csv(
    input_file: str,
    output_file: str = None,
    encoding: str = "utf-8",
    delimiter: str = ","
) -> List[Dict[str, str]]:
    """Transform CSV file with specified operations.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output file
        encoding: File encoding
        delimiter: CSV delimiter

    Returns:
        List of dictionaries (one per row)

    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    try:
        # Read CSV
        rows = []
        with open(input_file, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            rows = list(reader)

        # Apply transformations
        {{transformations_code}}

        # Save if output specified
        if output_file and rows:
            with open(output_file, 'w', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=delimiter)
                writer.writeheader()
                writer.writerows(rows)

        return rows

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
```

## Post-Conditions
- [ ] Output file created (if specified)
- [ ] All transformations applied correctly
- [ ] No data loss (unless intentional filtering)
- [ ] Output encoding matches specification
- [ ] Column names preserved or updated as intended

## Anti-Patterns
**DON'T do this:**
- Load entire large CSV into memory without chunking
- Assume encoding is UTF-8 (check file first)
- Ignore malformed rows (handle gracefully)
- Modify original file (always write to new file)
- Skip validation of transformation results
- Hardcode column names (CSV structure may vary)
- Forget to close file handles (use context managers)

**WHY**:
- Large files cause memory errors
- Encoding issues corrupt data
- Malformed rows break processing
- Original data should be preserved
- Silent failures hide bugs
- Hardcoded names break on schema changes
- Unclosed files cause resource leaks

## Examples

### Example 1: Clean and Filter Data
**Input:**
```
input_file: data/sales.csv
output_file: data/sales_clean.csv
transformations: |
  - Remove rows with missing values
  - Convert date column to datetime
  - Filter for sales > 100
  - Add calculated column: profit_margin
encoding: utf-8
delimiter: ,
has_header: true
handle_missing: skip
```

**Output:**
```python
import pandas as pd
from pathlib import Path


def transform_csv(
    input_file: str = "data/sales.csv",
    output_file: str = "data/sales_clean.csv",
    encoding: str = "utf-8",
    delimiter: str = ","
) -> pd.DataFrame:
    """Transform sales CSV: clean, filter, and calculate metrics.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output file
        encoding: File encoding
        delimiter: CSV delimiter

    Returns:
        Transformed DataFrame

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If CSV is malformed or required columns missing
    """
    try:
        # Read CSV
        df = pd.read_csv(input_file, encoding=encoding, delimiter=delimiter)

        # Validate required columns
        required_cols = ['date', 'sales', 'cost']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")

        # Remove rows with missing values
        df = df.dropna()

        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Filter for sales > 100
        df = df[df['sales'] > 100]

        # Add calculated column: profit_margin
        df['profit_margin'] = (df['sales'] - df['cost']) / df['sales'] * 100

        # Save
        df.to_csv(output_file, index=False, encoding=encoding)

        print(f"Processed {len(df)} rows")
        print(f"Output saved to: {output_file}")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing error: {e}")


if __name__ == "__main__":
    df = transform_csv()
    print(df.head())
```

### Example 2: Aggregate and Group
**Input:**
```
input_file: data/transactions.csv
output_file: data/transactions_summary.csv
transformations: |
  - Group by customer_id
  - Sum total_amount per customer
  - Count transactions per customer
  - Calculate average transaction value
encoding: utf-8
delimiter: ,
```

**Output:**
```python
import pandas as pd


def transform_csv(
    input_file: str = "data/transactions.csv",
    output_file: str = "data/transactions_summary.csv",
    encoding: str = "utf-8",
    delimiter: str = ","
) -> pd.DataFrame:
    """Aggregate transaction data by customer.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output summary file
        encoding: File encoding
        delimiter: CSV delimiter

    Returns:
        Aggregated DataFrame
    """
    # Read CSV
    df = pd.read_csv(input_file, encoding=encoding, delimiter=delimiter)

    # Group by customer_id and aggregate
    summary = df.groupby('customer_id').agg({
        'total_amount': ['sum', 'count', 'mean']
    }).reset_index()

    # Flatten column names
    summary.columns = [
        'customer_id',
        'total_spent',
        'transaction_count',
        'avg_transaction_value'
    ]

    # Round decimals
    summary['total_spent'] = summary['total_spent'].round(2)
    summary['avg_transaction_value'] = summary['avg_transaction_value'].round(2)

    # Save
    summary.to_csv(output_file, index=False, encoding=encoding)

    return summary


if __name__ == "__main__":
    summary = transform_csv()
    print(f"Summarized {len(summary)} customers")
    print(summary.head())
```

### Example 3: Data Type Conversion and Validation
**Input:**
```
input_file: data/users.csv
output_file: data/users_validated.csv
transformations: |
  - Convert age to integer
  - Validate email format
  - Standardize phone numbers
  - Remove invalid records
encoding: utf-8
```

**Output:**
```python
import pandas as pd
import re


def transform_csv(
    input_file: str = "data/users.csv",
    output_file: str = "data/users_validated.csv",
    encoding: str = "utf-8",
    delimiter: str = ","
) -> pd.DataFrame:
    """Validate and clean user data.

    Args:
        input_file: Path to input CSV
        output_file: Path to validated output
        encoding: File encoding
        delimiter: CSV delimiter

    Returns:
        Validated DataFrame
    """
    # Read CSV
    df = pd.read_csv(input_file, encoding=encoding, delimiter=delimiter)

    original_count = len(df)

    # Convert age to integer (coerce errors to NaN)
    df['age'] = pd.to_numeric(df['age'], errors='coerce').astype('Int64')

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    df['email_valid'] = df['email'].str.match(email_pattern, na=False)

    # Standardize phone numbers (remove non-digits)
    df['phone'] = df['phone'].str.replace(r'\D', '', regex=True)

    # Remove invalid records
    df = df[
        df['age'].notna() &
        df['email_valid'] &
        (df['phone'].str.len() >= 10)
    ]

    # Drop validation column
    df = df.drop(columns=['email_valid'])

    # Save
    df.to_csv(output_file, index=False, encoding=encoding)

    removed_count = original_count - len(df)
    print(f"Removed {removed_count} invalid records")
    print(f"Kept {len(df)} valid records")

    return df


if __name__ == "__main__":
    df = transform_csv()
    print(df.head())
```

## Usage Notes

### Memory Considerations
For large files (>100MB), use chunking:
```python
chunk_size = 10000
chunks = []
for chunk in pd.read_csv(file, chunksize=chunk_size):
    processed = process_chunk(chunk)
    chunks.append(processed)
df = pd.concat(chunks)
```

### Encoding Detection
If encoding unknown:
```python
import chardet

with open(file, 'rb') as f:
    result = chardet.detect(f.read(10000))
    encoding = result['encoding']
```

### Common Transformations
- **Remove duplicates**: `df.drop_duplicates()`
- **Fill missing**: `df.fillna(value)`
- **Rename columns**: `df.rename(columns={'old': 'new'})`
- **Filter rows**: `df[df['column'] > value]`
- **Sort**: `df.sort_values('column')`

## Error Handling Best Practices
```python
try:
    df = pd.read_csv(file)
except FileNotFoundError:
    # Handle missing file
except pd.errors.ParserError:
    # Handle malformed CSV
except UnicodeDecodeError:
    # Handle encoding issues
```

## Related Patterns
- `json-parse.pattern.md` - For JSON output
- `excel-read.pattern.md` - For Excel input/output
- `python-function.pattern.md` - For transformation functions
