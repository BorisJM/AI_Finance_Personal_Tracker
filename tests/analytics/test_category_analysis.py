import pandas as pd
import pytest

from src.analytics.category_analysis import (
    expenses_by_category,
    category_percentages,
    category_percentage_per_month,
    top_categories,
)


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "transaction_category": [
            "Groceries",
            "Groceries",
            "Shopping",
            "Food",
            "Income",
        ],
        "debit_amount": [
            -100.00,
            -50.00,
            -200.00,
            -50.00,
            0.00,
        ],
        "credit_amount": [
            0.00,
            0.00,
            0.00,
            0.00,
            3000.00,
        ],
        "transaction_month": [
            "January",
            "January",
            "January",
            "February",
            "February",
        ],
    })


def test_expenses_by_category(transactions_df):
    result = expenses_by_category(transactions_df)

    result = result.set_index("transaction_category")

    assert result.loc["Groceries", "debit_amount"] == -150.00
    assert result.loc["Shopping", "debit_amount"] == -200.00
    assert result.loc["Food", "debit_amount"] == -50.00

    assert "Income" not in result.index


def test_category_percentages(transactions_df):
    result = category_percentages(transactions_df)

    result = result.set_index("transaction_category")

    assert result.loc["Groceries", "percentage_of_total_expenses"] == pytest.approx(
        37.5
    )

    assert result.loc["Shopping", "percentage_of_total_expenses"] == pytest.approx(
        50.0
    )

    assert result.loc["Food", "percentage_of_total_expenses"] == pytest.approx(
        12.5
    )


def test_category_percentage_per_month(transactions_df):
    result = category_percentage_per_month(transactions_df)

    january = result[
        (result["transaction_month"] == "January")
        & (result["transaction_category"] == "Shopping")
    ].iloc[0]

    assert january["category_percentage_of_month"] == pytest.approx(57.14)


def test_top_categories(transactions_df):
    result = top_categories(transactions_df)

    assert result.iloc[0]["transaction_category"] == "Shopping"
    assert result.iloc[0]["percentage_of_total_expenses"] == pytest.approx(50.0)