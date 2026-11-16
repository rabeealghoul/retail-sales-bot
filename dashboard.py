import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).parent / "data" / "retail.db"
VALID = "Quantity > 0 AND StockCode NOT IN ('POST', 'DOT', 'M', 'm')"

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")


@st.cache_data
def load(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)


st.title("Retail Sales Dashboard")

# فلتر الدولة
countries = load(
    f"SELECT DISTINCT Country FROM sales WHERE {VALID} ORDER BY Country"
)["Country"].tolist()
choice = st.sidebar.selectbox("Country", ["All"] + countries)

where, params = VALID, ()
if choice != "All":
    where += " AND Country = ?"
    params = (choice,)

# الأرقام الرئيسية
kpi = load(
    f"""
    SELECT SUM(Quantity * UnitPrice) AS revenue,
           COUNT(DISTINCT InvoiceNo) AS orders
    FROM sales WHERE {where}
    """,
    params,
).iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Total revenue", f"{kpi['revenue']:,.0f}")
c2.metric("Orders", f"{kpi['orders']:,.0f}")
c3.metric("Avg order value", f"{kpi['revenue'] / kpi['orders']:,.2f}")

# المبيعات الشهرية
st.subheader("Monthly revenue")
monthly = load(
    f"""
    SELECT strftime('%Y-%m', InvoiceDate) AS month,
           SUM(Quantity * UnitPrice) AS revenue
    FROM sales WHERE {where}
    GROUP BY month ORDER BY month
    """,
    params,
)
st.line_chart(monthly.set_index("month"))

# أعلى المنتجات
st.subheader("Top 10 products by revenue")
products = load(
    f"""
    SELECT Description, SUM(Quantity * UnitPrice) AS revenue
    FROM sales WHERE {where}
    GROUP BY Description ORDER BY revenue DESC LIMIT 10
    """,
    params,
)
st.bar_chart(products.set_index("Description"))

# ترتيب الدول (بس لما ما يكون في دولة محددة)
if choice == "All":
    st.subheader("Top 10 countries by revenue")
    top_countries = load(
        f"""
        SELECT Country, SUM(Quantity * UnitPrice) AS revenue
        FROM sales WHERE {VALID}
        GROUP BY Country ORDER BY revenue DESC LIMIT 10
        """
    )
    st.bar_chart(top_countries.set_index("Country"))