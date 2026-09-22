import pandas as pd
import pytest

from src.analytics.income_analysis import (
    calculate_total_income,
    calculate_monthly_income,
    calculate_monthly_income_growth_rate,
)


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "credit_amount": [
            3000.00,
            500.00,
            2500.00,
            1000.00,
        ],
        "transaction_date": pd.to_datetime([
            "2026-01-10",
            "2026-01-20",
            "2026-02-10",
            "2026-02-20",
        ]),
    })


def test_calculate_total_income(transactions_df):
    result = calculate_total_income(transactions_df)

    assert result == 7000.00


def test_calculate_monthly_income(transactions_df):
    result = calculate_monthly_income(transactions_df)

    january = result[
        result["transaction_period"] == pd.Period("2026-01")
    ].iloc[0]

    february = result[
        result["transaction_period"] == pd.Period("2026-02")
    ].iloc[0]

    assert january["monthly_income"] == 3500.00
    assert february["monthly_income"] == 3500.00


def test_calculate_monthly_income_growth_rate(transactions_df):
    result = calculate_monthly_income_growth_rate(transactions_df)

    february = result[
        result["transaction_period"] == pd.Period("2026-02")
    ].iloc[0]

    assert february["income_growth_rate"] == 0.0


def test_calculate_monthly_income_separates_same_month_different_year():
    df = pd.DataFrame({
        "transaction_date": pd.to_datetime([
            "2026-01-10",
            "2027-01-10",
        ]),
        "credit_amount": [
            1000.00,
            2000.00,
        ],
    })

    result = calculate_monthly_income(df)

    assert len(result) == 2
    assert result.iloc[0]["monthly_income"] == 1000.00
    assert result.iloc[1]["monthly_income"] == 2000.00