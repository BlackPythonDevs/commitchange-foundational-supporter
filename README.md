# Foundational Supporters Web App

A web application built with [FastAPI](https://fastapi.tiangolo.com/) and [DuckDB](https://duckdb.org/) to process payment CSV files. It calculates the total gross amount per donor and presents the data either grouped by year or as a lifetime total.

## Features

- **Web Interface:** Drag-and-drop file upload for processing `payments.csv` files.
- **Two Processing Modes:**
  - **Annual**: Aggregates by `Year` and `Full Name`.
  - **Lifetime**: Aggregates total gross amounts for the donor's entire lifetime.
- **Minimum Contribution Filter:** Excludes records based on a minimum gross amount (Defaults to $200).
- **JSON Output:** Renders the result as formatted JSON with a one-click "Copy to Clipboard" feature.

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

Start the web server using `uv run`.

```bash
uv run main.py
```

This will start the FastAPI application on `http://127.0.0.1:8080`.

**Using the Web Interface:**

1. Navigate to `http://127.0.0.1:8080` in your web browser.
2. Select your view type: **Annual Supporters** or **Lifetime Supporters**.
3. Set your **Minimum Contribution** (defaults to `200`).
4. Drag and drop your `payments.csv` file into the upload zone (or click to browse).
5. The processed results will immediately be displayed on the page as JSON.

**Sample `payments.csv` Format:**

```csv
Date,Full Name,Gross Amount,Anonymous?
2023-01-01,John Doe,$100.00,True
2023-01-02,Jane Smith,$50.00,False
2023-01-03,John Doe,$25.50,True
2023-01-04,Anonymous Donor,$500.00,True
2023-01-05,Bob Jones,$75.00,False
2023-01-06,Alice Brown,$200.00,True
```

**Sample Output (Annual Mode):**

```json
{
  "2023": [
    "Alice Brown",
    "Anonymous Donor",
    "John Doe"
  ]
}
```

**Sample Output (Lifetime Mode):**

```json
[
  "Alice Brown",
  "Anonymous Donor",
  "John Doe"
]
```