"""
Financial Discipline Score (FDS), 0-100.

Components (max points):
- Savings  (40) - how much of the income was not spent.
- Budgets  (35) - how much of the planned budgets was used. Optional.
- Stability (25) - how much monthly expenses vary (coefficient of variation).

Without budgets the score is savings + stability, rescaled from 65 to 100.

Period: the last 6 full calendar months (the current, unfinished month is skipped).

Design decisions:
- Transactions in the "Transfers" category are excluded. This removes card
  repayments and own transfers, but also BLIK/phone transfers to other people.
  Known limitation: some of those are real expenses.
- A month with transactions but no expenses counts as 0 zł spent.
- A month with no transactions at all means the data is incomplete
  (e.g. a bank export was not imported), so stability cannot be calculated.
"""
import calendar
import statistics
from datetime import date
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from database.models.enums import TransactionType

FDS_MONTHS = 6
TRANSFER_CATEGORY = "Transfers"


# 1. Function for savings points
def calculate_savings_point(total_income, total_expenses):
    if total_income <= 0:
        return None
    # Expenses can be passed as negative (as stored in the database) or positive
    savings_rate = ((total_income - abs(total_expenses)) / total_income) * 100
    if savings_rate < 5:
        return 0
    elif savings_rate < 10:
        return 10
    elif savings_rate < 15:
        return 15
    elif savings_rate < 20:
        return 25
    elif savings_rate < 25:
        return 35
    else:
        return 40


# 2. Calculate budget points
def calculate_budget_points(budget_utilization):
    # No budgets -> budget component is skipped
    if budget_utilization is None:
        return None
    if budget_utilization <= 80:
        return 35
    elif budget_utilization <= 90:
        return 30
    elif budget_utilization <= 100:
        return 25
    elif budget_utilization <= 110:
        return 15
    elif budget_utilization <= 125:
        return 5
    else:
        return 0


# 3. Calculate stability points
def calculate_stability_points(monthly_expenses):
    # Can't calculate stability points without 6 months of expenses
    if monthly_expenses is None or len(monthly_expenses) != FDS_MONTHS:
        return None
    average_monthly_expenses = sum(monthly_expenses) / len(monthly_expenses)
    # Nothing spent in 6 months - stability is undefined (division by 0)
    if average_monthly_expenses == 0:
        return None
    standard_deviation = statistics.pstdev(monthly_expenses)
    stability_rate = standard_deviation / average_monthly_expenses * 100
    if stability_rate < 5:
        return 25
    elif stability_rate < 10:
        return 20
    elif stability_rate < 15:
        return 15
    elif stability_rate < 25:
        return 10
    elif stability_rate < 35:
        return 5
    else:
        return 0


# 4. Calculate FDS points
def calculate_fds(savings_points, budget_points, stability_points):
    if stability_points is None or savings_points is None:
        return None
    # If there are no budgets created
    if budget_points is None:
        # Only savings (40) + stability (25) = 65 points, rescaled to 100
        return round(((savings_points + stability_points) / 65) * 100)
    return round(savings_points + budget_points + stability_points)


# 5. Interpret FDS
def interpret_fds(score):
    if score is None:
        return None
    if score <= 39:
        return "Bad discipline"
    elif score <= 59:
        return "Moderate discipline"
    elif score <= 74:
        return "Good discipline"
    elif score <= 89:
        return "Very good discipline"
    else:
        return "Perfect discipline"


# 6. Get last six months range
def get_last_six_months_range(today=None):
    # `today` can be passed in tests; by default the real current date is used
    if today is None:
        today = date.today()
    start_date = (today - relativedelta(months=FDS_MONTHS)).replace(day=1)
    last_month_date = today - relativedelta(months=1)
    last_day = calendar.monthrange(last_month_date.year, last_month_date.month)[1]
    end_date = date(last_month_date.year, last_month_date.month, last_day)

    return start_date, end_date


# 7. Get transactions from database for FDS
def get_transactions_for_fds(transaction_repository, today=None):
    start_date, end_date = get_last_six_months_range(today)
    return transaction_repository.get_all(start_date=start_date, end_date=end_date)


# Helper function to identify if transaction is a transfer
def is_internal_transfer(transaction):
    # In the ORM model `category` is a Category object, so we compare its name
    return transaction.category.name == TRANSFER_CATEGORY


# 8. Separate transactions by INCOME and EXPENSE (transfers are skipped)
def separate_transactions(transactions):
    transactions_filtered = [t for t in transactions if not is_internal_transfer(t)]
    income_transactions = []
    expense_transactions = []
    for transaction in transactions_filtered:
        if transaction.transaction_type == TransactionType.INCOME:
            income_transactions.append(transaction)
        elif transaction.transaction_type == TransactionType.EXPENSE:
            expense_transactions.append(transaction)

    return income_transactions, expense_transactions


# 9. Calculate totals
def calculate_totals(income_transactions, expense_transactions):
    total_income = Decimal("0")
    total_expenses = Decimal("0")
    for transaction in income_transactions:
        total_income += transaction.amount
    for transaction in expense_transactions:
        total_expenses += transaction.amount

    # Expenses stay negative, as in the database
    return total_income, total_expenses


# 10. Monthly expenses for the FDS period
def calculate_monthly_expenses_for_fds(transactions, expense_transactions, start_date):
    """
    Return a list of 6 positive monthly expense totals (oldest month first),
    or None when any month has no transactions at all (incomplete data).

    `transactions` - all transactions in the period (used to check data coverage)
    `expense_transactions` - expenses only, already without transfers
    """
    months = [start_date + relativedelta(months=i) for i in range(FDS_MONTHS)]
    month_keys = [(month.year, month.month) for month in months]

    months_with_data = {(t.transaction_date.year, t.transaction_date.month) for t in transactions}
    if any(key not in months_with_data for key in month_keys):
        return None

    totals = {key: Decimal("0") for key in month_keys}
    for transaction in expense_transactions:
        key = (transaction.transaction_date.year, transaction.transaction_date.month)
        if key in totals:
            totals[key] += abs(transaction.amount)

    return [totals[key] for key in month_keys]


# 11. Budget utilization (average % used of budgets in the period)
def calculate_budget_utilization(budget_statuses):
    """
    `budget_statuses` - results of BudgetService.get_budget_status().
    Returns None when there are no budgets.
    """
    percentages = [status["spent_percentage"] for status in budget_statuses if status is not None]
    if not percentages:
        return None
    return sum(percentages) / len(percentages)


# 12. Full FDS from a list of transactions
def calculate_fds_from_transactions(transactions, today=None, budget_utilization=None):
    """
    Pure function (no database): calculates the whole score and returns every
    component, so the dashboard can explain where the score comes from.
    """
    start_date, end_date = get_last_six_months_range(today)
    transactions = [t for t in transactions if start_date <= t.transaction_date <= end_date]

    income_transactions, expense_transactions = separate_transactions(transactions)
    total_income, total_expenses = calculate_totals(income_transactions, expense_transactions)
    monthly_expenses = calculate_monthly_expenses_for_fds(transactions, expense_transactions, start_date)

    savings_points = calculate_savings_point(total_income, total_expenses)
    budget_points = calculate_budget_points(budget_utilization)
    stability_points = calculate_stability_points(monthly_expenses)
    score = calculate_fds(savings_points, budget_points, stability_points)

    if savings_points is None:
        reason = "No income in the last 6 months."
    elif monthly_expenses is None:
        reason = "Missing transactions for at least one of the last 6 months."
    elif stability_points is None:
        reason = "No expenses in the last 6 months."
    else:
        reason = None

    return {
        "score": score,
        "label": interpret_fds(score),
        "reason": reason,
        "start_date": start_date,
        "end_date": end_date,
        "total_income": total_income,
        "total_expenses": abs(total_expenses),
        "monthly_expenses": monthly_expenses,
        "budget_utilization": budget_utilization,
        "savings_points": savings_points,
        "budget_points": budget_points,
        "stability_points": stability_points,
    }


# 13. Full FDS from the database
def get_financial_discipline_score(session, today=None):
    # Imported here to keep the pure functions above free of database setup
    from database.repositories.transaction_repository import TransactionRepository
    from database.services.budget_service import BudgetService

    transactions = get_transactions_for_fds(TransactionRepository(session), today)

    start_date, end_date = get_last_six_months_range(today)
    budget_service = BudgetService(session)
    budgets = budget_service.get_budgets_by_date_range(start_date, end_date)
    budget_statuses = [budget_service.get_budget_status(budget.id) for budget in budgets]
    budget_utilization = calculate_budget_utilization(budget_statuses)

    return calculate_fds_from_transactions(transactions, today, budget_utilization)
