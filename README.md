# Payment Processing CLI

A command-line tool built with [Typer](https://typer.tiangolo.com/) and [DuckDB](https://duckdb.org/) to process payment CSV files. It calculates the total gross amount per donor, excluding those marked as not anonymous.

## Features

- Reads a CSV file using DuckDB.
- Filters out records where `Anonymous?` is `False`.
- Aggregates `Gross Amount` by `Full Name`.
- Outputs the result as a JSON list sorted by total gross amount.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (for dependency management)

## Setup

This project uses `uv` for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd commit-change-foundational-supporters
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## Usage

Run the script using `uv run`. You must provide the path to the CSV file as an argument.

```bash
uv run main.py <path-to-csv>
```

### Example

Given a `payments.csv` file:

```bash
uv run main.py payments.csv
```

**Input CSV Format:**

The CSV file must have the following headers:
- `Full Name`: The name of the donor.
- `Gross Amount`: The amount of the donation.
- `Anonymous?`: Boolean value (`True` or `False`).

**Sample `payments.csv`:**

```csv
Full Name,Gross Amount,Anonymous?
John Doe,100.00,True
Jane Smith,50.00,False
John Doe,25.50,True
Anonymous Donor,500.00,True
```

**Output:**

```json
[
  {
    "Full Name": "Anonymous Donor",
    "Total Gross Amount": 500.0
  },
  {
    "Full Name": "John Doe",
    "Total Gross Amount": 125.5
  }
]
```
