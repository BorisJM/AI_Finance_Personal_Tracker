import plotly.express as px

from src.analytics.spending_analysis import calculate_monthly_expenses


def render_monthly_chart(filtered_df):
    monthly_expenses = calculate_monthly_expenses(filtered_df)
    monthly_expenses["debit_amount"] = (monthly_expenses["debit_amount"].abs())


    figMonthlyExpenses = px.bar(
        monthly_expenses,
        x="transaction_month",
        y="debit_amount",
        color="debit_amount",
        text_auto=True,
        color_discrete_sequence=px.colors.sequential.Reds
    )

    figMonthlyExpenses.update_layout(
        title="📊 Monthly Expenses",
        xaxis_title="Month",
        yaxis_title="Expenses",
        showlegend=False,
    )

    figMonthlyExpenses.update_traces(
        texttemplate="%{y:.2f} zł",
    )
    return figMonthlyExpenses