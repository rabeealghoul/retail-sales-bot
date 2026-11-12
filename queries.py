import sqlite3
import pandas as pd

conn = sqlite3.connect("data/retail.db")

query = """
SELECT Description, COUNT(*) AS n_rows
FROM sales
GROUP BY Description        
ORDER BY n_rows DESC
LIMIT 5
"""

print(pd.read_sql(query, conn))
conn.close()