import datetime
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction
from .enums import Currency

class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    bank: Mapped["str"] = mapped_column(String(255))
    account_name: Mapped[str] = mapped_column(String(255), unique=True)
    currency: Mapped[Currency] = mapped_column(nullable=False)
    created_at: Mapped[datetime.date]
    # Account -> Transactions relationship one-to-many
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="account")