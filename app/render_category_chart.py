import plotly.express as px

from src.analytics.category_analysis import expenses_by_category


def render_category_chart(filtered_df):
    # Plot of expenses by category
    category_expenses = expenses_by_category(filtered_df)
    # Convert numbers to positive for plot
    category_expenses["debit_amount"] = (
        category_expenses["debit_amount"].abs()
    )
    fig = px.pie(
        category_expenses,
        values="debit_amount",
        names="transaction_category",
        title="🥧 Expenses by Category",
        hole=0.3,
        color_discrete_sequence= px.colors.qualitative.Pastel,
        height=500,
    )

    fig.update_layout(
        font=dict(size=14)
    )
    return fig