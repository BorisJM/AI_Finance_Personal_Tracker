import hashlib

IDENTIFIER_FIELDS = [
    "account_number",
    "transaction_date",
    "settlement_date",
    "transaction_type",
    "counterparty_account",
    "transaction_description",
    "debit_amount",
    "credit_amount",
    "account_balance",
    "currency_code",
]

# Every transaction will have unique identifier
def generate_transaction_identifier(row) -> str:
    values = "|".join(str(row[field]) for field in IDENTIFIER_FIELDS)

    return hashlib.sha256(values.encode('utf-8')).hexdigest()