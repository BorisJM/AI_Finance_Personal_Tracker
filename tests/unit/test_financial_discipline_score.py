from datetime import date
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

from database.models.enums import TransactionType
from database.services.import_service import ImportService
from src.analytics.financial_discipline_score import (
    calculate_budget_points,
    calculate_budget_utilization,
    calculate_fds,
    calculate_fds_from_transactions,
    calculate_monthly_expenses_for_fds,
    calculate_savings_point,
    calculate_stability_points,
    calculate_totals,
    get_financial_discipline_score,
    get_last_six_months_range,
    interpret_fds,
    is_internal_transfer,
    separate_transactions,
)

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "fixtures" / "millennium_sample.csv"


def make_transaction(amount, transaction_date=date(2026, 5, 10), category="Groceries"):
    """Fake transaction with the same shape as the ORM Transaction model."""
    amount = Decimal(str(amount))
    return SimpleNamespace(
        amount=amount,
        transaction_type=TransactionType.INCOME if amount > 0 else TransactionType.EXPENSE,
        transaction_date=transaction_date,
        # In the ORM model `category` is an object with a `name`, not a string
        category=SimpleNamespace(name=category),
    )


# --- Scoring functions ---

def test_interpret_fds():
    assert interpret_fds(39) == "Bad discipline"
    assert interpret_fds(40) == "Moderate discipline"
    assert interpret_fds(None) is None


def test_calculate_savings_point():
    assert calculate_savings_point(2000, 1900) == 10
    assert calculate_savings_point(2000, 1800) == 15
    assert calculate_savings_point(2000, 1600) == 35
    assert calculate_savings_point(0, 1000) is None


def test_calculate_savings_point_accepts_negative_expenses():
    # Expenses are stored as negative amounts in the database
    assert calculate_savings_point(2000, -1800) == 15


def test_calculate_savings_point_when_spending_more_than_income():
    assert calculate_savings_point(1000, -1200) == 0


def test_calculate_budget_points():
    assert calculate_budget_points(75) == 35
    assert calculate_budget_points(100) == 25
    assert calculate_budget_points(130) == 0
    assert calculate_budget_points(None) is None


def test_calculate_stability_points():
    assert calculate_stability_points([1000, 1000, 1000, 1000, 1000, 1000]) == 25
    assert calculate_stability_points([500, 1000, 1500, 1000, 500, 1500]) == 0
    assert calculate_stability_points([1000, 1200, 900]) is None
    assert calculate_stability_points(None) is None
    assert calculate_stability_points([0, 0, 0, 0, 0, 0]) is None


def test_calculate_fds():
    assert calculate_fds(30, 25, 20) == 75
    assert calculate_fds(30, None, 20) == 77
    assert calculate_fds(30, 25, None) is None


# --- Period ---

def test_last_six_months_range_skips_current_month():
    assert get_last_six_months_range(date(2026, 11, 24)) == (date(2026, 5, 1), date(2026, 10, 31))


def test_last_six_months_range_across_year_boundary():
    assert get_last_six_months_range(date(2026, 3, 15)) == (date(2025, 9, 1), date(2026, 2, 28))


# --- Transactions ---

def test_is_internal_transfer():
    assert is_internal_transfer(make_transaction(-50, category="Transfers")) is True
    assert is_internal_transfer(make_transaction(-50, category="Groceries")) is False


def test_separate_transactions_skips_transfers():
    salary = make_transaction(6000, category="Income")
    groceries = make_transaction(-100)
    transfer = make_transaction(-50, category="Transfers")

    income, expenses = separate_transactions([salary, groceries, transfer])

    assert income == [salary]
    assert expenses == [groceries]


def test_calculate_totals():
    income = [make_transaction(100), make_transaction(200)]
    expenses = [make_transaction(-100), make_transaction(-200)]

    assert calculate_totals(income, expenses) == (Decimal("300"), Decimal("-300"))


def test_monthly_expenses_month_without_expenses_counts_as_zero():
    start = date(2026, 5, 1)
    # Every month has a salary, but June has no expenses
    transactions = [make_transaction(5000, date(2026, m, 1), "Income") for m in range(5, 11)]
    expenses = [make_transaction(-1000, date(2026, m, 15)) for m in (5, 7, 8, 9, 10)]

    result = calculate_monthly_expenses_for_fds(transactions + expenses, expenses, start)

    assert result == [Decimal("1000"), Decimal("0"), Decimal("1000"),
                      Decimal("1000"), Decimal("1000"), Decimal("1000")]


def test_monthly_expenses_month_without_any_transactions_is_missing_data():
    start = date(2026, 5, 1)
    # No transactions at all in June -> probably not imported
    expenses = [make_transaction(-1000, date(2026, m, 15)) for m in (5, 7, 8, 9, 10)]

    assert calculate_monthly_expenses_for_fds(expenses, expenses, start) is None


def test_calculate_budget_utilization():
    assert calculate_budget_utilization([{"spent_percentage": 80}, {"spent_percentage": 100}]) == 90
    assert calculate_budget_utilization([]) is None


# --- Full score ---

def stable_profile():
    """6 months (May-Oct 2026): 5000 income, 4000 expenses, one transfer per month."""
    transactions = []
    for month in range(5, 11):
        transactions.append(make_transaction(5000, date(2026, month, 1), "Income"))
        transactions.append(make_transaction(-4000, date(2026, month, 10)))
        transactions.append(make_transaction(-3000, date(2026, month, 20), "Transfers"))
    return transactions


def test_full_score_without_budgets():
    result = calculate_fds_from_transactions(stable_profile(), today=date(2026, 11, 24))

    # Savings rate 20% -> 35 pts, identical months -> 25 pts, (35 + 25) / 65 -> 92
    assert result["savings_points"] == 35
    assert result["stability_points"] == 25
    assert result["budget_points"] is None
    assert result["score"] == 92
    assert result["label"] == "Perfect discipline"
    assert result["reason"] is None
    # Transfers (3000 / month) are not counted as expenses
    assert result["total_expenses"] == Decimal("24000")


def test_full_score_with_budgets():
    result = calculate_fds_from_transactions(stable_profile(), today=date(2026, 11, 24), budget_utilization=95)

    # 35 savings + 25 budget + 25 stability
    assert result["score"] == 85


def test_full_score_ignores_transactions_outside_period():
    transactions = stable_profile() + [make_transaction(-50000, date(2026, 11, 2))]

    result = calculate_fds_from_transactions(transactions, today=date(2026, 11, 24))

    assert result["score"] == 92


def test_full_score_without_income():
    expenses_only = [t for t in stable_profile() if t.transaction_type == TransactionType.EXPENSE]

    result = calculate_fds_from_transactions(expenses_only, today=date(2026, 11, 24))

    assert result["score"] is None
    assert result["reason"] == "No income in the last 6 months."


def test_full_score_from_database_with_too_little_history(session):
    # Sample CSV covers only July-September 2026
    ImportService(session).import_transactions(SAMPLE_CSV)

    result = get_financial_discipline_score(session, today=date(2026, 10, 15))

    assert result["score"] is None
    assert result["reason"] == "Missing transactions for at least one of the last 6 months."
    assert result["total_income"] > 0
