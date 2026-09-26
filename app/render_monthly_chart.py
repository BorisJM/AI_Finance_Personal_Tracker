import plotly.express as px

from src.analytics.spending_analysis import calculate_monthly_expenses


def render_monthly_chart(filtered_df):
    monthly_expenses = calculate_monthly_expenses(filtered_df).copy()

    monthly_expenses["transaction_period"] = (monthly_expenses["transaction_period"].astype(str))

    fig_monthly_expenses = px.bar(
        monthly_expenses,
        x="transaction_period",
        y="expense_amount",
        color="expense_amount",
        text_auto=True,
        color_discrete_sequence=px.colors.sequential.Reds,
    )

    fig_monthly_expenses.update_layout(
        title="📊 Monthly Expenses",
        xaxis_title="Month",
        yaxis_title="Expenses",
        showlegend=False,
    )

    fig_monthly_expenses.update_traces(
        texttemplate="%{y:.2f} zł",
    )

    return fig_monthly_expenses