# Function to calculate income
def calculate_total_income(df):
    total_income = df["credit_amount"].sum()
    return total_income

# Function to calculate monthly income
def calculate_monthly_income(df):
    monthly_income = df.groupby("transaction_month")["credit_amount"].sum().reset_index(name="monthly_income")
    return monthly_income

# Function to calculate monthly income growth rate
def calculate_monthly_income_growth_rate(df):
    every_month_income = calculate_monthly_income(df)
    every_month_income["month_growth_rate"] = every_month_income["monthly_income"].pct_change()*100
    return every_month_income