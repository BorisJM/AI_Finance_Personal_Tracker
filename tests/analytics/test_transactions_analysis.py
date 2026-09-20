import pandas as pd
import pytest

from src.analytics.transactions_analysis import (
    get_last_transactions,
    get_average_transaction_value,
)


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "transaction_date": pd.to_datetime([
            "2026-01-01",
            "2026-01-02",
            "2026-01-03",
            "2026-01-04",
            "2026-01-05",
        ]),
        "transaction_description": [
            "Transaction 1",
            "Transaction 2",
            "Transaction 3",
            "Transaction 4",
            "Transaction 5",
        ],
        "transaction_category": [
            "Food",
            "Groceries",
            "Shopping",
            "Transport",
            "Food",
        ],
        "debit_amount": [
            -20.00,
            -50.00,
            -100.00,
            -30.00,
            -40.00,
        ],
        "counterparty_account": [
            "111",
            "222",
            "333",
            "444",
            "555",
        ],
        "counterparty_name": [
            "Seller 1",
            "Seller 2",
            "Seller 3",
            "Seller 4",
            "Seller 5",
        ],
        "account_balance": [
            5000.00,
            4950.00,
            4850.00,
            4820.00,
            4780.00,
        ],
        "currency_code": [
            "PLN",
            "PLN",
            "PLN",
            "PLN",
            "PLN",
        ],
    })


def test_get_last_transactions_returns_last_10(transactions_df):
    result = get_last_transactions(transactions_df)

    assert len(result) == 5
    assert result.iloc[-1]["transaction_description"] == "Transaction 5"


def test_get_last_transactions_sorted_by_date(transactions_df):
    shuffled_df = transactions_df.sample(frac=1, random_state=42)

    result = get_last_transactions(shuffled_df)

    dates = result["transaction_date"].tolist()

    assert dates == sorted(dates)


def test_get_last_transactions_removes_sensitive_columns(transactions_df):
    result = get_last_transactions(transactions_df)

    assert "counterparty_account" not in result.columns
    assert "counterparty_name" not in result.columns
    assert "account_balance" not in result.columns
    assert "currency_code" not in result.columns


def test_get_average_transaction_value(transactions_df):
    result = get_average_transaction_value(transactions_df)

    assert result == pytest.approx(-48.00)