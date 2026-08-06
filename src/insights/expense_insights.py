import numpy as np

from src.analytics.category_analysis import category_percentages
import pandas as pd

from src.analytics.income_analysis import calculate_monthly_income
from src.analytics.spending_analysis import calculate_total_expenses, calculate_monthly_expenses


def expense_insights(df):
    insights = []
    # Insight 1
    # Category that takes the biggest part of all expenses
    try:
        categories_expenses = category_percentages(df)
        category_percentage = categories_expenses["percentage_of_total_expenses"].max()
        category_name = categories_expenses[categories_expenses["percentage_of_total_expenses"] == category_percentage]["transaction_category"].iloc[0]
        insight_category = {
            "type": "info",
            "title": "Most expensive category",
            "message": f"{category_name} account for {category_percentage}% of total expenses.",
        }
        insights.append(insight_category)
    except Exception:
        pass
    # Insight 2
    # Biggest increase compared to previous month
    try:
        biggest_category_increase_month = df.copy()
        # Ascending sorting by month name
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        biggest_category_increase_month["transaction_month"] = pd.Categorical(
            biggest_category_increase_month["transaction_month"],
            categories=months,
            ordered=True)
        biggest_category_increase_month.sort_values(by=["transaction_month"], inplace=True)
        biggest_category_increase_month = \
        biggest_category_increase_month.groupby(["transaction_month", "transaction_category"])[
            "debit_amount"].sum().reset_index().sort_values(["transaction_category"], ascending=True)

        biggest_category_increase_month["percentage_diff"] = \
        biggest_category_increase_month.groupby("transaction_category")["debit_amount"].pct_change() * 100
        # If previous month has 0 expenses -> will return inf, code below is used in case of INF
        biggest_category_increase_month["percentage_diff"] = biggest_category_increase_month["percentage_diff"].replace(
            [np.inf, -np.inf], np.nan)
        biggest_expense = biggest_category_increase_month.iloc[
            biggest_category_increase_month["percentage_diff"].idxmax()]

        insight_biggest_month_increase = {
            "type": "warning",
            "title": f"{biggest_expense["transaction_category"]} spending increased",
            "message": f"{biggest_expense["transaction_category"]} spending increased by {biggest_expense["percentage_diff"]:.2f}% compared to last month.",
        }
        insights.append(insight_biggest_month_increase)
    except Exception:
        pass

    try:
        # Insight 3
        # Biggest spending decrease compared to previous month
        biggest_category_decrease_month = biggest_category_increase_month.iloc[biggest_category_increase_month["percentage_diff"].idxmin()]

        insight_biggest_month_decrease = {
            "type": "info",
            "title": f"{biggest_category_decrease_month["transaction_category"]} spending decreased",
            "message": f"{biggest_category_decrease_month["transaction_category"]} spending decreased by {abs(biggest_category_decrease_month["percentage_diff"]):.2f}% compared to last month.",
        }
        insights.append(insight_biggest_month_decrease)
    except Exception:
        pass
    try:
        # Insight 4
        # Largest expense transaction
        largest_expense_transaction = df.copy()
        largest_expense = largest_expense_transaction.iloc[largest_expense_transaction["debit_amount"].idxmin()]

        insight_largest_expense_transaction = {
            "type": "warning",
            "title": "Largest expense",
            "message": f"{largest_expense['transaction_category']}: {largest_expense["transaction_description"]}, {abs(largest_expense["debit_amount"]):.2f} zł."
        }
        insights.append(insight_largest_expense_transaction)
    except Exception:
        pass

    try:
        # Insight 5
        # Most expensive day of the week
        df_added_day_of_the_week = df.copy()
        # Add day of the week column to our dataframe
        df_added_day_of_the_week["day_of_the_week"] = df_added_day_of_the_week["transaction_date"].dt.day_name()
        df_added_day_of_the_week = df_added_day_of_the_week.groupby("day_of_the_week")["debit_amount"].sum().reset_index()
        # Sorted by day of the week
        sorted_weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_added_day_of_the_week["day_of_the_week"] = pd.Categorical(df_added_day_of_the_week["day_of_the_week"],                                                                 sorted_weekdays)
        df_added_day_of_the_week = df_added_day_of_the_week.sort_values(["day_of_the_week"])
        # Most expensive day of the week
        most_expensive_day_of_the_week = df_added_day_of_the_week.iloc[df_added_day_of_the_week["debit_amount"].idxmin()]

        insight_most_expensive_day_of_the_week = {
            "type": "info",
            "title": "Most expensive day of the week",
            "message": f"Most money is spent on {most_expensive_day_of_the_week["day_of_the_week"]}."
        }
        insights.append(insight_most_expensive_day_of_the_week)
    except Exception:
        pass

    try:
        # Insight 6
        # Most money spent for one seller
        grouped_by_sellers = df.copy().groupby("transaction_description")
        money_spent_sellers = grouped_by_sellers["debit_amount"].sum().reset_index()
        most_money_spent_seller = money_spent_sellers.iloc[money_spent_sellers["debit_amount"].idxmin()]
        seller_percentage_of_whole_spending = (most_money_spent_seller["debit_amount"] / calculate_total_expenses(df)) * 100

        insight_most_money_spent_seller = {
            "type": "info",
            "title": "Most money spent seller",
            "message": f"{most_money_spent_seller['transaction_description']} accounts for {seller_percentage_of_whole_spending:.2f}% of your total spending",
        }
        insights.append(insight_most_money_spent_seller)
    except Exception:
        pass

    try:
        # Insight 7
        # Most expensive month
        highest_spending_month = df.copy()
        highest_spending_month["expense"] = abs(highest_spending_month["debit_amount"])
        highest_spending_month = highest_spending_month.groupby("transaction_month")["expense"].sum().reset_index()
        highest_spending_month = highest_spending_month.iloc[highest_spending_month["expense"].idxmax()]

        insight_highest_spending_month = {
            "type": "info",
            "title": "Highest spending month",
            "message": f"{highest_spending_month['transaction_month']} was your most expensive month this year.",
        }
        insights.append(insight_highest_spending_month)
    except Exception:
        pass
    try:
        # Insight 8
        # Consecutive increase (Increase should be at least for 3 month span
        # - Groupby transaction category and CATEGORY, sum spending for every month in categories, then to calculate pct change for those expenses so we can find the increase
        consecutive_increase = df.copy()
        consecutive_increase["expense"] = abs(consecutive_increase["debit_amount"])
        # Sort by months
        consecutive_increase["transaction_month"] = pd.Categorical(
            consecutive_increase["transaction_month"],
            categories=months,
            ordered=True)
        consecutive_increase.sort_values(by=["transaction_month"], inplace=True)
        consecutive_increase = consecutive_increase.groupby(["transaction_month", "transaction_category"])["expense"].sum().reset_index()
        # Sort by categories so we can calculate the percentage difference
        consecutive_increase = consecutive_increase.sort_values(by=["transaction_category"], ascending=True)
        # Percentage difference
        consecutive_increase["monthly_percentage_category_diff"] = (consecutive_increase.groupby("transaction_category")["expense"].pct_change() * 100).round(2)
        # Check if value increases
        consecutive_increase["consecutive_increase"] = consecutive_increase["monthly_percentage_category_diff"] > 0
        # Check if we got 2 TRUES in the row, if yes then it's a 3-month streak else no
        consecutive_increase["3_month_streak"]= (
            consecutive_increase.groupby("transaction_category")["consecutive_increase"].rolling(window=2, min_periods=2).sum().eq(2).reset_index(level=0, drop=True)
        )
        # Filtering
        consecutive_increase = consecutive_increase[(consecutive_increase["3_month_streak"] == True)].reset_index(drop=True)
        consecutive_increase = consecutive_increase.iloc[consecutive_increase["monthly_percentage_category_diff"].idxmax()]
        # Message
        consecutive_increase_insight = {
            "type": "warning",
            "title": "Increased consecutive spending",
            "message": f"{consecutive_increase["transaction_category"]} spending has increased for three consecutive months."
        }
        insights.append(consecutive_increase_insight)
    except Exception:
        pass
    try:
        # Insight 9
        # Spending vs income
        monthly_expenses = calculate_monthly_expenses(df)
        monthly_income = calculate_monthly_income(df)
        last_month_expenses = abs(monthly_expenses.tail(1)["debit_amount"])
        last_month_income = monthly_income.tail(1)["monthly_income"]
        spending_percentage = ((last_month_expenses / last_month_income) * 100).round(2).values[0]

        # Message
        insight_spending_vs_income = {
            "type": "info",
            "title": "Spending vs income",
            "message": f"You spent {spending_percentage}% of your income this month.",
        }
        insights.append(insight_spending_vs_income)
    except Exception:
        pass
    return insights