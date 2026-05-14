import json
import re

# Load STOPWORDS Data
with open("./data/dictionaries/stopwords.json", "r") as f:
    STOPWORDS = json.load(f)

def clean_transactions(text):
    pattern = r"\b(?:{})\b".format("|".join(STOPWORDS))
    text = str(text).upper()
    # Applying regex, removing:
    # - numbers
    # - symbols
    # - multiple spaces
    # - stop words from the list
    # 1. Delete stop words
    text = re.sub(pattern, "", text)
    # 2. Delete numbers
    text = re.sub(r"\d+", "", text)
    # 3. Delete symbols
    text = re.sub(r"[^\w\s]", "", text)
    # 4. Delete multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    print(text)
    return text