```markdown
# Module Design: analyst.py

## Class: Analyst

This class encapsulates functionality to analyze CSV data files, providing size, data types, missing values count, and summary statistics for numeric and categorical columns.

---

### Initialization

```python
def __init__(self) -> None
```

- Initializes the Analyst instance.
- Sets up any internal state needed to hold the data after loading.

---

### Method: upload_csv

```python
def upload_csv(self, file_path: str) -> None
```

- Reads data from a CSV file located at `file_path`.
- Stores the data internally for subsequent analysis.
- Should handle file reading errors with appropriate exceptions.
- Uses standard CSV reading capabilities (e.g., pandas internally) to load data.

---

### Method: get_data_size

```python
def get_data_size(self) -> tuple[int, int]
```

- Returns the size of the current data.
- Output is a tuple: `(number_of_rows, number_of_columns)`.

---

### Method: get_column_data_types

```python
def get_column_data_types(self) -> dict[str, str]
```

- Returns a dictionary mapping each column name to its data type as a string.
- Data types should reflect the nature of the data (e.g., "int64", "float64", "object" for strings).

---

### Method: get_missing_values_count

```python
def get_missing_values_count(self) -> dict[str, int]
```

- Returns a dictionary mapping each column name to the count of missing/null values in that column.

---

### Method: get_numeric_column_stats

```python
def get_numeric_column_stats(self) -> dict[str, dict[str, float]]
```

- For every numeric column, returns a nested dictionary:
  - Outer dict key: column name (string)
  - Inner dict keys and values:
    - `"mean"`: mean of the column
    - `"median"`: median value
    - `"mode"`: mode value (single most frequent; if multiple modes, return any one)
    - `"std_dev"`: standard deviation
    - `"range"`: difference between max and min values

---

### Method: get_categorical_column_stats

```python
def get_categorical_column_stats(self) -> dict[str, dict[str, int | str]]
```

- For every categorical (non-numeric) column, returns a nested dictionary:
  - Outer dict key: column name (string)
  - Inner dict keys and values:
    - `"mode"`: mode value (most frequent category)
    - `"unique_values"`: count of unique values in the column

---

# Summary of the class interface for clarity:

```python
class Analyst:
    def __init__(self) -> None:
        pass

    def upload_csv(self, file_path: str) -> None:
        pass

    def get_data_size(self) -> tuple[int, int]:
        pass

    def get_column_data_types(self) -> dict[str, str]:
        pass

    def get_missing_values_count(self) -> dict[str, int]:
        pass

    def get_numeric_column_stats(self) -> dict[str, dict[str, float]]:
        pass

    def get_categorical_column_stats(self) -> dict[str, dict[str, int | str]]:
        pass
```

---

# Notes for the engineer:

- Use standard libraries such as `pandas` to handle CSV reading and data processing efficiently.
- Ensure proper error handling for file operations and data processing.
- The mode function should handle the cases where multiple values have the same highest count; returning one is acceptable.
- The class should keep the loaded dataset in memory until a new file is uploaded.
- The output types and formats are fixed as described to enable easy future UI integration or automated testing.

---
```