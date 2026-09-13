import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.budget import Budget
from database.models.category import Category

# ----------- BUSINESS LOGIC -----------
# 1. Create budget
# 2. Update budget (monthly_limit, start_date, end_date, category)
# 3. Get by ID
# 4. Get by monthly_limit greater than or less than
# 5. Get by date range (start_date, end_date)
# 6. Get by category name
# 7. Delete budget


class BudgetRepository:
    def __init__(self, session: Session):
        self.session = session

    # 1. Create budget
    def create_budget(self, monthly_limit: Decimal, start_date: datetime.date, end_date: datetime.date, category_id: int | None = None) -> Budget:
        # Date validation
        if start_date > end_date:
            raise ValueError("Start date cannot be greater than end date")
        current_date = datetime.date.today()
        if start_date > current_date:
            raise ValueError("Start date cannot be greater than current date")
        # Monthly limit validation
        if monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than zero")
        new_budget = Budget(monthly_limit=monthly_limit, start_date=start_date, end_date=end_date, category_id=category_id)
        self.session.add(new_budget)
        return new_budget


    # 2. Update budget
    def update_budget(self, budget_id: int, monthly_limit: Decimal | None = None, start_date: datetime.date | None = None, end_date: datetime.date | None = None, category_id: int | None = None) -> Budget | None:
        updated_budget = self.session.get(Budget, budget_id)
        # No budget return None
        if updated_budget is None:
            return None
        # assigning start date and end date
        new_start_date = start_date if start_date is not None else updated_budget.start_date
        new_end_date = end_date if end_date is not None else updated_budget.end_date

        if monthly_limit is not None:
            if monthly_limit <= 0:
                raise ValueError("Monthly limit must be greater than zero")
            updated_budget.monthly_limit = monthly_limit

        # Validation of dates
        if new_start_date > new_end_date:
            raise ValueError("Start date cannot be greater than end date")
        # Is start date greater than todays date
        current_date = datetime.date.today()
        if new_start_date > current_date:
            raise ValueError("Start date cannot be greater than current date")
        updated_budget.start_date = new_start_date
        updated_budget.end_date = new_end_date

        if category_id is not None:
            updated_budget.category_id = category_id

        return updated_budget


    # 3. Get by ID
    def get_by_id(self, budget_id: int) -> Budget | None:
        return self.session.get(Budget, budget_id)

    # 4. Get by monthly_limit range
    def get_by_amount_range(self, min_amount: Decimal | None = None, max_amount: Decimal | None = None) -> list[Budget]:
        stmt = select(Budget)
        # 1. Only min amount passed
        if min_amount is not None and max_amount is None:
            stmt = stmt.where(Budget.monthly_limit >= min_amount)
        # 2. Only max amount passed
        if max_amount is not None and min_amount is None:
            stmt = stmt.where(Budget.monthly_limit <= max_amount)
        # 3. Both passed
        if min_amount is not None and max_amount is not None:
        # Validation amount range
            if min_amount > max_amount:
                raise ValueError("Minimum amount cannot be greater than maximum amount")
            stmt = stmt.where(Budget.monthly_limit.between(min_amount, max_amount))

        result = self.session.execute(stmt).scalars().all()
        return result


    # 5. Get by date range
    def get_by_date_range(self, start_date: datetime.date | None = None, end_date: datetime.date | None = None) -> list[Budget]:
        stmt = select(Budget)
        # 1. Only start date passed
        if start_date is not None and end_date is None:
            stmt = stmt.where(Budget.start_date >= start_date)
        # 2. Only end date passed
        if end_date is not None and start_date is None:
            stmt = stmt.where(Budget.end_date <= end_date)
        # 3. Both passed
        if start_date is not None and end_date is not None:
            # Date range validation
            if start_date > end_date:
                raise ValueError("Start date cannot be greater than end date")
            stmt = stmt.where(Budget.start_date >= start_date, Budget.end_date <= end_date)
        result = self.session.execute(stmt).scalars().all()
        return result

    # 6. Get by category name
    def get_by_category_name(self, category_name: str) -> list[Budget]:
        stmt = select(Budget).join(Category).where(Category.name == category_name)
        result = self.session.execute(stmt).scalars().all()

        return result

    # 7. Delete budget
    def delete_budget(self, budget_id: int):
        stmt = select(Budget).where(Budget.id == budget_id)
        budget = self.session.execute(stmt).scalar_one_or_none()
        if budget is None:
            return False
        else:
            self.session.delete(budget)
            return True