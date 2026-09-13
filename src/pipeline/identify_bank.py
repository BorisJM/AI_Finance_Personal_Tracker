import json

# Import Polish banks JSON
with open("data/dictionaries/polish_banks.json", "r") as file:
    polish_bank_dictionary = json.load(file)


def identify_bank(account_number: str) -> str:
    # 1. Delete some whitespaces or dash and PL
    cleaned_account_number = str(account_number).replace(" ", "").replace("-", "").upper().replace("PL", "")
    # 2. Check length (Polish account number should be always 26 digits)
    if len(cleaned_account_number) != 26 or not cleaned_account_number.isdigit():
        raise ValueError("ERROR: Account number is invalid.")

    # 3. Algorithm MOD97 to check if account number is valid (IBAN standard)
    check_digits = cleaned_account_number[:2]
    remaining_number = cleaned_account_number[2:]
    pl_code_numeric = "2521" # # "P" = 25, "L" = 21

    # 30-digit number for validation
    number_to_test = int(remaining_number + pl_code_numeric + check_digits)

    # Check the remainder of division by 97
    if number_to_test % 97 != 1:
        raise ValueError("Error: Invalid account number (checksum failed).")

    # 4. Identify the bank using digits 3 to 6
    bank_code = cleaned_account_number[2:6]

    bank_name = polish_bank_dictionary.get(bank_code, "Unknown")

    return bank_name