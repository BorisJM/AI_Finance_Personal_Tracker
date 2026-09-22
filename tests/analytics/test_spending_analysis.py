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
    add_transaction_period

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
        "transaction_date": pd.to_datetime([
            "2026-01-10",
            "2026-01-15",
            "2026-01-20",
            "2026-02-10",
        ]),
    })


def test_calculate_total_expenses(transactions_df):
    result = calculate_total_expenses(transactions_df)

    assert result == 475.00


def test_calculate_biggest_expenses(transactions_df):
    result = calculate_biggest_expenses(transactions_df)

    assert len(result) == 4
    assert result.iloc[0]["expense_amount"] == 300.00


def test_calculate_average_monthly_expense(transactions_df):
    result = calculate_average_monthly_expense(transactions_df)

    assert result == 237.50


def test_calculate_monthly_expenses(transactions_df):
    result = calculate_monthly_expenses(transactions_df)

    january = result[
        result["transaction_period"] == pd.Period("2026-01")
    ].iloc[0]

    february = result[
        result["transaction_period"] == pd.Period("2026-02")
    ].iloc[0]

    assert january["expense_amount"] == 450.00
    assert february["expense_amount"] == 25.00

def test_calculate_monthly_expense_growth_rate(transactions_df):
    result = calculate_monthly_expense_growth_rate(transactions_df)

    february = result[
        result["transaction_period"] == pd.Period("2026-02")
    ].iloc[0]

    # January: -450
    # February: -25
    # (-25 - (-450)) / -450 * 100 = -94.444...
    assert february["expense_growth_rate"] == pytest.approx(
        -94.4444444
    )


def test_calculate_month_savings(transactions_df):
    result = calculate_month_savings(transactions_df)

    january = result[
        result["transaction_period"] == pd.Period("2026-01")
    ].iloc[0]

    february = result[
        result["transaction_period"] == pd.Period("2026-02")
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
    assert result.iloc[0]["expense_amount"] == 300.00

def test_calculate_month_savings_with_zero_income():
    df = pd.DataFrame({
        "transaction_date": pd.to_datetime(["2026-01-15"]),
        "debit_amount": [-500.00],
        "credit_amount": [0.00],
    })

    result = calculate_month_savings(df)

    assert result.iloc[0]["month_savings"] == -500.00

def test_calculate_savings_rate_with_zero_income():
    df = pd.DataFrame({
        "transaction_date": pd.to_datetime(["2026-01-15"]),
        "debit_amount": [-500.00],
        "credit_amount": [0.00],
    })

    result = calculate_savings_rate(df)

    assert result == 0


def test_add_transaction_period():
    df = pd.DataFrame({
        "transaction_date": pd.to_datetime([
            "2026-01-15",
            "2026-02-20",
            "2027-01-05",
        ])
    })

    result = add_transaction_period(df)

    assert str(result.iloc[0]["transaction_period"]) == "2026-01"
    assert str(result.iloc[1]["transaction_period"]) == "2026-02"
    assert str(result.iloc[2]["transaction_period"]) == "2027-01"

def test_calculate_monthly_expenses_separates_same_month_different_year():
    df = pd.DataFrame({
        "transaction_date": pd.to_datetime([
            "2026-01-10",
            "2027-01-10",
        ]),
        "debit_amount": [
            -100.00,
            -200.00,
        ],
        "credit_amount": [
            0.00,
            0.00,
        ],
    })

    result = calculate_monthly_expenses(df)

    assert len(result) == 2
    assert result.iloc[0]["expense_amount"] == 100.00
    assert result.iloc[1]["expense_amount"] == 200.00