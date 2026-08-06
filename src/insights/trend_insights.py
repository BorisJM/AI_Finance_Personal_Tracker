
def trend_insights(df):
    insights = []
    # Insight: Unusual expense
    # Now let's define what is unusual expense
    # The expenses that will be larger than calculated value below, are going to be UNUSUAL
    threshold = df["debit_amount"].abs().quantile(0.95)
    expenses_df = df.copy()
    expenses_df["expense"] =  expenses_df["debit_amount"].abs()
    category_average_value = expenses_df.groupby("transaction_category")["expense"].mean()
    expenses_df["category_average"] = expenses_df["transaction_category"].map(category_average_value)
    is_top_5_percent = (expenses_df["expense"] > threshold)

    is_large_for_category = (
        expenses_df["expense"] >
        expenses_df["category_average"] * 3
    )

    expenses_df = expenses_df[
        is_top_5_percent | is_large_for_category
    ]
    try:
        largest_unusual_expense = expenses_df.loc[expenses_df["expense"].idxmax()]
        unusual_expense_insight = {
            "type": "warning",
            "title": "Large unusual expense detected.",
            "message": (
                f"You spent {largest_unusual_expense["expense"]} zł "
                f"in category '{largest_unusual_expense["transaction_category"]}'. "
            )
        }
        insights.append(unusual_expense_insight)
    except Exception:
        pass
    return insights


