import hashlib

# Every transaction will have unique identifier
def generate_transaction_identifier(row) -> str:
    values = "|".join(str(value) for value in row.values)

    return hashlib.sha256(values.encode('utf-8')).hexdigest()