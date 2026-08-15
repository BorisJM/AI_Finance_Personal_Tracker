import datetime
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base
from models.transaction import Currency
from models.transaction import Transaction


class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    bank: Mapped["str"] = mapped_column(String(255))
    account_name: Mapped[str] = mapped_column(String(255), unique=True)
    currency: Mapped[Currency] = mapped_column(nullable=False)
    created_at: Mapped[datetime.date] # Upewnić się czy to wgl jest potrzebne
    # Account -> Transactions relationship one-to-many
    transaction: Mapped[List["Transaction"]] = relationship(back_populates="account")