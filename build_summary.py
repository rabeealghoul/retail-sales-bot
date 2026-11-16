import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
SRC = BASE / "data" / "retail.db"
OUT = BASE / "retail_summary.db"
VALID = "Quantity > 0 AND StockCode NOT IN ('POST', 'DOT', 'M', 'm')"

if OUT.exists():
    OUT.unlink()

with sqlite3.connect(SRC) as src, sqlite3.connect(OUT) as out:
    # جدول 1: إيرادات وطلبات لكل شهر ودولة
    monthly_country = pd.read_sql_query(
        f"""
        SELECT strftime('%Y-%m', InvoiceDate) AS month,
               Country,
               ROUND(SUM(Quantity * UnitPrice), 2) AS revenue,
               SUM(Quantity) AS units,
               COUNT(DISTINCT InvoiceNo) AS orders
        FROM sales WHERE {VALID}
        GROUP BY month, Country
        """,
        src,
    )
    monthly_country.to_sql("monthly_country", out, index=False)

    # جدول 2: إيرادات ووحدات لكل منتج ودولة
    product_country = pd.read_sql_query(
        f"""
        SELECT Country, Description,
               ROUND(SUM(Quantity * UnitPrice), 2) AS revenue,
               SUM(Quantity) AS units
        FROM sales WHERE {VALID}
        GROUP BY Country, Description
        """,
        src,
    )
    product_country.to_sql("product_country", out, index=False)

    # فحص: الإجمالي لازم يتطابق مع القاعدة الأصلية
    original = pd.read_sql_query(
        f"SELECT SUM(Quantity * UnitPrice) AS total FROM sales WHERE {VALID}", src
    ).iloc[0, 0]

print("monthly_country rows:", len(monthly_country))
print("product_country rows:", len(product_country))
print("original total:     ", round(original, 2))
print("summary total:      ", round(monthly_country["revenue"].sum(), 2))
print("file size (MB):     ", round(OUT.stat().st_size / 1_000_000, 2))