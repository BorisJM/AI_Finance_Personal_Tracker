import streamlit as st
import plotly.express as px

from src.analytics.analytics_helpers import prepare_spending_data


def render_income_expense_chart(df):

    st.subheader(
        "📊 Incomes and expenses",
        text_alignment="center",
        divider=True
    )

    df = prepare_spending_data(df)

    fig = px.scatter(
        df,
        x="transaction_date",
        y="expense_amount",
        labels={
            "transaction_date": "Date",
            "expense_amount": "Expenses",
        },
    )

    income_fig = px.line(
        df,
        x="transaction_date",
        y="income_amount",
        labels={
            "transaction_date": "Date",
            "income_amount": "Income",
        },
    )

    fig.add_trace(income_fig.data[0])

    fig.data[0].name = "Expenses"
    fig.data[1].name = "Incomes"

    fig.update_layout(
        showlegend=True
    )

    fig.update_traces(
        line_width=5,
        marker_size=8,
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )