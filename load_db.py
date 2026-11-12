import pandas as pd
import sqlite3

df = pd.read_csv("data/retail.csv")

conn = sqlite3.connect("data/retail.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
conn.close()

print("تم إنشاء قاعدة البيانات")