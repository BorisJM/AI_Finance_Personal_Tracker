from unidecode import unidecode
import pandas as pd

def data_conversion(df):
    df.columns = [unidecode(column_name.strip().lower().replace(" ", "_")) for column_name in df.columns]
    # Translate columns to English
    translated_columns = [
        'transaction_date',
        'transaction_type',
        'counterparty_account',
        'counterparty_name',
        'transaction_description',
        'debit_amount',
        'credit_amount',
        'account_balance',
        'currency_code'
    ]
    # 1 Create object for mapping
    mapping_columns_name = dict(zip(df.columns, translated_columns))
    # 2 Change columns names
    df.rename(columns=mapping_columns_name, inplace=True)

    # 3. Data conversion to numeric
    df["account_balance"] = pd.to_numeric(df["account_balance"], errors='coerce')
    df["credit_amount"] = pd.to_numeric(df["credit_amount"], errors='coerce')
    df["debit_amount"] = pd.to_numeric(df["debit_amount"], errors='coerce')
    # 4. Remove whitespaces, change NAN to 0 and convert column value to numeric
    df["counterparty_account"] = (pd.to_numeric(df["counterparty_account"].str.replace(" ", "").fillna(0)))
    # 5. Convert string to Date Format
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    # 6. Create month column for every transaction
    df["transaction_month"] = df["transaction_date"].dt.month_name()