import json
from rapidfuzz import fuzz # To detect fuzzy words
from src.cleaning.clean_transactions import clean_transactions
from src.cleaning.data_conversion import data_conversion

# --- DATA CLEANING ---
def data_cleaning(df):
    # Drop duplicates from the table.
    df.drop_duplicates()
    # Drop useless column
    df.drop(columns=['Data rozliczenia', 'Numer rachunku/karty'], inplace=True)
    ''' --- Data conversion ---
    - Convert column names to LowerCase, remove Whitespaces and convert to SnakeCase
    - Remove polish symbols from column names with unidecode 
    '''
    data_conversion(df)
    # Cleaning description, regex cleaning, remove numbers, symbols, non-word characters
    df["transaction_description"] = df["transaction_description"].apply(clean_transactions)
    # For empty fields we will put name of receiver/sender
    df.loc[df["transaction_description"] == "", "transaction_description"] = df["counterparty_name"]
    return df

