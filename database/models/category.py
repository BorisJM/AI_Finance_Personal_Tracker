from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from ..base import Base
from typing import TYPE_CHECKING
from .enums import Colors

if TYPE_CHECKING:
    from .budget import Budget

if TYPE_CHECKING:
    from .transaction import Transaction


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    icon: Mapped[str] = mapped_column(String(255), unique=True)
    color: Mapped[Colors]
    # Category -> Transactions relationship One-to-Many
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="category")
    # Budget relationship One-To-Many
    budgets: Mapped[list["Budget"]] = relationship("Budget", back_populates="category")
