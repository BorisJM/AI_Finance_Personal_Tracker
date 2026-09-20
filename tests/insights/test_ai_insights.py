import pandas as pd
import pytest

from src.insights.ai_insights import generate_ai_insights


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
            5000.00,
            0.00,
            0.00,
            0.00,
            5500.00,
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


def test_generate_ai_insights_returns_list(transactions_df):
    result = generate_ai_insights(transactions_df)

    assert isinstance(result, list)
    assert len(result) > 0


def test_generate_ai_insights_contains_insight_dicts(transactions_df):
    result = generate_ai_insights(transactions_df)

    for insight in result:
        assert isinstance(insight, dict)
        assert "type" in insight
        assert "title" in insight
        assert "message" in insight


def test_generate_ai_insights_combines_insights(transactions_df):
    result = generate_ai_insights(transactions_df)

    # Każdy moduł powinien dostarczyć przynajmniej jeden insight.
    assert len(result) >= 5