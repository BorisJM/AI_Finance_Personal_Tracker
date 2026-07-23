from src.insights.expense_insights import expense_insights
from src.insights.income_insights import income_insights
from src.insights.savings_insights import saving_insights
from src.insights.waste_insights import waste_insights


def generate_ai_insights(df):
    insights = []
    # Expenses
    expense_insights_data = expense_insights(df)
    # Incomes
    income_insights_data = income_insights(df)
    # Waste
    waste_insights_data = waste_insights(df)
    # Savings
    saving_insights_data = saving_insights(df)
    insights.append(expense_insights_data)
    insights.append(income_insights_data)
    insights.append(waste_insights_data)
    insights.append(saving_insights_data)
    insights = [x for l in insights for x in l]
    return insights