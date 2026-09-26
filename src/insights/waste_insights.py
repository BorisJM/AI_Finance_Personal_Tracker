from src.analytics.analytics_helpers import prepare_spending_data


def waste_insights(df):
    insights = []

    cheap_purchase_value = 20

    df = prepare_spending_data(df)

    waste_transactions = (
        df[df["expense_amount"] < cheap_purchase_value]
        .groupby("transaction_category")["expense_amount"]
        .count()
        .reset_index(name="count")
    )

    if not waste_transactions.empty:
        largest_waste_transaction = waste_transactions.loc[
            waste_transactions["count"].idxmax()
        ]

        insights.append({
            "type": "warning",
            "title": (
                f"Waste detection: "
                f"{largest_waste_transaction['transaction_category']}"
            ),
            "message": (
                f"You made "
                f"{largest_waste_transaction['count']} purchases "
                f"below {cheap_purchase_value} zł."
            ),
        })

    return insights