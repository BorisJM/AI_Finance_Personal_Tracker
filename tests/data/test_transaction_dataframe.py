import pandas as pd
from datetime import date
from decimal import Decimal

from database.models.account import Account
from database.models.category import Category
from database.models.enums import Currency, TransactionType
from database.models.merchant import Merchant
from database.models.transaction import Transaction
from src.data.transaction_dataframe import transaction_to_dataframe
from src.data.transaction_dataframe import get_transactions_dataframe
from src.data.transaction_dataframe import prepare_analytics_data
from src.analytics.spending_analysis import calculate_total_expenses
from src.analytics.income_analysis import calculate_total_income


def test_prepare_analytics_data():
    df = pd.DataFrame(
        {
            "transaction_date": [
                date(2026, 9, 1),
                date(2026, 9, 2),
            ],
            "amount": [
                Decimal("-100.50"),
                Decimal("5000.00"),
            ],
            "transaction_type": [
                "EXPENSE",
                "INCOME",
            ],
            "cleaned_description": [
                "Biedronka",
                "Wynagrodzenie",
            ],
            "category": [
                "Food",
                "Food"
            ]
        }
    )

    result = prepare_analytics_data(df)

    assert result.loc[0, "expense_amount"] == Decimal("100.50")
    assert result.loc[0, "income_amount"] == 0

    assert result.loc[1, "expense_amount"] == 0
    assert result.loc[1, "income_amount"] == Decimal("5000.00")

    assert result.loc[0, "description"] == "Biedronka"
    assert result.loc[1, "description"] == "Wynagrodzenie"

    assert str(result.loc[0, "transaction_period"]) == "2026-09"
    assert str(result.loc[1, "transaction_period"]) == "2026-09"
    assert result.loc[0, "debit_amount"] == Decimal("-100.50")
    assert result.loc[0, "credit_amount"] == 0
    assert result.loc[0, "transaction_category"] == "Food"
    assert result.loc[0, "transaction_description"] == "Biedronka"

    assert result.loc[1, "debit_amount"] == 0
    assert result.loc[1, "credit_amount"] == Decimal("5000.00")
    assert result.loc[1, "transaction_category"] == "Food"
    assert result.loc[1, "transaction_description"] == "Wynagrodzenie"

def test_transaction_to_dataframe():
    merchant = Merchant(
        name="Biedronka",
        normalized_name="biedronka",
        location="Bydgoszcz",
    )

    category = Category(
        name="Food",
        icon="food",
        color="#FFFFFF",
    )

    account = Account(
        bank="Millennium",
        account_name="123456789",
        currency=Currency.PLN,
    )

    transaction = Transaction(
        transaction_identifier="abc123",
        currency=Currency.PLN,
        transaction_date=date(2026, 9, 1),
        amount=Decimal("100.50"),
        merchant=merchant,
        original_description="Biedronka",
        cleaned_description="Biedronka",
        category=category,
        account=account,
        transaction_type=TransactionType.EXPENSE,
        source_file_id=1,
        counterparty_account="987654321",
    )

    df = transaction_to_dataframe([transaction])

    assert len(df) == 1
    assert df.loc[0, "transaction_date"] == date(2026, 9, 1)
    assert df.loc[0, "amount"] == Decimal("100.50")
    assert df.loc[0, "merchant"] == "Biedronka"
    assert df.loc[0, "category"] == "Food"
    assert df.loc[0, "account"] == "123456789"
    assert df.loc[0, "currency_code"] == "PLN"
    assert df.loc[0, "transaction_type"] == "EXPENSE"
    assert df.loc[0, "transaction_identifier"] == "abc123"

def test_get_transactions_dataframe(session):
    merchant = Merchant(
        name="Biedronka",
        normalized_name="biedronka",
        location="Bydgoszcz",
    )

    category = Category(
        name="Food",
        icon="food",
        color="#FFFFFF",
    )

    account = Account(
        bank="Millennium",
        account_name="123456789",
        currency=Currency.PLN,
        created_at=date(2026, 9, 1),
    )

    transaction = Transaction(
        transaction_identifier="db-test-123",
        currency=Currency.PLN,
        transaction_date=date(2026, 9, 1),
        amount=Decimal("100.50"),
        merchant=merchant,
        category=category,
        account=account,
        original_description="Biedronka",
        cleaned_description="Biedronka",
        transaction_type=TransactionType.EXPENSE,
        source_file_id=1,
        counterparty_account="987654321",
    )

    session.add_all([merchant, category, account, transaction])
    session.commit()

    df = get_transactions_dataframe(session)

    print(df.columns.tolist())
    print(df.head())
    print(df.shape)

    assert len(df) == 1
    assert df.loc[0, "merchant"] == "Biedronka"
    assert df.loc[0, "category"] == "Food"
    assert df.loc[0, "account"] == "123456789"
    assert df.loc[0, "amount"] == Decimal("100.50")

def test_database_dataframe_is_compatible_with_analytics(session):
    merchant = Merchant(
        name="Biedronka",
        normalized_name="biedronka",
        location="Bydgoszcz",
    )

    category = Category(
        name="Food",
        icon="food",
        color="#FFFFFF",
    )

    account = Account(
        bank="Millennium",
        account_name="123456789",
        currency=Currency.PLN,
        created_at=date(2026, 9, 1),
    )

    transaction_expense = Transaction(
        transaction_identifier="analytics-expense",
        currency=Currency.PLN,
        transaction_date=date(2026, 9, 1),
        amount=Decimal("-100.50"),
        merchant=merchant,
        category=category,
        account=account,
        original_description="Biedronka",
        cleaned_description="Biedronka",
        transaction_type=TransactionType.EXPENSE,
        source_file_id=1,
        counterparty_account="987654321",
    )

    transaction_income = Transaction(
        transaction_identifier="analytics-income",
        currency=Currency.PLN,
        transaction_date=date(2026, 9, 2),
        amount=Decimal("5000.00"),
        merchant=merchant,
        category=category,
        account=account,
        original_description="Wynagrodzenie",
        cleaned_description="Wynagrodzenie",
        transaction_type=TransactionType.INCOME,
        source_file_id=1,
        counterparty_account="987654321",
    )

    session.add_all([
        merchant,
        category,
        account,
        transaction_expense,
        transaction_income,
    ])
    session.commit()

    df = get_transactions_dataframe(session)
    df = prepare_analytics_data(df)

    assert calculate_total_expenses(df) == Decimal("100.50")
    assert calculate_total_income(df) == Decimal("5000.00")