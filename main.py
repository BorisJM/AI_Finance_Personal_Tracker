import pandas as pd

from src.classification.transcation_classification import classification
from src.cleaning.cleaning import data_cleaning

df = pd.read_csv('data/raw/transactions.csv')
df = pd.DataFrame(df)

# 1. Clean and prepare data
df = data_cleaning(df)
# 2. Assign every transaction to category
classification(df)
# 3. Dashboard