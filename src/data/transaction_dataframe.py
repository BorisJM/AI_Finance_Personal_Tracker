import pandas as pd
from sqlalchemy.orm import Session

from database.models.transaction import Transaction
from database.repositories.transaction_repository import TransactionRepository

# Helper function to prepare data for analytics
def prepare_analytics_data(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["amount"] = result["amount"].astype(float)
    result["debit_amount"] = result["amount"].where(
        result["transaction_type"] == "EXPENSE",
        0
    )

    result["credit_amount"] = result["amount"].where(
        result["transaction_type"] == "INCOME",
        0
    )

    result["transaction_category"] = result["category"]
    result["transaction_description"] = result["cleaned_description"]

    result["expense_amount"] = result["debit_amount"].abs()
    result["income_amount"] = result["credit_amount"]

    result["description"] = result["cleaned_description"]

    result["transaction_period"] = (
        pd.to_datetime(result["transaction_date"])
        .dt.to_period("M")
    )

    return result

def transaction_to_dataframe(transactions: list[Transaction]) -> pd.DataFrame:
    rows = []

    for transaction in transactions:
        rows.append({
            "transaction_date": transaction.transaction_date,
            "amount": transaction.amount,
            "merchant": transaction.merchant.name,
            "original_description": transaction.original_description,
            "cleaned_description": transaction.cleaned_description,
            "category": transaction.category.name,
            "account": transaction.account.account_name,
            "currency_code": transaction.currency.value,
            "transaction_type": transaction.transaction_type.value,
            "source_file_id": transaction.source_file_id,
            "counterparty_account": transaction.counterparty_account,
            "transaction_identifier": transaction.transaction_identifier,
        })

    return pd.DataFrame(rows)

def get_transactions_dataframe(session: Session) -> pd.DataFrame:
    repository = TransactionRepository(session)
    transactions = repository.get_all()
    return transaction_to_dataframe(transactions)