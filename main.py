import json
import tempfile
import os
from collections import defaultdict

from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import duckdb

app = FastAPI(title="Foundational Supporters")
templates = Jinja2Templates(directory="templates")


def process_annual(
    file_path: str, allow_anonymous: bool = False, limit: int = 200
) -> dict:
    """
    Process payments.csv to sum gross amounts by donor name grouped by year.
    """
    con = duckdb.connect(database=":memory:")
    query = f"""
        SELECT 
            YEAR(Date) as Year,
            "Full Name"
        FROM read_csv_auto('{file_path}')
        WHERE "Anonymous?" = {allow_anonymous} and "Full Name" NOT Null
        GROUP BY YEAR(Date), "Full Name"
        HAVING SUM(CAST(REPLACE(REPLACE("Gross Amount", '$', ''), ',', '') AS DECIMAL(10, 2))) >= {limit}
        ORDER BY Year DESC, "Full Name" ASC
    """
    result = con.execute(query).fetchall()

    grouped_output = defaultdict(list)
    for year, name in result:
        grouped_output[str(year)].append(name.title())

    return dict(grouped_output)


def process_lifetime(
    file_path: str, allow_anonymous: bool = False, limit: int = 200
) -> list:
    """
    Process payments.csv to sum total gross amounts by donor name for their lifetime.
    """
    con = duckdb.connect(database=":memory:")
    query = f"""
        SELECT 
            "Full Name"
        FROM read_csv_auto('{file_path}')
        WHERE "Anonymous?" = {allow_anonymous} and "Full Name" NOT Null
        GROUP BY "Full Name"
        HAVING SUM(CAST(REPLACE(REPLACE("Gross Amount", '$', ''), ',', '') AS DECIMAL(10, 2))) >= {limit}
        ORDER BY "Full Name" ASC
    """
    result = con.execute(query).fetchall()

    return [name.title() for (name,) in result]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    mode: str = Form("annual"),
    limit: int = Form(200),
):
    # Save the file temporarily so duckdb can read it
    fd, temp_path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "wb") as f:
            content = await file.read()
            f.write(content)

        # Process the temporary file based on mode
        if mode == "annual":
            results = process_annual(temp_path, limit=limit)
        else:
            results = process_lifetime(temp_path, limit=limit)

        return JSONResponse(content=results)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
