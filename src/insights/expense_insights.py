from src.analytics.category_analysis import category_percentages
import pandas as pd

def expense_insights(df):
    # Insight 1
    # Category that takes the biggest part of all expenses
    categories_expenses = category_percentages(df)
    category_percentage = categories_expenses["percentage_of_total_expenses"].max()
    category_name = categories_expenses[categories_expenses["percentage_of_total_expenses"] == category_percentage]["transaction_category"].iloc[0]
    insight_category = {
        "type": "info",
        "title": "Most expensive category",
        "message": f"{category_name} account for {category_percentage}% of total expenses.",
    }

    # Insight 2
    # Biggest increase compared to previous month
    biggest_category_increase_month = df.copy()
    # Ascending sorting by month name
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    biggest_category_increase_month["transaction_month"] = pd.Categorical(biggest_category_increase_month["transaction_month"],
                                                                   categories=months,
                                                                   ordered=True)
    biggest_category_increase_month.sort_values(by=["transaction_month"], inplace=True)
    biggest_category_increase_month = biggest_category_increase_month.groupby(["transaction_month", "transaction_category"])["debit_amount"].sum().reset_index().sort_values(["transaction_category"], ascending=True)
    
    biggest_category_increase_month["percentage_diff"]  = biggest_category_increase_month.groupby("transaction_category")["debit_amount"].pct_change()*100
    biggest_expense = biggest_category_increase_month.iloc[biggest_category_increase_month["percentage_diff"].idxmax()]

    insight_biggest_month_increase = {
        "type": "warning",
        "title": f"{biggest_expense["transaction_category"]} spending increased",
        "message": f"{biggest_expense["transaction_category"]} spending increased by {biggest_expense["percentage_diff"]:.2f}% compared to last month.",
    }

    # Insight 3
    # Biggest spending decrease compared to previous month
    biggest_category_decrease_month = biggest_category_increase_month.iloc[biggest_category_increase_month["percentage_diff"].idxmin()]

    insight_biggest_month_decrease = {
        "type": "info",
        "title": f"{biggest_category_decrease_month["transaction_category"]} spending decreased",
        "message": f"{biggest_category_decrease_month["transaction_category"]} spending decreased by {abs(biggest_category_decrease_month["percentage_diff"]):.2f}% compared to last month.",
    }

    # Insight 4
    # Largest expense transaction
    largest_expense_transaction = df.copy()
    largest_expense = largest_expense_transaction.iloc[largest_expense_transaction["debit_amount"].idxmin()]

    insight_largest_expense_transaction = {
        "type": "warning",
        "title": "Largest expense",
        "message": f"{largest_expense['transaction_category']}: {largest_expense["transaction_description"]}, {abs(largest_expense["debit_amount"]):.2f} zł."
    }

    return [insight_category, insight_biggest_month_increase, insight_biggest_month_decrease, insight_largest_expense_transaction]