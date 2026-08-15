import datetime
from enum import Enum
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from transaction import Transaction
from database.base import Base

class Status(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    PENDING = 'PENDING'


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