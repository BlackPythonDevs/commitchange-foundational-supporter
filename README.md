# Payment Processing CLI

A command-line tool built with [Typer](https://typer.tiangolo.com/) and [DuckDB](https://duckdb.org/) to process payment CSV files. It calculates the total gross amount per donor, excluding those marked as not anonymous.

## Features

- Reads a CSV file using DuckDB.
- Aggregates by `Year` and `Full Name`.
- Filters records based on anonymous status (Defaults to showing non-anonymous donors).
- Filters records based on a minimum gross amount (Defaults to 200).
- Outputs the result as a JSON dictionary grouped by year.

## Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (for dependency management)

## Setup

This project uses `uv` for dependency management.

1.  **Clone the repository:**
    ```bash
    gh repo clone blackpythondevs/commitchange-foundational-supporters
    cd commitchange-foundational-supporters
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## Usage

Run the script using `uv run`.

```bash
uv run main.py <file_path> [allow_anonymous] [limit]
```

**Arguments:**

*   `file_path`: Path to the payments CSV file.
*   `allow_anonymous` (Optional): Set to `True` to show *only* anonymous donors, or `False` (default) to show *only* public donors.
*   `limit` (Optional): The minimum total gross amount required for a donor to be included in the report. Defaults to `200`.

### Example

Given a `test_payments.csv` file:

```bash
uv run main.py test_payments.csv True 0
```

**Sample `payments.csv`:**

```csv
Date,Full Name,Gross Amount,Anonymous?
2023-01-01,John Doe,$100.00,True
2023-01-02,Jane Smith,$50.00,False
2023-01-03,John Doe,$25.50,True
2023-01-04,Anonymous Donor,$500.00,True
2023-01-05,Bob Jones,$75.00,False
2023-01-06,Alice Brown,$200.00,True
```

**Output:**

```json
{
  "2023": [
    "Alice Brown",
    "Anonymous Donor",
    "John Doe"
  ]
}
```
