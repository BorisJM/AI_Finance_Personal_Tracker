import streamlit as st
import plotly.express as px
import sys
import pandas as pd
from pathlib import Path

from spacy.attrs import key

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from app.render_category_chart import render_category_chart
from app.render_kpis import render_kpis
from app.render_monthly_chart import render_monthly_chart
from app.render_tables import render_tables
from app.render_trend_chart import render_trend_chart
from src.pipeline.data_pipeline import run_pipeline

# Page config
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide",
)

# add page title
st.title("💰 Personal Finance Dashboard")
st.caption("Overview of your personal finances")
@st.cache_data
def load_data():
    return run_pipeline()
df = load_data()
# Filtering functionality
filtered_df = df.copy()

# Intialize default options in session state
if "selected_category" not in st.session_state:
    st.session_state.selected_category = []
if "date_range" not in st.session_state:
    st.session_state.date_range = (df["transaction_date"].min(), df["transaction_date"].max())

def reset_filters():
    st.session_state.selected_category = []
    st.session_state.date_range = (
            df["transaction_date"].min(),
            df["transaction_date"].max()
        )
# Sidebar for filtering
with st.sidebar:
    st.multiselect(
        "Category",
        options=sorted(df["transaction_category"].unique()),
        key="selected_category",
    )

    st.date_input(
        "Date Range",
        value=(
            df["transaction_date"].min(),
            df["transaction_date"].max()
        ),
        key="date_range"
    )

    # Reset filters button
    st.button(label="Reset filters", use_container_width=True, on_click=reset_filters)

# If category was selected
if st.session_state.selected_category:
    filtered_df = filtered_df[filtered_df["transaction_category"].isin(st.session_state.selected_category)]

# If date range was selected
if len(st.session_state.date_range) == 2:
    start_date, end_date = pd.to_datetime(st.session_state.date_range)

    filtered_df = filtered_df[(filtered_df["transaction_date"] >= start_date) & (filtered_df["transaction_date"] <= end_date)]
# KPI CARDS
render_kpis(filtered_df)

st.divider()

# Placing for charts, plots
left, right = st.columns(2)

# Category chart
fig = render_category_chart(filtered_df)

# Monthly expenses chart
figMonthlyExpenses = render_monthly_chart(filtered_df)

with left:
    st.plotly_chart(figMonthlyExpenses, use_container_width=True)

with right:
    st.plotly_chart(fig, width='stretch')

# Tables
render_tables(filtered_df)

# Trending monthly expenses
render_trend_chart(filtered_df)