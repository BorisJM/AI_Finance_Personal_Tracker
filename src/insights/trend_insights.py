from src.analytics.analytics_helpers import prepare_spending_data


def trend_insights(df):
    insights = []

    df = prepare_spending_data(df)

    # Define unusual expense:
    # - expense is in the top 5% of all expenses
    # OR
    # - expense is more than 3x the average expense
    #   for its category

    threshold = df["expense_amount"].quantile(0.95)

    category_average = (
        df.groupby("transaction_category")["expense_amount"]
        .mean()
    )

    df["category_average"] = (
        df["transaction_category"]
        .map(category_average)
    )

    is_top_5_percent = (
        df["expense_amount"] > threshold
    )

    is_large_for_category = (
        df["expense_amount"]
        > df["category_average"] * 3
    )

    unusual_expenses = df[
        is_top_5_percent | is_large_for_category
    ]

    if not unusual_expenses.empty:
        largest_unusual_expense = unusual_expenses.loc[
            unusual_expenses["expense_amount"].idxmax()
        ]

        insights.append({
            "type": "warning",
            "title": "Large unusual expense detected.",
            "message": (
                f"You spent "
                f"{largest_unusual_expense['expense_amount']:.2f} zł "
                f"in category "
                f"'{largest_unusual_expense['transaction_category']}'."
            ),
        })

    return insights