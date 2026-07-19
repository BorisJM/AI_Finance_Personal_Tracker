import streamlit as st
import math
from src.analytics.income_analysis import calculate_total_income, calculate_monthly_income_growth_rate
from src.analytics.spending_analysis import calculate_total_expenses, calculate_monthly_expense_growth_rate, \
    calculate_month_savings


def render_kpis(filtered_df):
    # Total expenses
    total_expenses = calculate_total_expenses(filtered_df)
    # Expenses growth rate
    expenses_month_rate = calculate_monthly_expense_growth_rate(filtered_df)["trend_expense_percentage"]
    if len(expenses_month_rate) > 0:
        expenses_month_rate = expenses_month_rate.iloc[-1].round()
        if math.isnan(expenses_month_rate):
            delta_expenses = ""
        else:
            # Delta string format
            delta_expenses = f"{"" if expenses_month_rate < 0 else "+"}{expenses_month_rate:}%"
    else:
        delta_expenses = ""
    # Total income
    total_income = calculate_total_income(filtered_df)
    # Income growth rate
    income_month_rate = calculate_monthly_income_growth_rate(filtered_df)["month_growth_rate"]
    if len(income_month_rate) > 0:
        income_month_rate = income_month_rate.iloc[-1].round()
        if math.isnan(income_month_rate):
            delta_income = ""
        else:
            # Delta string format
            delta_income = f"{"" if income_month_rate < 0 else "+"}{income_month_rate:}%"
    else:
        delta_income = ""
    # Total savings
    monthly_savings = calculate_month_savings(filtered_df)
    total_savings = monthly_savings["month_savings"].sum()
    if total_savings < 0:
        total_savings = 0
    if total_income != 0:
        savings_rate =( total_savings / total_income) * 100
    else:
        savings_rate = 0
    # Transactions count
    transactions_count = len(filtered_df)

    # KPI CARDS
    col1, col2, col3, col4, col5 = st.columns(5)

    # KPIS
    col1.metric(
        "Total expenses",
        f"{total_expenses:,.2f} zł".replace(",", " "),
        delta=delta_expenses
    )
    col1.caption("Compared to previous month")

    col2.metric(
        "Total income",
        f"{total_income:,.2f} zł".replace(",", " "),
        delta=delta_income
    )

    col2.caption("Compared to previous month")

    col3.metric(
        "Total savings",
        f"{total_savings:,.2f} zł".replace(",", " ")
    )

    col4.metric(
        "Savings rate",
        f"{savings_rate:.2f}%"
    )

    col5.metric(
        "Transactions",
        transactions_count,
    )