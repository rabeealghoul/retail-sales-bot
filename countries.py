import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/retail.db")

query = """
SELECT Country, ROUND(SUM(Quantity * UnitPrice), 2) AS total_sales
FROM sales
WHERE Quantity > 0 AND UnitPrice > 0 AND InvoiceNo NOT LIKE 'C%'
GROUP BY Country
ORDER BY total_sales DESC
LIMIT 5
"""

by_country = pd.read_sql(query, conn)       # SQL تجيب
by_country.to_excel("countries.xlsx", index=False)   # pandas تكتب إكسل

by_country.plot(x="Country", y="total_sales", kind="bar")   # pandas ترسم
plt.tight_layout()
plt.savefig("countries.png")
conn.close()