import pandas as pd

from src.analytics.income_analysis import calculate_monthly_income


# Function to calculate total expenses
def calculate_total_expenses(df):
    total_expenses = df["debit_amount"].sum()
    return total_expenses

# Function to calculate total expenses per month
def calculate_monthly_expenses(df):
    total_expenses_per_month = df.groupby("transaction_month")["debit_amount"].sum().reset_index()
    # Ascending sorting by month name
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    total_expenses_per_month["transaction_month"] = pd.Categorical(total_expenses_per_month["transaction_month"], categories=months,
                                                           ordered=True)
    total_expenses_per_month.sort_values(by=["transaction_month"], inplace=True)
    print(total_expenses_per_month)
    return total_expenses_per_month

# Function to calculate top 10 expenses
def calculate_biggest_expenses(df):
    biggest_expenses = df.nsmallest(10, "debit_amount")[["transaction_description", "transaction_category", "debit_amount"]]
    return biggest_expenses

# Function to calculate average monthly expense
def calculate_average_monthly_expense(df):
    monthly = df.groupby("transaction_month")["debit_amount"].sum().mean().round(2)
    return monthly

# Function to calculate top transactions
def top_transactions(df):
    biggest_transactions = df.copy()
    biggest_transactions["debit_amount"] = biggest_transactions["debit_amount"].apply(lambda val: abs(val))
    biggest_transactions["transaction_amount"] = biggest_transactions["debit_amount"] + biggest_transactions["credit_amount"]
    biggest_transactions = biggest_transactions.nlargest(10, "transaction_amount")[["transaction_category", "debit_amount", "credit_amount"]]
    return biggest_transactions

# Function to track monthly expense trends.
def calculate_monthly_expense_growth_rate(df):
    monthly_total_expenses = calculate_monthly_expenses(df)
    # calculate monthly expense for every month
    monthly_total_expenses["trend_expense_percentage"] = monthly_total_expenses["debit_amount"].pct_change()*100
    print(monthly_total_expenses)

    return monthly_total_expenses

# Function to calculate month savings
def calculate_month_savings(df):
    monthly_savings = df.copy()
    monthly_savings = (monthly_savings.groupby("transaction_month")["credit_amount"].sum().round(2) + monthly_savings.groupby("transaction_month")["debit_amount"].sum().round(2)).reset_index(name="month_savings")
    # Monthly income to calculate savings percentage
    monthly_income = calculate_monthly_income(df)
    monthly_savings["month_savings_percentage"] = (monthly_savings["month_savings"] / monthly_income["monthly_income"]) * 100

    return monthly_savings

