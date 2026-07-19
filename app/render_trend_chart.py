import streamlit as st
import plotly.express as px
from src.analytics.spending_analysis import calculate_monthly_expense_growth_rate


def render_trend_chart(filtered_df):
    monthly_expense_trends_data = calculate_monthly_expense_growth_rate(filtered_df)

    st.subheader("📈 Monthly expense trends", text_alignment="center", divider=True)

    figTrendExpenses = px.line(
        monthly_expense_trends_data,
        x="transaction_month",
        y="trend_expense_percentage",
        labels={"transaction_month": "Month", "trend_expense_percentage": "Expense Percentage"},
        markers=True,
    )

    figTrendExpenses.update_traces(
        line_width=4,
        marker_size=8,
    )

    figTrendExpenses.update_layout(
        hovermode="x unified",
    )
    st.plotly_chart(figTrendExpenses, use_container_width=True)
