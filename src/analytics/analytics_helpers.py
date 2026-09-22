import pandas as pd
# Helper function to prepare data for analysis
def prepare_spending_data(df):
    result = df.copy()
    if "debit_amount" in result.columns:
        result["expense_amount"] = result["debit_amount"].abs()
    if "credit_amount" in result.columns:
        result["income_amount"] = result["credit_amount"]

    return result

def add_transaction_period(df):
    result = df.copy()

    result["transaction_period"] = (
        pd.to_datetime(result["transaction_date"])
        .dt.to_period("M")
    )

    return result