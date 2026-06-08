from src.analytics.spending_analysis import calculate_monthly_expenses

# Function to calculate expenses by category
def expenses_by_category(df):
    # Don't include income category
    total_expenses_by_category = df[df["transaction_category"] != "Income"].groupby("transaction_category")["debit_amount"].sum().reset_index()
    return total_expenses_by_category

# Function to calculate what percentage every category takes
def category_percentages(df):
    total_expenses = df["debit_amount"].sum()
    total_expenses_by_category = expenses_by_category(df)
    # Check if expenses not zero
    if total_expenses == 0:
        return 0
    else:
        total_expenses_by_category["percentage_of_total_expenses"] = ((total_expenses_by_category["debit_amount"] / total_expenses)*100).round(2)
        return total_expenses_by_category

# Category percentage per month
def category_percentage_per_month(df):
    category_per_month_percentage = df[df["transaction_category"] != "Income"].groupby(["transaction_month", "transaction_category"])["debit_amount"].sum().reset_index()
    total_expenses_per_month = calculate_monthly_expenses(df)
    # We merge two tables with all expenses per month and category expenses per category in each month
    category_per_month_percentage = category_per_month_percentage.merge(total_expenses_per_month, on="transaction_month", suffixes=("_category", "_month"))
    category_per_month_percentage["category_percentage_of_month"] = (category_per_month_percentage["debit_amount_category"] / category_per_month_percentage["debit_amount_month"]*100).round(2)
    return category_per_month_percentage
# Function to get top categories
def top_categories(df):
    top_categories_sorted = category_percentages(df).sort_values(by=["percentage_of_total_expenses"], ascending=False)
    return top_categories_sorted