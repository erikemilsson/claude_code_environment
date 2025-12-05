# Pattern: Excel Read

## Metadata
- **ID**: pattern-data-excel-read
- **Version**: 1.0.0
- **Category**: data-operations
- **Difficulty Range**: 3-5 (Excel processing tasks)

## Triggers
Keywords that suggest this pattern applies:
- excel
- read excel
- xlsx
- xls
- spreadsheet
- read workbook
- parse excel

File types: .xlsx, .xls, .xlsm, .py (for processing scripts)

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | yes | Path to Excel file |
| sheet_name | string | no | Specific sheet (default: first sheet) |
| header_row | number | no | Row number for headers (default: 0) |
| skip_rows | number | no | Rows to skip from top (default: 0) |
| use_cols | string | no | Columns to read (e.g., "A:D" or [0,1,2,3]) |
| output_format | enum | no | dataframe/dict/list (default: dataframe) |

## Pre-Conditions
- [ ] Excel file exists and is accessible
- [ ] pandas and openpyxl/xlrd libraries installed
- [ ] File is not password protected
- [ ] File is not corrupted
- [ ] Sufficient memory for file size

## Template

### Basic Excel Reading (Pandas)
```python
import pandas as pd
from pathlib import Path
from typing import Union, List


def read_excel_file(
    file_path: str,
    sheet_name: Union[str, int] = 0,
    header_row: int = 0,
    skip_rows: int = 0
) -> pd.DataFrame:
    """Read Excel file and return as DataFrame.

    Args:
        file_path: Path to Excel file
        sheet_name: Sheet name or index (0 for first sheet)
        header_row: Row number to use as column names
        skip_rows: Number of rows to skip from top

    Returns:
        DataFrame with Excel data

    Raises:
        FileNotFoundError: If Excel file doesn't exist
        ValueError: If sheet doesn't exist
    """
    try:
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=header_row,
            skiprows=skip_rows,
            engine='openpyxl'  # For .xlsx files
        )

        # Basic cleaning
        df = df.dropna(how='all')  # Remove completely empty rows
        df.columns = df.columns.str.strip()  # Clean column names

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    except ValueError as e:
        raise ValueError(f"Error reading Excel sheet: {e}")
```

### Reading Multiple Sheets
```python
import pandas as pd
from typing import Dict


def read_excel_all_sheets(
    file_path: str,
    skip_empty: bool = True
) -> Dict[str, pd.DataFrame]:
    """Read all sheets from Excel file.

    Args:
        file_path: Path to Excel file
        skip_empty: Skip empty sheets

    Returns:
        Dictionary mapping sheet names to DataFrames

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path, engine='openpyxl')
        sheets = {}

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(
                excel_file,
                sheet_name=sheet_name
            )

            # Skip empty sheets if requested
            if skip_empty and df.empty:
                continue

            sheets[sheet_name] = df

        return sheets

    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found: {file_path}")
```

### Reading Specific Columns
```python
import pandas as pd
from typing import List, Union


def read_excel_columns(
    file_path: str,
    columns: Union[str, List[int]],
    sheet_name: Union[str, int] = 0
) -> pd.DataFrame:
    """Read specific columns from Excel file.

    Args:
        file_path: Path to Excel file
        columns: Column range (e.g., "A:D") or list of indices
        sheet_name: Sheet name or index

    Returns:
        DataFrame with selected columns

    Examples:
        >>> read_excel_columns("data.xlsx", "A:C")  # Columns A, B, C
        >>> read_excel_columns("data.xlsx", [0, 2, 5])  # Columns 0, 2, 5
    """
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        usecols=columns,
        engine='openpyxl'
    )

    return df
```

### Advanced Reading with Validation
```python
import pandas as pd
from pathlib import Path
from typing import List, Optional


def read_and_validate_excel(
    file_path: str,
    required_columns: List[str],
    sheet_name: Union[str, int] = 0,
    date_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Read Excel file with column validation and type conversion.

    Args:
        file_path: Path to Excel file
        required_columns: Columns that must exist
        sheet_name: Sheet name or index
        date_columns: Columns to convert to datetime

    Returns:
        Validated DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns missing or validation fails
    """
    # Read Excel
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        engine='openpyxl'
    )

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Validate required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Convert date columns
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

    # Remove completely empty rows
    df = df.dropna(how='all')

    return df
```

## Post-Conditions
- [ ] Data successfully loaded into DataFrame or desired format
- [ ] Column names clean and accessible
- [ ] Empty rows removed (if specified)
- [ ] Data types correct (especially dates)
- [ ] Required columns present
- [ ] No corrupted data

## Anti-Patterns
**DON'T do this:**
- Assume first row is always headers
- Ignore empty rows/columns (clean them)
- Use Excel formulas as data (formulas don't transfer)
- Hardcode sheet names (they change)
- Load entire large Excel file into memory
- Skip type validation (Excel types are unreliable)
- Use Excel for large datasets (>100K rows, use CSV/database)
- Modify original Excel file without backup

**WHY**:
- Excel structures vary widely
- Empty rows break data processing
- Formulas evaluate to values only
- Sheet names not guaranteed
- Large files cause memory errors
- Excel stores dates/numbers inconsistently
- Excel not designed for big data
- Original data should be preserved

## Examples

### Example 1: Read Sales Data
**Input:**
```
file_path: data/sales_2024.xlsx
sheet_name: Q4 Sales
header_row: 0
skip_rows: 2
use_cols: A:F
output_format: dataframe
```

**Output:**
```python
import pandas as pd


def read_sales_data(
    file_path: str = "data/sales_2024.xlsx",
    sheet_name: str = "Q4 Sales"
) -> pd.DataFrame:
    """Read quarterly sales data from Excel.

    Args:
        file_path: Path to sales Excel file
        sheet_name: Sheet containing Q4 data

    Returns:
        Clean sales DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns missing
    """
    # Read Excel with specific configuration
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=0,
        skiprows=2,  # Skip title rows
        usecols="A:F",  # Only first 6 columns
        engine='openpyxl'
    )

    # Clean column names
    df.columns = ['date', 'product', 'quantity', 'unit_price', 'total', 'region']

    # Data type conversions
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df['total'] = pd.to_numeric(df['total'], errors='coerce')

    # Remove invalid rows
    df = df.dropna(subset=['date', 'product'])

    # Validation
    if len(df) == 0:
        raise ValueError("No valid data found in Excel file")

    print(f"Loaded {len(df)} sales records")
    return df


# Usage
df = read_sales_data()
print(df.head())
print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
```

### Example 2: Read Multiple Sheets with Aggregation
**Input:**
```
file_path: reports/monthly_data.xlsx
```

**Output:**
```python
import pandas as pd
from typing import Dict


def read_monthly_reports(
    file_path: str = "reports/monthly_data.xlsx"
) -> pd.DataFrame:
    """Read and combine monthly data from multiple sheets.

    Args:
        file_path: Path to Excel file with monthly sheets

    Returns:
        Combined DataFrame with all months

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Read all sheets
    excel_file = pd.ExcelFile(file_path, engine='openpyxl')

    all_data = []
    for sheet_name in excel_file.sheet_names:
        # Skip summary or non-data sheets
        if 'summary' in sheet_name.lower():
            continue

        # Read sheet
        df = pd.read_excel(
            excel_file,
            sheet_name=sheet_name
        )

        # Add month identifier
        df['month'] = sheet_name

        all_data.append(df)

    # Combine all sheets
    combined = pd.concat(all_data, ignore_index=True)

    print(f"Loaded data from {len(all_data)} sheets")
    print(f"Total records: {len(combined)}")

    return combined


# Usage
df = read_monthly_reports()
monthly_summary = df.groupby('month')['total'].sum()
print("\nMonthly totals:")
print(monthly_summary)
```

### Example 3: Excel with Data Validation
**Input:**
```
file_path: imports/customer_data.xlsx
required_columns: name, email, phone, registration_date
```

**Output:**
```python
import pandas as pd
from typing import List
import re


def read_customer_data(
    file_path: str = "imports/customer_data.xlsx",
    sheet_name: str = "Customers"
) -> pd.DataFrame:
    """Read and validate customer data from Excel.

    Args:
        file_path: Path to customer Excel file
        sheet_name: Sheet containing customer data

    Returns:
        Validated customer DataFrame

    Raises:
        ValueError: If validation fails
    """
    # Read Excel
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        engine='openpyxl'
    )

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Validate required columns
    required = ['name', 'email', 'phone', 'registration_date']
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Data type conversions
    df['registration_date'] = pd.to_datetime(
        df['registration_date'],
        errors='coerce'
    )

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    df['email_valid'] = df['email'].astype(str).str.match(email_pattern)

    # Validate phone format (10+ digits)
    df['phone'] = df['phone'].astype(str).str.replace(r'\D', '', regex=True)
    df['phone_valid'] = df['phone'].str.len() >= 10

    # Filter to valid records
    valid_df = df[
        df['name'].notna() &
        df['email_valid'] &
        df['phone_valid'] &
        df['registration_date'].notna()
    ].copy()

    # Drop validation columns
    valid_df = valid_df.drop(columns=['email_valid', 'phone_valid'])

    # Report validation results
    invalid_count = len(df) - len(valid_df)
    if invalid_count > 0:
        print(f"Warning: Removed {invalid_count} invalid records")

    print(f"Validated {len(valid_df)} customer records")

    return valid_df


# Usage
df = read_customer_data()
print(df.head())
```

## Usage Notes

### Engine Selection
- **openpyxl**: For .xlsx files (Excel 2010+) - Recommended
- **xlrd**: For .xls files (Excel 2003 and earlier)
- **pyxlsb**: For .xlsb files (binary Excel)

```python
# Install required engine
# pip install openpyxl  # For .xlsx
# pip install xlrd       # For .xls
```

### Memory Optimization for Large Files
```python
# Read in chunks
chunk_size = 10000
chunks = pd.read_excel(
    file,
    sheet_name=0,
    chunksize=chunk_size,
    engine='openpyxl'
)
for chunk in chunks:
    process(chunk)
```

### Date Handling
Excel dates can be tricky:
```python
# Explicit date parsing
df['date'] = pd.to_datetime(
    df['date'],
    format='%Y-%m-%d',  # Specify format if known
    errors='coerce'     # Convert errors to NaT
)
```

### Writing Excel
```python
# Write single sheet
df.to_excel('output.xlsx', index=False, sheet_name='Data')

# Write multiple sheets
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df1.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)
```

## Common Issues and Solutions

### Issue: "Excel file format cannot be determined"
```python
# Solution: Specify engine explicitly
df = pd.read_excel(file, engine='openpyxl')
```

### Issue: Dates appear as numbers
```python
# Solution: Convert Excel serial dates
df['date'] = pd.to_datetime(df['date'], unit='D', origin='1899-12-30')
```

### Issue: Leading zeros lost (e.g., ZIP codes)
```python
# Solution: Read as string
df = pd.read_excel(file, dtype={'zip_code': str})
```

### Issue: Merged cells cause NaN
```python
# Solution: Forward fill merged cells
df['column'] = df['column'].fillna(method='ffill')
```

## Related Patterns
- `csv-transform.pattern.md` - For Excel to CSV conversion
- `json-parse.pattern.md` - For Excel to JSON conversion
- `python-function.pattern.md` - For Excel processing functions
