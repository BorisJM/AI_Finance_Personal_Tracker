import pandas as pd

from src.analytics.category_analysis import expenses_by_category, category_percentages, category_percentage_per_month, \
    top_categories
from src.analytics.income_analysis import calculate_total_income, calculate_monthly_income
from src.analytics.spending_analysis import calculate_total_expenses, calculate_monthly_expenses, \
    calculate_biggest_expenses, calculate_average_monthly_expense, top_transactions
from src.classification.transcation_classification import classification
from src.cleaning.cleaning import data_cleaning
from src.pipeline.data_pipeline import run_pipeline

# Run pipeline
df = run_pipeline()
print(df.head())
# 3. Dashboard
# -------- INCOMES --------
# Calculate total income
calculate_total_income(df)
# Calculate monthly income
calculate_monthly_income(df)
# -------- EXPENSES --------
# Calculate total expenses
calculate_total_expenses(df)
# Calculate expenses per month
calculate_monthly_expenses(df)
# Calculate expenses per category
expenses_by_category(df)
# Calculate top 10 expenses
calculate_biggest_expenses(df)
# Calculate what percentage every category takes
category_percentages(df)
# Calculate category percentage per month
category_percentage_per_month(df)
# Calculate Top categories
top_categories(df)
# Calculate average monthly expense
calculate_average_monthly_expense(df)
# Calculate top transactions
top_transactions(df)