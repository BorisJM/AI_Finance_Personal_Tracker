import pandas as pd
from src.cleaning.cleaning import data_cleaning

df = pd.read_csv('data/raw/transactions.csv')
df = pd.DataFrame(df)

# 1. Clean and prepare data
data_cleaning(df)
