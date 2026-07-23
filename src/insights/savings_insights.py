from src.analytics.spending_analysis import calculate_savings_rate


def saving_insights(df):
    # Recommended saving rate
    recommended_saving_rate = 20
    # Saving rate
    savings_rate = calculate_savings_rate(df)
    savings_insight_message = {
        "type": f"{"success" if savings_rate >= recommended_saving_rate else "danger"}",
        "title": f"Your savings rate is {savings_rate:.2f}%",
        "message": f"This is {"above" if savings_rate >= recommended_saving_rate else "below"} the recommended savings rate of {savings_rate:.2f}%",
    }
    return [savings_insight_message]