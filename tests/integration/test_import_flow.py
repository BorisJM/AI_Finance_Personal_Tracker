from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.base import Base
from database.models.transaction import Transaction
from database.models.source_file import Import
from database.services.import_service import ImportService


def test_import_flow():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    csv_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "raw"
        / "transactions.csv"
    )

    with Session(engine) as session:
        service = ImportService(session)

        service.import_transactions(csv_path)

        transactions = session.scalars(
            select(Transaction)
        ).all()

        imports = session.scalars(
            select(Import)
        ).all()

        assert len(transactions) == 239
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