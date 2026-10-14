import pandas as pd

def load_transactions(file_path: str):
    df = pd.read_csv(file_path)
    df = pd.DataFrame(df)
    print("Wczytane kolumny:", df.columns.tolist())
    print("Liczba wierszy:", len(df))
    print(df.head(3).to_string())
    return df

