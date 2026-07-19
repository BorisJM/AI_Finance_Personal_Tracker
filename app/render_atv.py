import streamlit as st

from src.analytics.transactions_analysis import get_average_transaction_value


# Average transaction value

def render_atv(filtered_df):
    average_transaction_value = get_average_transaction_value(filtered_df)
    st.header("Average Transaction Value", text_alignment="center")
    st.subheader(f"{abs(average_transaction_value):.2f} zł", text_alignment="center")