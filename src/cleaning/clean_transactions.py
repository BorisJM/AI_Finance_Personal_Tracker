import re

from src.utils.paths import load_dictionary

# Load STOPWORDS Data
STOPWORDS = load_dictionary("stopwords.json")

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
    return text