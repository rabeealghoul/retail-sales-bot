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


def run_query(query):
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)
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