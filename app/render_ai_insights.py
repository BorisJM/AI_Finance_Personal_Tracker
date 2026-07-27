import streamlit as st

from src.insights.ai_insights import generate_ai_insights

ICONS = {
    "info": "🔵",
    "warning": "🟠",
    "danger": "🛑",
    "success": "🟢",
}


def render_ai_insights(filtered_df):
    insights = generate_ai_insights(filtered_df)
    st.header("AI Insights", text_alignment="center")

    if not insights:
        st.info("No insights available.")
        return

    # How many cards in one row
    CARDS_PER_ROW = 3

    for i in range(0, len(insights), CARDS_PER_ROW):
        row = insights[i : i + CARDS_PER_ROW]
        cols = st.columns(len(row), gap="medium")

        for col, insight in zip(cols, row):

            icon = ICONS.get(insight["type"], "⚪")

            with col:
                with st.container(border=True):
                    st.subheader(f"{icon} {insight["title"]}")
                    st.write(insight["message"])

