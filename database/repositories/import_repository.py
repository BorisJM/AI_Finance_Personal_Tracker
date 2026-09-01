import datetime
from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from database.models.source_file import Import
from database.models.enums import Status
from database.models.transaction import Transaction

# ----------- BUSINESS LOGIC -----------
# 1. Create import
# 2. Get by id
# 3. Get by bank
# 4. Get import by date range (start_date, end_date)
# 5. Get by import status
# 6. Cant delete import
# 7. Update: bank, import_status

class ImportRepository:
    def __init__(self, session: Session):
        self.session = session

    # 1. Create Import
    def create_source_file(self, bank: str, transactions: list[Transaction]) -> Import:
        # Protection from 0 transactions
        if not transactions:
            raise ValueError("Transactions cannot be empty")
        # Current date
        created_at = datetime.datetime.now()
        # Last transaction date
        date = transactions[-1].transaction_date
        new_import = Import(bank=bank, date=date, created_at=created_at, transactions=transactions, rows_count=len(transactions))
        self.session.add(new_import)
        return new_import
    # 2. Get by ID
    def get_by_id(self, import_id: int) -> Import | None:
        source_file = self.session.get(Import, import_id)
        return source_file

    # 3. Get imports by BANK
    def get_by_bank(self, bank_name: str) -> list[Import]:
        stmt = select(Import).where(Import.bank == bank_name)
        result = self.session.execute(stmt).scalars().all()

        return result

    # 4. Get imports by date range
    def get_by_date_range(self, start_date: datetime.date | None = None, end_date: datetime.date | None = None) -> list[Import]:
        stmt = select(Import)
        # - Extra protection from bugs with dates
        if start_date is not None and end_date is not None:
            if end_date < start_date:
                raise ValueError("End date cannot be earlier than start date")
        # None passed
        if start_date is None and end_date is None:
            return self.session.execute(stmt).scalars().all()
        # start date and end date passed
        if start_date and end_date:
            stmt = stmt.where(Import.date >= start_date, Import.date <= end_date)
        # only start date
        if start_date and end_date is None:
            stmt = stmt.where(Import.date >= start_date)
        # only end date
        if end_date and start_date is None:
            stmt = stmt.where(Import.date <= end_date)
        result = self.session.execute(stmt).scalars().all()
        return result

    # 5. Get imports by Status
    def get_by_import_status(self, import_status: Status) -> list[Import]:
        stmt = select(Import).where(Import.import_status == import_status)
        result = self.session.execute(stmt).scalars().all()

        return result

    # 6. Update (bank, import_status)
    def update(self, import_id: int, import_status: Status | None = None, bank: str | None = None) -> Import | None:

        import_file = self.session.get(Import, import_id)
        if import_file is None:
            return None
        # If it exists than we update the fields that were passed
        if import_status is not None:
            import_file.import_status = import_status

        if bank is not None:
            import_file.bank = bank

        return import_file