from src.classification.detect_category import detect_transaction_category

def classification(df):
    df["transaction_category"] = df["transaction_description"].apply(detect_transaction_category)
