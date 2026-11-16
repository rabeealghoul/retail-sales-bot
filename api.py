import os
import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
API_KEY = os.environ["REPORT_API_KEY"]
DB_PATH = Path(__file__).parent / "data" / "retail.db"


def check_key(x_api_key):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

VALID = "Quantity > 0 AND StockCode NOT IN ('POST', 'DOT', 'M', 'm')"


def run_query(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df.to_dict(orient="records")


@app.get("/report")
def get_report(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query("""
        SELECT Description, SUM(Quantity * UnitPrice) AS revenue
        FROM sales
        WHERE Quantity > 0
          AND StockCode NOT IN ('POST', 'DOT', 'M', 'm')
        GROUP BY Description
        ORDER BY revenue DESC
        LIMIT 5;
    """)


@app.get("/revenue")
def get_revenue(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query("""
        SELECT SUM(Quantity * UnitPrice) AS total_revenue
        FROM sales
        WHERE Quantity > 0
          AND StockCode NOT IN ('POST', 'DOT', 'M', 'm');
    """)
@app.get("/countries")
def get_countries(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query(f"""
        SELECT Country, SUM(Quantity * UnitPrice) AS revenue
        FROM sales
        WHERE {VALID}
        GROUP BY Country
        ORDER BY revenue DESC
        LIMIT 10;
    """)


@app.get("/country")
def get_country(name: str, x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query(f"""
        SELECT Country,
               SUM(Quantity * UnitPrice) AS revenue,
               COUNT(DISTINCT InvoiceNo) AS orders
        FROM sales
        WHERE {VALID} AND Country = ? COLLATE NOCASE
        GROUP BY Country;
    """, (name,))


@app.get("/monthly")
def get_monthly(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query(f"""
        SELECT strftime('%Y-%m', InvoiceDate) AS month,
               SUM(Quantity * UnitPrice) AS revenue
        FROM sales
        WHERE {VALID}
        GROUP BY month
        ORDER BY month;
    """)


@app.get("/best-sellers")
def get_best_sellers(limit: int = 5, x_api_key: str = Header()):
    check_key(x_api_key)
    limit = max(1, min(limit, 20))
    return run_query(f"""
        SELECT Description, SUM(Quantity) AS units
        FROM sales
        WHERE {VALID}
        GROUP BY Description
        ORDER BY units DESC
        LIMIT ?;
    """, (limit,))