from src.analytics.analytics_helpers import (prepare_spending_data, add_transaction_period)
from src.analytics.spending_analysis import calculate_monthly_expenses

# Function to calculate expenses by category
def expenses_by_category(df):
    df = prepare_spending_data(df)

    total_expenses_by_category = (
        df[df["transaction_category"] != "Income"]
        .groupby("transaction_category")["expense_amount"]
        .sum()
        .reset_index()
    )

    return total_expenses_by_category

# Function to calculate what percentage every category takes
def category_percentages(df):
    df = prepare_spending_data(df)

    total_expenses = df["expense_amount"].sum()
    total_expenses_by_category = expenses_by_category(df)

    if total_expenses == 0:
        return 0

    total_expenses_by_category["percentage_of_total_expenses"] = (
        total_expenses_by_category["expense_amount"]
        / total_expenses
        * 100
    ).round(2)

    return total_expenses_by_category


# Category percentage per month
def category_percentage_per_month(df):
    df = add_transaction_period(df)
    df = prepare_spending_data(df)

    category_per_month = (
        df[df["transaction_category"] != "Income"]
        .groupby(
            ["transaction_period", "transaction_category"]
        )["expense_amount"]
        .sum()
        .reset_index()
    )

    total_expenses_per_month = calculate_monthly_expenses(df)

    category_per_month = category_per_month.merge(
        total_expenses_per_month,
        on="transaction_period",
        suffixes=("_category", "_month")
    )

    category_per_month["category_percentage_of_month"] = (
        category_per_month["expense_amount_category"]
        / category_per_month["expense_amount_month"]
        * 100
    ).round(2)

    return category_per_month
# Function to get top categories
def top_categories(df):
    top_categories_sorted = category_percentages(df).sort_values(by=["percentage_of_total_expenses"], ascending=False)
    return top_categories_sorted