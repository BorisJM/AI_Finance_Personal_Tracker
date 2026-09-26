from src.analytics.analytics_helpers import prepare_spending_data, add_transaction_period


def income_insights(df):
    insights = []

    df = prepare_spending_data(df)
    df = add_transaction_period(df)

    # 1. LARGEST INCOME

    income_transactions = df[df["income_amount"] > 0]

    if not income_transactions.empty:
        largest_income = income_transactions.loc[
            income_transactions["income_amount"].idxmax()
        ]

        insights.append({
            "type": "info",
            "title": (
                f"Largest income: "
                f"{largest_income['income_amount']:.2f} zł"
            ),
            "message": (
                f"{largest_income['transaction_description'].lower()}"
            ),
        })

    # 2. MONTHLY INCOME CHANGE

    monthly_income = (
        df.groupby("transaction_period")["income_amount"]
        .sum()
        .reset_index(name="monthly_income")
        .sort_values("transaction_period")
    )

    if len(monthly_income) >= 2:
        monthly_income["income_percentage_diff"] = (
            monthly_income["monthly_income"]
            .pct_change()
            * 100
        )

        previous_month = monthly_income.iloc[-2]
        last_month = monthly_income.iloc[-1]

        income_increased = (
            last_month["income_percentage_diff"] > 0
        )

        income_change_type = (
            "success"
            if income_increased
            else "warning"
        )

        income_change_word = (
            "increased"
            if income_increased
            else "decreased"
        )

        insights.append({
            "type": income_change_type,
            "title": f"Income has {income_change_word}!",
            "message": (
                f"Previous month "
                f"{previous_month['transaction_period']} was "
                f"{previous_month['monthly_income']:.2f} zł "
                f"compared to last month "
                f"{last_month['transaction_period']} "
                f"{last_month['monthly_income']:.2f} zł, "
                f"the difference is "
                f"{last_month['income_percentage_diff']:.2f}%!"
            ),
        })

    return insights