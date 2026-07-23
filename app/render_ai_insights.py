import streamlit as st

from src.insights.ai_insights import generate_ai_insights


def render_ai_insights(filtered_df):
    insights = generate_ai_insights(filtered_df)
    st.header("AI Insights", text_alignment="center")
    # Render cards based on insights list:
    for insight in insights:
        messageType = ""
        if insight.get('type') == "info":
            messageType = "🔵"
        elif insight.get('type') == "warning":
            messageType = "🟠"
        elif insight.get('type') == "danger":
            messageType = "🛑"
        elif insight.get('type') == "success":
            messageType = "🟢"
        with st.container(border=True, width=300):
            st.subheader(f"{messageType} {insight.get('title')}")
            st.write(insight.get('message'))