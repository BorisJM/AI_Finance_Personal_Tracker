from sqlalchemy.orm import Session
from decimal import Decimal
from database.repositories.budget_repository import BudgetRepository
import datetime

from database.models.enums import TransactionType
from database.repositories.transaction_repository import TransactionRepository
from database.repositories.category_repository import CategoryRepository


class BudgetService:
    def __init__(self, session: Session):
        self.session = session

        self.budget_repo = BudgetRepository(session)
        self.transaction_repo = TransactionRepository(session)
        self.category_repo = CategoryRepository(session)
    # 1. Create budget
    def create_budget(self, monthly_limit: Decimal, start_date: datetime.date, end_date: datetime.date, category_id: int | None = None):
        budget = self.budget_repo.create_budget(monthly_limit=monthly_limit, start_date=start_date, end_date=end_date, category_id=category_id)

        self.session.commit()

        return budget

    # 2. Get budget
    def get_budget(self, budget_id: int):
        return self.budget_repo.get_by_id(budget_id)
    # 3. Get budgets by category
    def get_budgets_by_category(self, category_name: str):
        return self.budget_repo.get_by_category_name(category_name)
    # 4. Get budgets by date range
    def get_budgets_by_date_range(self, start_date: datetime.date | None = None, end_date: datetime.date | None = None):
        return self.budget_repo.get_by_date_range(start_date, end_date)
    # 5. Delete budget
    def delete_budget(self, budget_id: int):
        deleted_budget = self.budget_repo.delete_budget(budget_id)
        if deleted_budget:
            self.session.commit()

        return deleted_budget

    # 6. Get all budgets
    def get_all_budgets(self):
        return self.budget_repo.get_all()

    # 7. Get budget status
    def get_budget_status(self, budget_id: int):
        budget = self.budget_repo.get_by_id(budget_id)

        if budget is None:
            return None

        # Get all transactions
        transactions = self.transaction_repo.get_all(start_date=budget.start_date, end_date=budget.end_date, transaction_type=TransactionType.EXPENSE)

        # If budget has category
        if budget.category_id is not None:
            transactions = [transaction for transaction in transactions if transaction.category_id == budget.category_id]


        total_spent = sum((abs(transaction.amount) for transaction in transactions), Decimal("0"))

        remaining = budget.monthly_limit - total_spent

        spent_percentage = round((total_spent / budget.monthly_limit) * 100, 2)

        return {
            "budget": budget,
            "total_spent": total_spent,
            "remaining": remaining,
            "spent_percentage": spent_percentage,
        }

    # 8. Get all categories
    def get_categories(self):
        return self.category_repo.get_all()

    # 9. Update budget
    def update_budget(self, budget_id: int, monthly_limit: Decimal | None = None, start_date: datetime.date | None = None, end_date: datetime.date | None = None, category_id: int | None = None):
        updated_budget = self.budget_repo.update_budget(
            budget_id=budget_id,
            monthly_limit=monthly_limit,
            start_date=start_date,
            end_date=end_date,
            category_id=category_id
        )
        if updated_budget is None:
            return None
        self.session.commit()
        return updated_budget
