import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

df = pd.read_csv("data/retail.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
print("البداية:", len(df))

df = df.drop_duplicates()
print("بعد حذف المكرر:", len(df))

df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
print("بعد حذف الفواتير الملغية:", len(df))

df = df[df["Quantity"] > 0]
print("بعد حذف الكمية السالبة:", len(df))

df = df[df["UnitPrice"] > 0]
print("بعد حذف السعر الصفري:", len(df))
print(df["InvoiceDate"].dtype)
print(df.head())
print()
print(df.info())
print()
print(df.isna().sum())
df["total"] = df["Quantity"] * df["UnitPrice"]
print("إجمالي المبيعات:", round(df["total"].sum(), 2))
not_products = ["DOTCOM POSTAGE", "POSTAGE", "Manual"]
df = df[~df["Description"].isin(not_products)]
top_products = df.groupby("Description")["total"].sum().sort_values(ascending=False).head(10)
by_country = df.groupby("Country")["total"].sum().sort_values(ascending=False).head(5)
df["month"] = df["InvoiceDate"].dt.to_period("M")
monthly = df.groupby("month")["total"].sum()
with pd.ExcelWriter("report.xlsx") as writer:
    top_products.to_excel(writer, sheet_name="Top Products")
    by_country.to_excel(writer, sheet_name="By Country")
    monthly.to_excel(writer, sheet_name="Monthly")

print("تم إنشاء report.xlsx")
monthly.index = monthly.index.astype(str)
monthly.plot(kind="line", marker="o")
plt.title("Monthly Sales")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_sales.png")
plt.close()

top_products.sort_values().plot(kind="barh")
plt.title("Top 10 Products")
plt.xlabel("Sales")
plt.tight_layout()
plt.savefig("top_products.png")
plt.close()

print("تم حفظ الرسوم")
