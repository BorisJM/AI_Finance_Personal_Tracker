from src.classification.detect_category import detect_transaction_category

def classification(df):
    # Detect category for every transaction
    df["transaction_category"] = df["transaction_description"].apply(detect_transaction_category)
    # Set Income category for every transaction with positive credit amount
    df.loc[df["credit_amount"] > 0, 'transaction_category'] = "Income"
    print(df[df["transaction_category"] == "Other"][["transaction_description", "debit_amount"]])