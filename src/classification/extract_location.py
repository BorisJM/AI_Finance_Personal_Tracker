import re
import json

with open("./data/dictionaries/locations.json", "r", encoding="utf-8") as f:
    # All polish cities
    locations = json.load(f)


def extract_location(text: str, counterparty_name: str) -> str:
    text = text.upper()

    for location in locations:
        pattern = rf"\b{re.escape(location)}\b"
        if re.search(pattern, text):
            return location

        elif re.search(pattern, counterparty_name):
            return location
    return "Undefined location"
