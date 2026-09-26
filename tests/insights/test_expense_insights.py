import pandas as pd
import pytest

from src.insights.expense_insights import expense_insights


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        "transaction_description": [
            "Biedronka",
            "Lidl",
            "Allegro",
            "Biedronka",
            "Uber",
            "Allegro",
        ],
        "transaction_category": [
            "Groceries",
            "Groceries",
            "Shopping",
            "Groceries",
            "Transport",
            "Shopping",
        ],
        "debit_amount": [
            -100.00,
            -50.00,
            -300.00,
            -200.00,
            -80.00,
            -150.00,
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
            "2026-02-05",
            "2026-02-10",
            "2026-02-15",
        ]),
    })


def test_expense_insights_returns_list(transactions_df):
    result = expense_insights(transactions_df)

    assert isinstance(result, list)
    assert len(result) > 0


def test_most_expensive_category(transactions_df):
    result = expense_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"] == "Most expensive category"
    )

    assert "Shopping" in insight["message"]


def test_largest_expense(transactions_df):
    result = expense_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"] == "Largest expense"
    )

    assert "300" in insight["message"]


def test_spending_vs_income_with_zero_income():
    df = pd.DataFrame({
        "transaction_description": ["Biedronka"],
        "transaction_category": ["Groceries"],
        "debit_amount": [-100.00],
        "credit_amount": [0.00],
        "transaction_date": pd.to_datetime(["2026-02-05"]),
    })

    result = expense_insights(df)

    insight = next(
        x for x in result
        if x["title"] == "Spending vs income"
    )

    assert "0%" in insight["message"]

def test_category_spending_increase(transactions_df):
    result = expense_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"].endswith("spending increased")
    )

    assert insight["type"] == "warning"
    assert "increased by" in insight["message"]


def test_category_spending_decrease(transactions_df):
    result = expense_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"].endswith("spending decreased")
    )

    assert insight["type"] == "info"
    assert "decreased by" in insight["message"]


def test_most_expensive_day(transactions_df):
    result = expense_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"] == "Most expensive day of the week"
    )

    assert "Thursday" in insight["message"]


def test_most_money_spent_seller(transactions_df):
    result = expense_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"] == "Most money spent seller"
    )

    assert "Allegro" in insight["message"]


def test_highest_spending_month(transactions_df):
    result = expense_insights(transactions_df)

    insight = next(
        x for x in result
        if x["title"] == "Highest spending month"
    )

    assert "2026-01" in insight["message"]