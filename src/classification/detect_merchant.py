import json

with open("./data/dictionaries/merchants.json", "r", encoding="utf-8") as f:
    merchants = json.load(f)

def normalize_merchant_name(text):
    # Normalize text
    text = text.upper()
    # Loop through all the merchants first
    for merchant_name, merchant in merchants.items():
        # Check if any of aliases are in the string, then we return merchant name
        if any(elem in text for elem in merchant["aliases"]):
            return merchant_name
    return text

