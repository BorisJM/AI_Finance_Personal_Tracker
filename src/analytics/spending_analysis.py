import pandas as pd

from src.analytics.analytics_helpers import prepare_spending_data, add_transaction_period
from src.analytics.income_analysis import calculate_monthly_income, calculate_total_income

# Function to calculate total expenses
def calculate_total_expenses(df):
    df = prepare_spending_data(df)
    return df["expense_amount"].sum()

# Function to calculate total expenses per month
def calculate_monthly_expenses(df):
    df = add_transaction_period(df)
    df = prepare_spending_data(df)

    total_expenses_per_month = df.groupby("transaction_period")["expense_amount"].sum().reset_index()
    # Ascending sorting by month name
    total_expenses_per_month.sort_values(by=["transaction_period"], inplace=True)
    return total_expenses_per_month

# Function to calculate top 10 expenses
def calculate_biggest_expenses(df):
    df = prepare_spending_data(df)

    biggest_expenses = df.nlargest(10, "expense_amount")[["transaction_description", "transaction_category", "expense_amount"]]
    return biggest_expenses

# Function to calculate average monthly expense
def calculate_average_monthly_expense(df):
    df = add_transaction_period(df)
    df = prepare_spending_data(df)

    monthly = (
        df.groupby("transaction_period")["expense_amount"]
        .sum()
        .mean()
        .round(2)
    )

    return monthly

# Function to calculate top transactions
def top_transactions(df):
    df = prepare_spending_data(df)
    df["transaction_amount"] = df["expense_amount"] + df["income_amount"]
    biggest_transactions = df.nlargest(10, "transaction_amount")[["transaction_category", "expense_amount", "income_amount"]]
    return biggest_transactions

# Function to track monthly expense trends.
def calculate_monthly_expense_growth_rate(df):
    monthly_total_expenses = calculate_monthly_expenses(df)

    monthly_total_expenses["expense_growth_rate"] = (
        monthly_total_expenses["expense_amount"]
        .pct_change()
        * 100
    )

    return monthly_total_expenses

# Function to calculate month savings
def calculate_month_savings(df):
    df = add_transaction_period(df)
    df = prepare_spending_data(df)
    monthly_savings = (df.groupby("transaction_period").agg(monthly_income=("income_amount", "sum"),monthly_expenses=("expense_amount", "sum")).reset_index())
    monthly_savings["month_savings"] = (monthly_savings["monthly_income"] - monthly_savings["monthly_expenses"])
    monthly_savings["month_savings_percentage"] = (monthly_savings["month_savings"] / monthly_savings["monthly_income"] * 100)

    return monthly_savings

# Function to calculate savings rate
def calculate_savings_rate(df):
    # Saving rate
    monthly_savings = calculate_month_savings(df)
    total_savings = monthly_savings["month_savings"].sum()
    total_income = calculate_total_income(df)
    if total_savings < 0:
        total_savings = 0
    if total_income != 0:
        savings_rate = (total_savings / total_income) * 100
    else:
        savings_rate = 0
    return savings_rate

