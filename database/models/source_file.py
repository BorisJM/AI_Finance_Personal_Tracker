import datetime
from enum import Enum
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction
from ..base import Base
from .enums import Status

class Import(Base):
    __tablename__ = "source_file"
    id: Mapped[int] = mapped_column(primary_key=True)
    bank: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    import_status: Mapped[Status]
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
    rows_count: Mapped[int]
    # Transactions relationship
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="source_file")