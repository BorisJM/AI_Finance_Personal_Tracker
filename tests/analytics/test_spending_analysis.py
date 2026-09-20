import pandas as pd
import pytest

from src.analytics.spending_analysis import (
    calculate_total_expenses,
    calculate_biggest_expenses,
    calculate_average_monthly_expense,
    calculate_monthly_expenses,
    calculate_monthly_expense_growth_rate,
    calculate_month_savings,
    calculate_savings_rate,
    top_transactions,
)


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "transaction_description": [
            "Biedronka",
            "Lidl",
            "Allegro",
            "Biedronka",
        ],
        "transaction_category": [
            "Groceries",
            "Groceries",
            "Shopping",
            "Groceries",
        ],
        "debit_amount": [
            -100.00,
            -50.00,
            -300.00,
            -25.00,
        ],
        "credit_amount": [
            0.00,
            0.00,
            0.00,
            0.00,
        ],
        "transaction_month": [
            "January",
            "January",
            "January",
            "February",
        ],
    })


def test_calculate_total_expenses(transactions_df):
    result = calculate_total_expenses(transactions_df)

    assert result == -475.00


def test_calculate_biggest_expenses(transactions_df):
    result = calculate_biggest_expenses(transactions_df)

    assert len(result) == 4
    assert result.iloc[0]["debit_amount"] == -300.00


def test_calculate_average_monthly_expense(transactions_df):
    result = calculate_average_monthly_expense(transactions_df)

    assert result == -237.50


def test_calculate_monthly_expenses(transactions_df):
    result = calculate_monthly_expenses(transactions_df)

    january = result[result["transaction_month"] == "January"].iloc[0]
    february = result[result["transaction_month"] == "February"].iloc[0]

    assert january["debit_amount"] == -450.00
    assert february["debit_amount"] == -25.00


def test_calculate_monthly_expense_growth_rate(transactions_df):
    result = calculate_monthly_expense_growth_rate(transactions_df)

    february = result[
        result["transaction_month"] == "February"
    ].iloc[0]

    # January: -450
    # February: -25
    # (-25 - (-450)) / -450 * 100 = -94.444...
    assert february["trend_expense_percentage"] == pytest.approx(
        -94.4444444
    )


def test_calculate_month_savings(transactions_df):
    result = calculate_month_savings(transactions_df)

    january = result[
        result["transaction_month"] == "January"
    ].iloc[0]

    february = result[
        result["transaction_month"] == "February"
    ].iloc[0]

    # January:
    # income = 0
    # expenses = -450
    # savings = -450

    assert january["month_savings"] == -450.00

    # February:
    # income = 0
    # expenses = -25
    # savings = -25

    assert february["month_savings"] == -25.00


def test_calculate_savings_rate(transactions_df):
    result = calculate_savings_rate(transactions_df)

    # No income in the fixture.
    # Therefore savings rate should be 0.

    assert result == 0


def test_top_transactions(transactions_df):
    result = top_transactions(transactions_df)

    assert len(result) == 4

    # Largest transaction = 300 zł
    assert result.iloc[0]["debit_amount"] == 300.00