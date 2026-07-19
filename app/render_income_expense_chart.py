import streamlit as st
import plotly.express as px

# Chart that will show incomes and expenses on one plot

def render_income_expense_chart(df):

    st.subheader("📊 Incomes and expenses", text_alignment="center", divider=True)

    # 2. Plotly figures
    fig1 = px.scatter(df, y="debit_amount", x="transaction_date", labels={"transaction_date": "Date", "debit_amount": "Income and Expense"})
    fig2 = px.line(df, y="credit_amount", x="transaction_date", labels={"transaction_date": "Date", "credit_amount": "Income"})

    fig1.add_trace(fig2.data[0])

    fig1.data[0].name = "Expenses"
    fig1.data[1].name = "Incomes"
    fig1.update_layout(showlegend=True)
    fig1.update_traces(
        line_width=5,
        marker_size=8,
    )
    st.plotly_chart(fig1, use_container_width=True)
