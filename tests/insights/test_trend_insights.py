import pandas as pd
import pytest

from src.insights.trend_insights import trend_insights


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "transaction_description": [
            "Biedronka",
            "Lidl",
            "Allegro",
            "Uber",
            "Biedronka",
            "Allegro",
        ],
        "transaction_category": [
            "Groceries",
            "Groceries",
            "Shopping",
            "Transport",
            "Groceries",
            "Shopping",
        ],
        "debit_amount": [
            -100.00,
            -80.00,
            -500.00,
            -50.00,
            -120.00,
            -200.00,
        ],
        "credit_amount": [
            0.00,
            0.00,
            0.00,
            0.00,
            0.00,
            0.00,
        ],
        "transaction_date": pd.to_datetime([
            "2026-01-05",
            "2026-01-10",
            "2026-01-15",
            "2026-01-20",
            "2026-02-05",
            "2026-02-15",
        ]),
        "transaction_month": [
            "January",
            "January",
            "January",
            "January",
            "February",
            "February",
        ],
    })


def test_trend_insights_returns_list(transactions_df):
    result = trend_insights(transactions_df)

    assert isinstance(result, list)

def test_trend_insights_detects_unusual_expense(transactions_df):
    result = trend_insights(transactions_df)

    assert len(result) > 0

def test_trend_insights_structure(transactions_df):
    result = trend_insights(transactions_df)

    if result:
        insight = result[0]

        assert "type" in insight
        assert "title" in insight
        assert "message" in insight