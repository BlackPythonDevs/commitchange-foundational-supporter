import typer
import duckdb
import json
import sys


def main(
    file_path: str = typer.Argument(..., help="Path to the payments.csv file"),
    allow_anonymous: bool = typer.Argument(
        default=False, help="Should you include or exclude donors listed anonymous"
    ),
):
    """
    Process payments.csv to sum gross amounts by donor name,
    excluding those with 'Anonymous?' = False.
    """
    try:
        # Connect to an in-memory database
        con = duckdb.connect(database=":memory:")

        # We use read_csv_auto to load the file.
        # We select Donor Name and sum Gross Amount.
        # We filter where "Anonymous?" is not False.
        # Note: duckdb usually interprets 'True'/'False' strings as booleans in read_csv_auto.
        # If it doesn't, we might need to adjust the where clause.

        query = f"""
            SELECT 
                "Full Name", 
                SUM(CAST(REPLACE(REPLACE("Gross Amount", '$', ''), ',', '') AS DECIMAL(10, 2))) AS "Total Gross Amount"
            FROM read_csv_auto('{file_path}')
            WHERE "Anonymous?" = false
            GROUP BY "Full Name"
            ORDER BY "Total Gross Amount" DESC
        """

        # Execute and fetch as a dictionary/JSON compatible format
        # duckdb.sql().df() or .fetchall() could work, but let's try to get a list of dicts directly if possible,
        # or construct it.

        result = con.execute(query).fetchdf()

        # Convert to dictionary records
        json_output = result.to_dict(orient="records")

        # Print JSON to stdout
        print(json.dumps(json_output, indent=2))

    except Exception as e:
        typer.echo(f"Error processing file: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)
