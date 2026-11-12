import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "retail.db"

query = """
SELECT Description,
       SUM(Quantity * UnitPrice) AS revenue
FROM sales
WHERE Quantity > 0
  AND StockCode NOT IN ('POST', 'DOT', 'M', 'm')
GROUP BY Description
ORDER BY revenue DESC
LIMIT 5;
"""

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql(query, conn)
conn.close()

print(df.to_string(index=False))