import pandas as pd
import pytest

from src.insights.waste_insights import waste_insights


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "transaction_description": [
            "Biedronka",
            "Biedronka",
            "Biedronka",
            "Biedronka",
            "Biedronka",
            "Allegro",
            "Uber",
        ],
        "transaction_category": [
            "Groceries",
            "Groceries",
            "Groceries",
            "Groceries",
            "Groceries",
            "Shopping",
            "Transport",
        ],
        "debit_amount": [
            -10.00,
            -12.00,
            -8.00,
            -15.00,
            -5.00,
            -200.00,
            -50.00,
        ],
        "credit_amount": [
            0.00,
            0.00,
            0.00,
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
            "February",
            "February",
            "February",
        ],
    })


def test_waste_insights_returns_list(transactions_df):
    result = waste_insights(transactions_df)

    assert isinstance(result, list)


def test_waste_insights_detects_frequent_small_expenses(transactions_df):
    result = waste_insights(transactions_df)

    assert len(result) > 0


def test_waste_insights_structure(transactions_df):
    result = waste_insights(transactions_df)

    if result:
        insight = result[0]

        assert "type" in insight
        assert "title" in insight
        assert "message" in insight