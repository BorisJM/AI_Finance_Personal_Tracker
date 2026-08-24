from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database.models.category import Category
from database.models.transaction import Transaction
from database.models.budget import Budget
from models.enums import Colors


# ----------- BUSINESS LOGIC -----------
# 1. Find by ID
# 2. Find by Name of Category
# 3. Create category
# 4. Update category
# 5. Delete category when - CONDITION 1: Not assigned to any Transactions, CONDITION 2: Not assigned to any Budget
# 6. Get all categories

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    # 1. Find by ID
    def get_by_id(self, category_id: int) -> Category | None:
        stmt = select(Category).where(Category.id == id)
        found_category = self.session.execute(stmt).scalar_one_or_none()
        return found_category

    # 2. Find by Name
    def get_by_name(self, name: str) -> Category | None:
        stmt = select(Category).where(Category.name == name)
        found_category = self.session.execute(stmt).scalar_one_or_none()
        return found_category

    # 3. Get all categories
    def get_all(self) -> list[Category]:
        stmt = select(Category)
        all_categories = self.session.execute(stmt).scalars().all()

        return all_categories

    # 4. Create category
    def create(self, name: str, icon: str, color: Colors) -> Category:
        new_category = Category(name=name, icon=icon, color=color)
        self.session.add(new_category)
        return new_category

    # 5. Update category
    def update(self, category_id: int, name: str | None = None, icon: str | None = None, color: Colors | None = None) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        found_category = self.session.execute(stmt).scalar_one_or_none()
        if found_category is None:
            return None

        if name is not None:
            found_category.name = name
        if icon is not None:
            found_category.icon = icon
        if color is not None:
            found_category.color = color

        return found_category

     # 6. Delete category when - CONDITION 1: Not assigned to any Transactions, CONDITION 2: Not assigned to any Budget
    def delete(self, category_id: int) -> bool:
        # Check if category exists
        # If no then return -> FALSE
        category = self.session.execute(select(Category).where(Category.id == category_id)).scalar_one_or_none()
        if category is None:
            return False
        stmt_transaction = select(Transaction).where(Transaction.category_id == category_id).exists()
        found_transaction = self.session.scalar(stmt_transaction)
        # Check if any transaction has CATEGORY
        # If it does then we return False
        if found_transaction:
            return False
        stmt_budget = select(Budget).where(Budget.category_id == category_id).exists()
        found_budget = self.session.scalar(stmt_budget)
        # Check if any budget has CATEGORY
        # If it does then we return False
        if found_budget:
            return False

        # Else delete the category
        self.session.delete(category)

        return True