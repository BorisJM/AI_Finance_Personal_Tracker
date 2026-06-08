# Function to calculate total expenses
def calculate_total_expenses(df):
    total_expenses = df["debit_amount"].sum()
    print("Total expenses:", round(total_expenses, 2))

# Function to calculate total expenses per month
def calculate_monthly_expenses(df):
    total_expenses_per_month = df.groupby("transaction_month")["debit_amount"].sum()
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