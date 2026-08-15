from enum import Enum
import datetime
import decimal
from database.base import Base
from merchant import Merchant
from category import Category
from account import Account
from source_file import Import
from sqlalchemy.orm import mapped_column, Mapped, relationship
import sqlalchemy as db
from sqlalchemy import ForeignKey, String

# Currency ENUM class with options
class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"

class TransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[Currency]
    transaction_date: Mapped[datetime.date]
    amount: Mapped[decimal.Decimal]
    # Transaction -> Merchant MANY-to-ONE relationship
    merchant_id: Mapped[int] = mapped_column(ForeignKey("merchant.id"))
    merchant: Mapped["Merchant"] = relationship("Merchant", back_populates="transactions")
    original_description: Mapped[str] = mapped_column(String(255))
    cleaned_description: Mapped[str] = mapped_column(String(255))
    # Transaction -> Category MANY-to-ONE relationship
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="transactions")
    # Transaction -> Account MANY-to-ONE relationship
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship(back_populates="transactions")
    transaction_type: Mapped[TransactionType]
    # Transaction -> Import MANY-to-ONE relationship
    source_file_id: Mapped[int] = mapped_column(ForeignKey("source_file.id"), nullable=False)
    source_file: Mapped["Import"] = relationship(back_populates="transactions")
    counterparty_account: Mapped[str]
