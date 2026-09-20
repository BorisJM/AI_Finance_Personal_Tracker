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
        "transaction_month": [
            "January",
            "January",
            "February",
            "February",
        ],
    })


def test_calculate_total_income(transactions_df):
    result = calculate_total_income(transactions_df)

    assert result == 7000.00


def test_calculate_monthly_income(transactions_df):
    result = calculate_monthly_income(transactions_df)

    january = result[result["transaction_month"] == "January"].iloc[0]
    february = result[result["transaction_month"] == "February"].iloc[0]

    assert january["monthly_income"] == 3500.00
    assert february["monthly_income"] == 3500.00


def test_calculate_monthly_income_growth_rate(transactions_df):
    result = calculate_monthly_income_growth_rate(transactions_df)

    february = result[result["transaction_month"] == "February"].iloc[0]

    assert february["month_growth_rate"] == 0.0