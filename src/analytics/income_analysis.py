# Function to calculate income
def calculate_total_income(df):
    total_income = df["credit_amount"].sum()
    return total_income

# Function to calculate monthly income
def calculate_monthly_income(df):
    monthly_income = df.groupby("transaction_month")["credit_amount"].sum().reset_index(name="monthly_income")
    return monthly_income