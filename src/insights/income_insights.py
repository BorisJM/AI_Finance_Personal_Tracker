import pandas as pd

def income_insights(df):
    # Insight
    # Largest income
    income_analysis = df.copy()
    largest_income = income_analysis.iloc[income_analysis["credit_amount"].idxmax()]
    print(largest_income)
    insight_largest_income = {
        "type": "info",
        "title": f"Largest income: {largest_income["credit_amount"]:.2f} zł",
        "message": f"{largest_income["transaction_description"].lower()}"
    }
        
    return [insight_largest_income]