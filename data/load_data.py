import pandas as pd

def load_transactions(file_path: str):
    df = pd.read_csv(file_path)
    df = pd.DataFrame(df)

    return df

