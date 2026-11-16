import os
import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
API_KEY = os.environ["REPORT_API_KEY"]
DB_PATH = Path(__file__).parent / "retail_summary.db"


def check_key(x_api_key):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


def run_query(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df.to_dict(orient="records")


@app.get("/report")
def get_report(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query("""
        SELECT Description, ROUND(SUM(revenue), 2) AS revenue
        FROM product_country
        GROUP BY Description
        ORDER BY revenue DESC
        LIMIT 5;
    """)


@app.get("/revenue")
def get_revenue(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query("""
        SELECT ROUND(SUM(revenue), 2) AS total_revenue
        FROM monthly_country;
    """)


@app.get("/countries")
def get_countries(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query("""
        SELECT Country, ROUND(SUM(revenue), 2) AS revenue
        FROM monthly_country
        GROUP BY Country
        ORDER BY revenue DESC
        LIMIT 10;
    """)


@app.get("/country")
def get_country(name: str, x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query("""
        SELECT Country,
               ROUND(SUM(revenue), 2) AS revenue,
               SUM(orders) AS orders
        FROM monthly_country
        WHERE Country = ? COLLATE NOCASE
        GROUP BY Country;
    """, (name,))


@app.get("/monthly")
def get_monthly(x_api_key: str = Header()):
    check_key(x_api_key)
    return run_query("""
        SELECT month, ROUND(SUM(revenue), 2) AS revenue
        FROM monthly_country
        GROUP BY month
        ORDER BY month;
    """)


@app.get("/best-sellers")
def get_best_sellers(limit: int = 5, x_api_key: str = Header()):
    check_key(x_api_key)
    limit = max(1, min(limit, 20))
    return run_query("""
        SELECT Description, SUM(units) AS units
        FROM product_country
        GROUP BY Description
        ORDER BY units DESC
        LIMIT ?;
    """, (limit,))