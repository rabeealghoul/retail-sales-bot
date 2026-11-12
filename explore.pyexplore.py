import sqlite3
import pandas as pd

conn = sqlite3.connect("data/retail.db")

print(pd.read_sql("""
SELECT DISTINCT StockCode, Description
FROM sales
WHERE Description IN ('DOTCOM POSTAGE', 'POSTAGE', 'Manual')
""", conn))

print(pd.read_sql("SELECT InvoiceDate FROM sales LIMIT 5", conn))

conn.close()