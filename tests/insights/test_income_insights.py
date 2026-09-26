import pandas as pd
import pytest

from src.insights.income_insights import income_insights


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "transaction_description": [
            "Salary",
            "Freelance",
            "Salary",
            "Freelance",
        ],
        "transaction_category": [
            "Income",
            "Income",
            "Income",
            "Income",
        ],
        "debit_amount": [
            0.00,
            0.00,
            0.00,
            0.00,
        ],
        "credit_amount": [
            5000.00,
            1000.00,
            5500.00,
            1500.00,
        ],
        "transaction_date": pd.to_datetime([
            "2026-01-05",
            "2026-01-15",
            "2026-02-05",
            "2026-02-15",
        ]),
        "transaction_month": [
            "January",
            "January",
            "February",
            "February",
        ],
    })


def test_income_insights_returns_list(transactions_df):
    result = income_insights(transactions_df)

    assert isinstance(result, list)
    assert len(result) > 0


def test_largest_income(transactions_df):
    result = income_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"].startswith("Largest income:")
    )

    assert "5500.00 zł" in insight["title"]
    assert insight["message"] == "salary"

def test_income_change_last_month(transactions_df):
    result = income_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"] == "Income has increased!"
    )

    assert "2026-01" in insight["message"]
    assert "2026-02" in insight["message"]
    assert "16.67%" in insight["message"]