from sqlalchemy.orm import Session

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