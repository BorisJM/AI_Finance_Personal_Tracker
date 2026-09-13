from data.load_data import load_transactions
from src.classification.transcation_classification import classification
from src.cleaning.cleaning import data_cleaning
from src.pipeline.identify_bank import identify_bank


# Pipeline for data load, cleaning, preparation
def run_pipeline(file_path):
    # Load data
    df = load_transactions(file_path)
    # Data cleaning
    df = data_cleaning(df)
    # Identify bank
    bank = identify_bank(df["account_number"].iloc[0])

    # Assign every transaction to category
    df = classification(df)

    return df, bank
