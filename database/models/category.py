from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from base import Base
from models.budget import Budget
from models.transaction import Transaction


class Colors(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    icon: Mapped[str] = mapped_column(String(255), unique=True)
    color: Mapped[Colors]
    # Category -> Transactions relationship One-to-Many
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="category")
    # Budget relationship One-To-Many
    budget: Mapped[list["Budget"]] = relationship(back_populates="category")
