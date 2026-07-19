import streamlit as st
from src.analytics.spending_analysis import calculate_biggest_expenses
from src.analytics.transactions_analysis import get_last_transactions

def render_tables(filtered_df):
    # Top 10 expenses dashboard
    top_10_expenses = calculate_biggest_expenses(filtered_df)
    top_10_expenses.rename(columns={"transaction_description": "Description", "transaction_category": "Category", "debit_amount": "Value"}, inplace=True)

    # Last 10 transactions
    last_transactions = get_last_transactions(filtered_df)

    st.subheader("🧾 Last user transactions", text_alignment="center", divider=True)
    st.dataframe(last_transactions,
                     hide_index=True,
                     use_container_width=True)

    st.header("🌐 Top 10 expenses", text_alignment="center", divider=True)
    st.dataframe(
            top_10_expenses,
            hide_index=True,
            use_container_width=True,
        )
