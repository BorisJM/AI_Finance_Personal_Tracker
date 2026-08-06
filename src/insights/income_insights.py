import pandas as pd

def income_insights(df):
    insights = []
    # Income Insights
    try:
        # 1. Largest income
        income_analysis = df.copy()
        largest_income = income_analysis.iloc[income_analysis["credit_amount"].idxmax()]

        # -------- Insight message --------

        insight_largest_income = {
            "type": "info",
            "title": f"Largest income: {largest_income["credit_amount"]:.2f} zł",
            "message": f"{largest_income["transaction_description"].lower()}"
        }
        insights.append(insight_largest_income)
    except Exception:
        pass
    try:
        # 2. Income monthly change, increased / decreased in %
        monthly_income_analysis = df.copy()
        # Sorted by months
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        monthly_income_analysis['transaction_month'] = pd.Categorical(df['transaction_month'], categories=months,
                                                                      ordered=True)
        monthly_income_analysis = monthly_income_analysis.groupby("transaction_month")["credit_amount"].sum().reset_index()
        # Difference in percentages monthly
        monthly_income_analysis["income_percentage_diff"] = (monthly_income_analysis["credit_amount"].pct_change() * 100).round(2)
        monthly_income_analysis["has_increased"] = (monthly_income_analysis["income_percentage_diff"] > 0)
        # Select last two months
        income_last_two_months = monthly_income_analysis.tail(2)
        # Income previous month
        income_previous_month = income_last_two_months.iloc[0]
        # Income last month
        income_last_month = income_last_two_months.iloc[1]


        # -------- Insight message --------

        insight_income_increased_decreased = {
            "type": f"{"success" if income_last_month["has_increased"] else "warning"}",
            "title": f"Income has {"increased" if income_last_month["has_increased"] else "decreased"}!",
            "message": f"Previous month {income_previous_month["transaction_month"]} was {income_previous_month["credit_amount"]:.2f} zł compared to last month {income_last_month["transaction_month"]} {income_last_month["credit_amount"]} zł, the difference is {income_last_month["income_percentage_diff"]:.2f}% !",
        }
        insights.append(insight_income_increased_decreased)
    except Exception:
        pass
    # 3. Insight

    return insights