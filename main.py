
from pathlib import Path

from src.analytics.category_analysis import (
    expenses_by_category,
    category_percentages,
    category_percentage_per_month,
    top_categories,
)
from src.analytics.income_analysis import (
    calculate_total_income,
    calculate_monthly_income,
)
from src.analytics.spending_analysis import (
    calculate_total_expenses,
    calculate_monthly_expenses,
    calculate_biggest_expenses,
    calculate_average_monthly_expense,
    top_transactions,
)
from src.machine_learning.category_classification import (
    prepare_data_for_classification_ml,
)
from src.pipeline.data_pipeline import run_pipeline


# Project paths
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "data" / "raw" / "transactions.csv"


# 1. Load, clean and classify transactions
df, bank = run_pipeline(csv_path)

print(f"Detected bank: {bank}")


# 2. Income analytics
calculate_total_income(df)
calculate_monthly_income(df)


# 3. Expense analytics
calculate_total_expenses(df)
calculate_monthly_expenses(df)
expenses_by_category(df)
calculate_biggest_expenses(df)
category_percentages(df)
category_percentage_per_month(df)
top_categories(df)
calculate_average_monthly_expense(df)
top_transactions(df)


# 4. Machine learning experiment
prepare_data_for_classification_ml(df)
