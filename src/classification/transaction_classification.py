from src.classification.detect_category import detect_transaction_category
from src.utils.generate_transaction_identifier import generate_transaction_identifier
import re

def classification(df):
    # Detect category for every transaction
    df["transaction_category"] = df["transaction_description"].apply(detect_transaction_category)

    # Classify phone transfers
    phone_transfer_mask = df["transaction_type"].str.contains(
        "PRZELEW NA TELEFON", case=False, na=False
    )

    df.loc[phone_transfer_mask, "transaction_category"] = "Transfers"
    salary_description = (
        df["transaction_original_description"]
        .fillna("")
        .str.upper()
        .str.replace(r"[^A-ZĄĆĘŁŃÓŚŹŻ]", "", regex=True)
    )
    salary_mask = (
            (df["credit_amount"] > 0)
            & salary_description.str.contains("WYNAGRODZENIE", na=False)
    )

    df.loc[salary_mask, "transaction_category"] = "Income"
    # Set transaction identifier for every row
    df["transaction_identifier"] = df.apply(generate_transaction_identifier, axis=1)
    return df