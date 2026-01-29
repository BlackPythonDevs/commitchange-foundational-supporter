import typer
import duckdb
import json
import sys
from collections import defaultdict


def main(
    file_path: str = typer.Argument(..., help="Path to the payments.csv file"),
    allow_anonymous: bool = typer.Argument(
        default=False, help="Should you include or exclude donors listed anonymous"
    ),
    limit: int = typer.Argument(
        default=200, help="The minimum gross amount to include"
    ),
) -> None:
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
                YEAR(Date) as Year,
                "Full Name"
            FROM read_csv_auto('{file_path}')
            WHERE "Anonymous?" = {allow_anonymous} and "Full Name" NOT Null
            GROUP BY YEAR(Date), "Full Name"
            HAVING SUM(CAST(REPLACE(REPLACE("Gross Amount", '$', ''), ',', '') AS DECIMAL(10, 2))) > {limit}
            ORDER BY Year DESC, "Full Name" ASC
        """

        # Execute and fetch as a list of tuples
        result = con.execute(query).fetchall()

        # Group by Year
        grouped_output = defaultdict(list)
        for year, name in result:
            grouped_output[str(year)].append(name)

        # Print JSON to stdout
        print(json.dumps(grouped_output, indent=2))

    except Exception as e:
        typer.echo(f"Error processing file: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)
