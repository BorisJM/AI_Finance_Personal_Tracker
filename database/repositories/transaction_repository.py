import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models.enums import Currency
from database.models.transaction import Transaction
from database.models.category import Category
from database.models.merchant import Merchant
from database.models.account import Account
from models.enums import TransactionType


# ----------- BUSINESS LOGIC -----------
# 1. Create transaction
# 2. Get all transactions
# - Find transaction by transaction type
# - Get transaction by category
# - Get transaction by date after
# - Get transaction by date before
# - Get transaction by merchant
# - Get transaction by account
# - Get transaction by counterparty account equals to
# - Get transaction by cleaned description including some text
# - Find transactions by amount greater than
# - Find transactions by amount lower than
# 3. Get by ID

# UPDATE - Allowed fields
# - Merchant
# - Cleaned description
# - Category

class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    # 1. Create transaction
    def create(self, currency: Currency, transaction_date: datetime.date, amount: Decimal, merchant_id: int, original_description: str,
               cleaned_description: str, category_id: int, account_id: int, transaction_type: TransactionType, source_file_id: int, counterparty_account: str) -> Transaction:
        new_transaction = Transaction(currency=currency, transaction_date=transaction_date, amount=amount, merchant_id=merchant_id, original_description=original_description,
                                      cleaned_description=cleaned_description, category_id=category_id, account_id=account_id, transaction_type=transaction_type,
                                      source_file_id=source_file_id, counterparty_account=counterparty_account)

        self.session.add(new_transaction)
        return new_transaction

    # 2. Get all transactions
    def get_all(self, category_name: str | None = None, start_date: datetime.date | None = None, end_date: datetime.date | None = None, merchant_name: str | None = None, account_name: str | None = None,
                counterparty_account: str | None = None, cleaned_description_text: str | None = None, min_amount: Decimal | None = None, max_amount: Decimal | None = None) -> list[Transaction]:
        # Create a base query that will be filtered
        # - Category filter
        stmt = select(Transaction)
        if category_name is not None:
            stmt = stmt.join(Transaction.category).where(
                Category.name == category_name
            )

        # - Start date filter
        if start_date is not None:
            stmt = stmt.where(Transaction.transaction_date >= start_date)
        # - End date filter
        if end_date is not None:
            stmt = stmt.where(Transaction.transaction_date <= end_date)
        # - Extra protection from bugs with dates
        if start_date is not None and end_date is not None:
            if end_date < start_date:
                raise ValueError("End date cannot be earlier than start date")
        # - Merchant Name filter
        if merchant_name is not None:
            stmt = stmt.join(Transaction.merchant).where(Merchant.name == merchant_name)
        # - Account name filter
        if account_name is not None:
            stmt = stmt.join(Transaction.account).where(Account.account_name == account_name)
        # - Counterparty account filter
        if counterparty_account is not None:
            stmt = stmt.where(Transaction.counterparty_account == counterparty_account)
        # - Cleaned description includes text filter
        if cleaned_description_text is not None:
            stmt = stmt.where(Transaction.cleaned_description.contains(cleaned_description_text))
        # - Min amount
        if min_amount is not None:
            stmt = stmt.where(Transaction.amount >= min_amount)
        # - Max amount
        if max_amount is not None:
            stmt = stmt.where(Transaction.amount <= max_amount)
        if min_amount is not None and max_amount is not None:
            if max_amount < min_amount:
                raise ValueError("Maximum amount cannot be less than minimum amount")
        found_transactions = self.session.execute(stmt).scalars().all()
        return found_transactions

    # 3. Get by ID transaction
    def get_by_id(self, transaction_id: int) -> Transaction | None:
        transaction = self.session.get(Transaction, transaction_id)

        if transaction is None:
            print("Transaction not found")
            return None
        else:
            return transaction

    # 4. Update transaction
    def update(self, transaction_id, new_merchant_id: int | None = None, new_category_id: int | None = None, cleaned_description: str | None = None) -> Transaction | None:
        stmt = select(Transaction).where(Transaction.id == transaction_id)
        updated_transaction = self.session.execute(stmt).scalar_one_or_none()

        if updated_transaction is None:
            return None
        # Update merchant
        if new_merchant_id is not None:
            updated_transaction.merchant_id = new_merchant_id
        # Update category
        if new_category_id is not None:
            updated_transaction.category_id = new_category_id
        # Update description
        if cleaned_description is not None:
            updated_transaction.cleaned_description = cleaned_description

        return updated_transaction