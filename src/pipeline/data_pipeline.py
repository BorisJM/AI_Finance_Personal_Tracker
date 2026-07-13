from data.load_data import load_transactions
from src.classification.transcation_classification import classification
from src.cleaning.cleaning import data_cleaning


# Pipeline for data load, cleaning, preparation
def run_pipeline():
    # Load data
    df = load_transactions()
    # Data cleaning
    df = data_cleaning(df)
    # Assign every transaction to category
    df = classification(df)

    return df
