import pandas as pd

def load_transactions():
    df = pd.read_csv('data/raw/transactions.csv')
    df = pd.DataFrame(df)

    return df

