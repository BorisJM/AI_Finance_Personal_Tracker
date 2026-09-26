from src.analytics.spending_analysis import (
    calculate_savings_rate,
    calculate_month_savings,
)


def saving_insights(df):
    insights = []

    # 1. SAVINGS RATE

    recommended_saving_rate = 20
    savings_rate = calculate_savings_rate(df)

    savings_insight = {
        "type": (
            "success"
            if savings_rate >= recommended_saving_rate
            else "danger"
        ),
        "title": f"Your savings rate is {savings_rate:.2f}%",
        "message": (
            f"This is "
            f"{'above' if savings_rate >= recommended_saving_rate else 'below'} "
            f"the recommended savings rate of "
            f"{recommended_saving_rate}%"
        ),
    }

    insights.append(savings_insight)

    # 2. BEST SAVINGS MONTH

    monthly_savings = calculate_month_savings(df)

    if not monthly_savings.empty:
        best_savings_month = monthly_savings.loc[
            monthly_savings["month_savings"].idxmax()
        ]

        insights.append({
            "type": "success",
            "title": "Best savings month",
            "message": (
                f"{best_savings_month['transaction_period']} "
                f"is your best savings month. "
                f"You saved: "
                f"{best_savings_month['month_savings']:.2f} zł"
            ),
        })

    return insights