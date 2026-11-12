import sqlite3
import pandas as pd

conn = sqlite3.connect("data/retail.db")

print(pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn))
print(pd.read_sql("PRAGMA table_info(sales)", conn))
print(pd.read_sql("SELECT * FROM sales LIMIT 5", conn))
print(pd.read_sql("SELECT COUNT(*) AS total_rows FROM sales", conn))    
query = """
SELECT Description,
       SUM(Quantity * UnitPrice) AS revenue
FROM sales
WHERE Quantity > 0
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;
"""

print(pd.read_sql(query, conn))

conn.close()    