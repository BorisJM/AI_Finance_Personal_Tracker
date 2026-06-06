# Load MERCHANTS Data
import json

with open("./data/dictionaries/merchants.json", "r", encoding="utf-8") as f:
    merchants = json.load(f)

def detect_transaction_category(text):
    # Normalize text
    text = text.upper()
    # Loop through all the merchants first
    for merchant in merchants.values():
        # Check if any of aliases are in the string, if yes then we assign category
        if any(elem in text for elem in merchant["aliases"]):
            return merchant["category"]
    return "Other"