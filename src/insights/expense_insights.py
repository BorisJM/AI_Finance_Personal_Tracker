import pandas as pd
from src.analytics.analytics_helpers import prepare_spending_data, add_transaction_period
from src.analytics.category_analysis import category_percentages
from src.analytics.income_analysis import calculate_monthly_income
from src.analytics.spending_analysis import (
    calculate_total_expenses,
    calculate_monthly_expenses,
)


def expense_insights(df):
    insights = []

    df = prepare_spending_data(df)
    df = add_transaction_period(df)

    # 1. MOST EXPENSIVE CATEGORY

    categories_expenses = category_percentages(df)

    if not categories_expenses.empty:
        biggest_category = categories_expenses.loc[
            categories_expenses["percentage_of_total_expenses"].idxmax()
        ]

        insights.append({
            "type": "info",
            "title": "Most expensive category",
            "message": (
                f"{biggest_category['transaction_category']} "
                f"account for "
                f"{biggest_category['percentage_of_total_expenses']:.2f}% "
                f"of total expenses."
            ),
        })

    # 2. BIGGEST CATEGORY INCREASE

    category_monthly = (
        df.groupby(
            ["transaction_period", "transaction_category"]
        )["expense_amount"]
        .sum()
        .reset_index()
    )

    category_monthly["percentage_diff"] = (
        category_monthly
        .sort_values("transaction_period")
        .groupby("transaction_category")["expense_amount"]
        .pct_change()
        * 100
    )

    valid_increases = category_monthly[
        category_monthly["percentage_diff"].notna()
        & (category_monthly["percentage_diff"] > 0)
    ]

    if not valid_increases.empty:
        biggest_increase = valid_increases.loc[
            valid_increases["percentage_diff"].idxmax()
        ]

        insights.append({
            "type": "warning",
            "title": f"{biggest_increase['transaction_category']} spending increased",
            "message": (
                f"{biggest_increase['transaction_category']} spending "
                f"increased by {biggest_increase['percentage_diff']:.2f}% "
                f"compared to last month."
            ),
        })

    # 3. BIGGEST CATEGORY DECREASE

    valid_decreases = category_monthly[
        category_monthly["percentage_diff"].notna()
        & (category_monthly["percentage_diff"] < 0)
    ]

    if not valid_decreases.empty:
        biggest_decrease = valid_decreases.loc[
            valid_decreases["percentage_diff"].idxmin()
        ]

        insights.append({
            "type": "info",
            "title": f"{biggest_decrease['transaction_category']} spending decreased",
            "message": (
                f"{biggest_decrease['transaction_category']} spending "
                f"decreased by "
                f"{abs(biggest_decrease['percentage_diff']):.2f}% "
                f"compared to last month."
            ),
        })

    # 4. LARGEST EXPENSE

    expenses_only = df[df["expense_amount"] > 0]

    if not expenses_only.empty:
        largest_expense = expenses_only.loc[
            expenses_only["expense_amount"].idxmax()
        ]

        insights.append({
            "type": "warning",
            "title": "Largest expense",
            "message": (
                f"{largest_expense['transaction_category']}: "
                f"{largest_expense['transaction_description']}, "
                f"{largest_expense['expense_amount']:.2f} zł."
            ),
        })

    # 5. MOST EXPENSIVE DAY OF THE WEEK

    df["day_of_week"] = df["transaction_date"].dt.day_name()

    spending_by_day = (
        df.groupby("day_of_week")["expense_amount"]
        .sum()
    )

    if not spending_by_day.empty:
        most_expensive_day = spending_by_day.idxmax()

        insights.append({
            "type": "info",
            "title": "Most expensive day of the week",
            "message": (
                f"Most money is spent on {most_expensive_day}."
            ),
        })

    # 6. MOST MONEY SPENT SELLER

    spending_by_seller = (
        df.groupby("transaction_description")["expense_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    total_expenses = calculate_total_expenses(df)

    if not spending_by_seller.empty and total_expenses > 0:
        top_seller = spending_by_seller.index[0]
        seller_expenses = spending_by_seller.iloc[0]

        seller_percentage = (
            seller_expenses / total_expenses * 100
        )

        insights.append({
            "type": "info",
            "title": "Most money spent seller",
            "message": (
                f"{top_seller} accounts for "
                f"{seller_percentage:.2f}% "
                f"of your total spending."
            ),
        })

    # 7. HIGHEST SPENDING MONTH

    monthly_expenses = calculate_monthly_expenses(df)

    if not monthly_expenses.empty:
        highest_spending_month = monthly_expenses.loc[
            monthly_expenses["expense_amount"].idxmax()
        ]

        insights.append({
            "type": "info",
            "title": "Highest spending month",
            "message": (
                f"{highest_spending_month['transaction_period']} "
                f"was your most expensive month."
            ),
        })

    # 8. THREE CONSECUTIVE MONTHS OF INCREASING SPENDING

    consecutive = category_monthly.copy()

    consecutive["increase"] = (
        consecutive
        .sort_values("transaction_period")
        .groupby("transaction_category")["expense_amount"]
        .diff()
        .gt(0)
    )

    consecutive["increase_streak"] = (
        consecutive
        .sort_values("transaction_period")
        .groupby("transaction_category")["increase"]
        .rolling(2)
        .sum()
        .reset_index(level=0, drop=True)
    )

    streaks = consecutive[
        consecutive["increase_streak"] == 2
    ]

    if not streaks.empty:
        streak = streaks.iloc[0]

        insights.append({
            "type": "warning",
            "title": "Increased consecutive spending",
            "message": (
                f"{streak['transaction_category']} spending "
                f"has increased for three consecutive months."
            ),
        })

    # 9. SPENDING VS INCOME

    monthly_income = calculate_monthly_income(df)

    if not monthly_expenses.empty and not monthly_income.empty:
        last_expense = monthly_expenses.iloc[-1]
        last_income = monthly_income.iloc[-1]

        last_month_expenses = last_expense["expense_amount"]
        last_month_income = last_income["monthly_income"]

        if last_month_income > 0:
            spending_percentage = (
                last_month_expenses
                / last_month_income
                * 100
            )
        else:
            spending_percentage = 0

        insights.append({
            "type": "info",
            "title": "Spending vs income",
            "message": (
                f"You spent {spending_percentage:.2f}% "
                f"of your income this month."
            ),
        })

    return insights