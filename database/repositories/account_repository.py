import datetime

from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from database.models.account import Account
from database.models.enums import Currency
from database.models.transaction import Transaction

# AccountRepository
# 1. get_by_id()
# 2. get_by_bank()
# 3. get_by_account_name()
# 4. create()
# 5. update()
# 6. delete()
# 7. get_by_date_created_at_after(start_date)

class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    # 1. Get by ID
    def get_by_id(self, account_id: int) -> Account | None:
        stmt = select(Account).where(Account.id == account_id)
        account = self.session.execute(stmt).scalar_one_or_none()

        return account

    # 2. Get by bank
    def get_by_bank(self, bank_name: str) -> list[Account]:
        stmt = select(Account).where(Account.bank == bank_name)
        accounts = self.session.execute(stmt).scalars().all()

        return accounts

    # 3. Get by account name
    def get_by_account_name(self, account_name: str) -> Account | None:
        stmt = select(Account).where(Account.account_name == account_name)
        account = self.session.execute(stmt).scalar_one_or_none()

        return account

    # 4. Create account
    def create(self, bank: str, account_name: str, currency: Currency, created_at: datetime.date) -> Account:
        new_account = Account(account_name=account_name, bank=bank, currency=currency, created_at=created_at)
        self.session.add(new_account)

        return new_account

    # 5. Update account
    def update(self, account_id: int, account_name: str | None = None, currency: Currency | None = None) -> Account | None:
        stmt = select(Account).where(Account.id == account_id)
        updated_account = self.session.execute(stmt).scalar_one_or_none()
        if updated_account is None:
            return None

        if account_name is not None:
            updated_account.account_name = account_name
        if currency is not None:
            updated_account.currency = currency
        return updated_account

    # 6. Delete account
    def delete(self, account_id: int):
        account = self.session.get(Account, account_id)

        if account is None:
            return False

        # We can delete account only when it has no transactions assigned
        transaction_exists = self.session.scalar(
            select(
                select(Transaction).where(Transaction.account.id == account_id).exists()
            )
        )
        if transaction_exists:
            return False

        self.session.delete(account)
        return True