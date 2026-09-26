import pandas as pd
from sqlalchemy.orm import Session

from database.models.transaction import Transaction
from database.repositories.transaction_repository import TransactionRepository


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