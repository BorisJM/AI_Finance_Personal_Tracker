import streamlit as st
import plotly.express as px

from src.analytics.spending_analysis import (
    calculate_monthly_expense_growth_rate,
)


def render_trend_chart(filtered_df):
    monthly_expense_trends_data = (
        calculate_monthly_expense_growth_rate(filtered_df).copy()
    )

    monthly_expense_trends_data["transaction_period"] = (monthly_expense_trends_data["transaction_period"].astype(str))

    st.subheader(
        "📈 Monthly expense trends",
        text_alignment="center",
        divider=True,
    )

    fig_trend_expenses = px.line(
        monthly_expense_trends_data,
        x="transaction_period",
        y="expense_growth_rate",
        labels={
            "transaction_period": "Month",
            "expense_growth_rate": "Expense Growth (%)",
        },
        markers=True,
    )

    fig_trend_expenses.update_traces(
        line_width=4,
        marker_size=8,
    )

    fig_trend_expenses.update_layout(
        hovermode="x unified",
    )

    st.plotly_chart(
        fig_trend_expenses,
        use_container_width=True,
    )