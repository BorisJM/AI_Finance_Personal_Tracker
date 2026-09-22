import pandas as pd

from src.analytics.analytics_helpers import prepare_spending_data, add_transaction_period


# Function to calculate income
def calculate_total_income(df):
    df = prepare_spending_data(df)
    total_income = df["income_amount"].sum()
    return total_income

# Function to calculate monthly income
def calculate_monthly_income(df):
    df = add_transaction_period(df)
    df = prepare_spending_data(df)
    monthly_income = df.groupby("transaction_period")["income_amount"].sum().reset_index(name="monthly_income")
    # Ascending sorting by month name
    monthly_income.sort_values(by=["transaction_period"], inplace=True)
    return monthly_income

# Function to calculate monthly income growth rate
def calculate_monthly_income_growth_rate(df):
    monthly_income = calculate_monthly_income(df)
    monthly_income["income_growth_rate"] = monthly_income["monthly_income"].pct_change()*100
    return monthly_income