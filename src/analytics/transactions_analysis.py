
def get_last_transactions(df):
    # Sort by date first and get 10 last transactions
    last_10_transactions = df.sort_values(by="transaction_date", ascending=True)
    last_10_transactions = last_10_transactions.tail(10)
    # Hide unnecessary columns
    last_10_transactions = last_10_transactions.drop(columns=['counterparty_account', 'counterparty_name', 'account_balance', 'currency_code'])
    return last_10_transactions