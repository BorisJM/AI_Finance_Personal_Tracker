import pandas as pd

from src.cleaning.cleaning import remove_exact_duplicates


def test_data_cleaning_removes_exact_duplicates():
    df = pd.DataFrame(
        {
            "transaction_description": [
                "BIEDRONKA",
                "BIEDRONKA",
                "LIDL",
            ],
            "counterparty_name": [
                "BIEDRONKA",
                "BIEDRONKA",
                "LIDL",
            ],
            "amount": [25.0, 25.0, 40.0],
        }
    )

    df_cleaned = remove_exact_duplicates(df)

    assert len(df_cleaned) == 2
    assert df_cleaned["amount"].tolist() == [25.0, 40.0]

def test_remove_exact_duplicates_keeps_different_transactions():
    df = pd.DataFrame(
        {
            "transaction_description": [
                "BIEDRONKA",
                "BIEDRONKA",
                "BIEDRONKA",
            ],
            "amount": [25.0, 25.0, 25.0],
            "transaction_date": [
                "2026-10-20",
                "2026-10-20",
                "2026-10-21",
            ],
        }
    )

    df_cleaned = remove_exact_duplicates(df)

    assert len(df_cleaned) == 2
    assert df_cleaned["transaction_date"].tolist() == [
        "2026-10-20",
        "2026-10-21",
    ]