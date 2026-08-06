from src.analytics.spending_analysis import calculate_savings_rate, calculate_month_savings


def saving_insights(df):
    insights = []
    # 1. Savings rate insight
    # Recommended saving rate
    recommended_saving_rate = 20
    # Saving rate
    savings_rate = calculate_savings_rate(df)
    savings_insight_message = {
        "type": f"{"success" if savings_rate >= recommended_saving_rate else "danger"}",
        "title": f"Your savings rate is {savings_rate:.2f}%",
        "message": f"This is {"above" if savings_rate >= recommended_saving_rate else "below"} the recommended savings rate of {recommended_saving_rate}%",
    }
    insights.append(savings_insight_message)
    try:
        # 2. Best savings month insight
        month_savings = calculate_month_savings(df)
        best_savings_month = month_savings.iloc[month_savings["month_savings"].idxmax()]

        # Message
        insight_best_savings_month = {
            "type": "success",
            "title": "Best savings month",
            "message": f"{best_savings_month["transaction_month"]} is your best savings month. You saved: {best_savings_month['month_savings']} zł",
        }
        insights.append(insight_best_savings_month)
    except Exception:
        pass
    return insights