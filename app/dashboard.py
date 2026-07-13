import streamlit as st
import plotly.express as px
import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from src.pipeline.data_pipeline import run_pipeline
from src.analytics.spending_analysis import calculate_total_expenses, calculate_monthly_expenses
from src.analytics.category_analysis import expenses_by_category

# Page config
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide",
)

# add page title
st.title("Personal Finance Dashboard")

st.write("Dashboard działa!")

df = run_pipeline()

# KPI CARDS
col1, col2, col3 = st.columns(3)

# Total expenses
total_expenses = calculate_total_expenses(df)
# Transactions count
transactions_count = len(df)
# Categories count
categories_count = df["transaction_category"].nunique()

col1.metric(
    "Total expenses",
    f"{total_expenses:.2f} zł",
)

col2.metric(
    "Transactions",
    transactions_count,
)

col3.metric(
    "Categories",
    categories_count,
)

# Plots
# Plot of expenses by category
category_expenses = expenses_by_category(df)
# Convert numbers to positive for plot
category_expenses["debit_amount"] = (
    category_expenses["debit_amount"].abs()
)
fig = px.pie(
    category_expenses,
    values="debit_amount",
    names="transaction_category",
    title="Expenses by Category",
)
st.plotly_chart(fig, width='stretch')

# Monthly expenses chart
monthly_expenses = calculate_monthly_expenses(df)
monthly_expenses["debit_amount"] = (monthly_expenses["debit_amount"].abs())
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
monthly_expenses["transaction_month"] = pd.Categorical(monthly_expenses["transaction_month"], categories=months, ordered=True)
monthly_expenses.sort_values(by=["transaction_month"], inplace=True)
st.bar_chart(monthly_expenses,
             x="transaction_month",
              y="debit_amount", )

# Top 10 expense