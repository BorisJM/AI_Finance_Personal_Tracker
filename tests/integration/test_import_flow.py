from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.base import Base
from database.models.transaction import Transaction
from database.models.source_file import Import
from database.services.import_service import ImportService
from src.data.transaction_dataframe import (
    get_transactions_dataframe,
    prepare_analytics_data,
)
from src.analytics.spending_analysis import calculate_total_expenses, calculate_monthly_expenses
from src.analytics.income_analysis import calculate_total_income, calculate_monthly_income
from src.insights.ai_insights import generate_ai_insights

# Synthetic Millennium export (fake accounts, 24 rows, the last row is an exact duplicate).
# Real bank exports stay in data/raw/ and are never used by tests.
SAMPLE_CSV = Path(__file__).resolve().parents[1] / "fixtures" / "millennium_sample.csv"
EXPECTED_TRANSACTIONS = 23


def test_import_flow():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        service = ImportService(session)

        service.import_transactions(SAMPLE_CSV)

        transactions = session.scalars(
            select(Transaction)
        ).all()

        imports = session.scalars(
            select(Import)
        ).all()

        assert len(transactions) == EXPECTED_TRANSACTIONS
        assert len(imports) == 1

        assert all(
            transaction.transaction_identifier
            for transaction in transactions
        )

        assert all(
            transaction.category_id is not None
            for transaction in transactions
        )

        assert all(
            transaction.merchant_id is not None
            for transaction in transactions
        )

    engine.dispose()


def test_reimporting_same_file_does_not_duplicate_transactions():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        service = ImportService(session)

        service.import_transactions(SAMPLE_CSV)
        service.import_transactions(SAMPLE_CSV)

        transactions = session.scalars(select(Transaction)).all()
        imports = session.scalars(select(Import)).all()

        assert len(transactions) == EXPECTED_TRANSACTIONS
        # Every import attempt is recorded, even when it adds nothing new
        assert len(imports) == 2

    engine.dispose()


def test_import_to_analytics_flow():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        service = ImportService(session)
        service.import_transactions(SAMPLE_CSV)

        df = get_transactions_dataframe(session)
        df = prepare_analytics_data(df)

        assert len(df) == EXPECTED_TRANSACTIONS

        total_expenses = calculate_total_expenses(df)
        total_income = calculate_total_income(df)

        assert total_expenses > 0
        assert total_income > 0

        monthly_expenses = calculate_monthly_expenses(df)
        monthly_income = calculate_monthly_income(df)

        assert not monthly_expenses.empty
        assert not monthly_income.empty

    engine.dispose()


def test_import_to_ai_insights_flow():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        service = ImportService(session)
        service.import_transactions(SAMPLE_CSV)

        df = get_transactions_dataframe(session)
        df = prepare_analytics_data(df)

        insights = generate_ai_insights(df)

        assert isinstance(insights, list)
        assert len(insights) > 0

        for insight in insights:
            assert isinstance(insight, dict)
            assert "type" in insight
            assert "title" in insight
            assert "message" in insight
    engine.dispose()
