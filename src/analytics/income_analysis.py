import pandas as pd

# Function to calculate income
def calculate_total_income(df):
    total_income = df["credit_amount"].sum()
    return total_income

# Function to calculate monthly income
def calculate_monthly_income(df):
    monthly_income = df.groupby("transaction_month")["credit_amount"].sum().reset_index(name="monthly_income")
    # Ascending sorting by month name
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    monthly_income["transaction_month"] = pd.Categorical(monthly_income["transaction_month"],
                                                                   categories=months,
                                                                   ordered=True)
    monthly_income.sort_values(by=["transaction_month"], inplace=True)
    return monthly_income

# Function to calculate monthly income growth rate
def calculate_monthly_income_growth_rate(df):
    every_month_income = calculate_monthly_income(df)
    every_month_income["month_growth_rate"] = every_month_income["monthly_income"].pct_change()*100
    return every_month_income