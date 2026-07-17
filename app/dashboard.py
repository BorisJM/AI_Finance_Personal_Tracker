import streamlit as st
import plotly.express as px
import sys
import pandas as pd
from pathlib import Path

from pandas.core.dtypes import astype

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from src.analytics.income_analysis import calculate_total_income
from src.analytics.transactions_analysis import get_last_transactions
from src.pipeline.data_pipeline import run_pipeline
from src.analytics.spending_analysis import calculate_total_expenses, calculate_monthly_expenses, \
    calculate_biggest_expenses, calculate_monthly_expense_growth_rate, calculate_month_savings
from src.analytics.category_analysis import expenses_by_category

# Page config
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide",
)

# add page title
st.title("💰 Personal Finance Dashboard")
st.caption("Overview of your personal finances")
df = run_pipeline()

# Sidebar for filtering
with st.sidebar:
    st.header("Filters")

    selected_category = st.multiselect(
        "Category",
        options=sorted(df["transaction_category"].unique()),
    )

    date_range = st.date_input(
        "Date Range",
        value=(
            df["transaction_date"].min(),
            df["transaction_date"].max()
        )
    )


# Filtering functionality
filtered_df = df.copy()

# If category was selected
if selected_category:
    filtered_df = filtered_df[filtered_df["transaction_category"].isin(selected_category)]

# If date range was selected
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range)

    filtered_df = filtered_df[(filtered_df["transaction_date"] >= start_date) & (filtered_df["transaction_date"] <= end_date)]
# KPI CARDS
col1, col2, col3, col4, col5 = st.columns(5)

st.divider()

# Placing for charts, plots
left, right = st.columns(2)

# Total expenses
total_expenses = calculate_total_expenses(filtered_df)
expenses_month_rate = calculate_monthly_expense_growth_rate(filtered_df).tail(1)["trend_expense_percentage"].round()
print(expenses_month_rate)
# Total income
total_income = calculate_total_income(filtered_df)
# Total savings
monthly_savings = calculate_month_savings(filtered_df)
total_savings = monthly_savings["month_savings"].sum()
savings_rate =( total_savings / total_income) * 100
# Transactions count
transactions_count = len(filtered_df)

col1.metric(
    "Total expenses",
    f"{total_expenses:,.2f} zł".replace(",", " "),
    delta=expenses_month_rate
)


col2.metric(
    "Total income",
    f"{total_income:,.2f} zł".replace(",", " ")
)

col3.metric(
    "Total savings",
    f"{total_savings:,.2f} zł".replace(",", " ")
)

col4.metric(
    "Savings rate",
    f"{savings_rate:.2f}%"
)

col5.metric(
    "Transactions",
    transactions_count,
)

# Plots
# Plot of expenses by category
category_expenses = expenses_by_category(filtered_df)
# Convert numbers to positive for plot
category_expenses["debit_amount"] = (
    category_expenses["debit_amount"].abs()
)
fig = px.pie(
    category_expenses,
    values="debit_amount",
    names="transaction_category",
    title="🥧 Expenses by Category",
    hole=0.4
)

# Monthly expenses chart
monthly_expenses = calculate_monthly_expenses(filtered_df)
monthly_expenses["debit_amount"] = (monthly_expenses["debit_amount"].abs())
monthly_expenses["debit_amount"] = monthly_expenses["debit_amount"].astype(str)

figMonthlyExpenses = px.bar(
    monthly_expenses,
    x="transaction_month",
    y="debit_amount",
    color="debit_amount",
    text_auto=True,
    color_discrete_sequence=px.colors.sequential.Reds
)

figMonthlyExpenses.update_layout(
    title="📊 Monthly Expenses",
    xaxis_title="Month",
    yaxis_title="Expenses",
    showlegend=False,
)

with left:
    st.plotly_chart(figMonthlyExpenses, use_container_width=True)

with right:
    st.plotly_chart(fig, width='stretch')

# Top 10 expenses dashboard
top_10_expenses = calculate_biggest_expenses(filtered_df)
top_10_expenses.rename(columns={"transaction_description": "Description", "transaction_category": "Category", "debit_amount": "Value"}, inplace=True)

# Last 10 transactions
last_transactions = get_last_transactions(filtered_df)

with left:
    st.subheader("🧾 Last user transactions", text_alignment="center", divider=True)
    st.dataframe(last_transactions,
                 hide_index=True,
                 use_container_width=True)

with right:
    st.header("🌐 Top 10 expenses", text_alignment="center", divider=True)
    st.dataframe(
        top_10_expenses,
        hide_index=True,
        use_container_width=True,
    )

# Trending monthly expenses
monthly_expense_trends_data = calculate_monthly_expense_growth_rate(filtered_df)

st.subheader("📈 Monthly expense trends", text_alignment="center",divider=True)

figTrendExpenses = px.line(
    monthly_expense_trends_data,
    x="transaction_month",
    y="trend_expense_percentage",
    markers=True,
)


figTrendExpenses.update_traces(
    line_width=4,
    marker_size=8,
)
st.plotly_chart(figTrendExpenses, use_container_width=True)
