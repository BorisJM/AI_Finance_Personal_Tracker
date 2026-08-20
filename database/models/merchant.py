from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


class Merchant(Base):
    __tablename__ = "merchant"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255))
    # Transaction relationship
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="merchant")