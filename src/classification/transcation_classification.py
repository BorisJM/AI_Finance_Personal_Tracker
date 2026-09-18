from src.classification.detect_category import detect_transaction_category
from src.utils import generate_transaction_identifier


def classification(df):
    # Detect category for every transaction
    df["transaction_category"] = df["transaction_description"].apply(detect_transaction_category)
    # Set Income category for every transaction with positive credit amount
    df.loc[df["credit_amount"] > 0, 'transaction_category'] = "Income"
    print(df[df["transaction_category"] == "Other"][["transaction_description", "debit_amount"]])
    # Set transaction identifier for every row
    df["transaction_identifier"] = df.apply(generate_transaction_identifier, axis=1)
    return df