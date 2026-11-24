import re

from src.utils.paths import load_dictionary

# All Polish cities, in priority order (first match in this list wins)
locations = load_dictionary("locations.json")

# Location name -> its position in the list (lower = higher priority)
LOCATION_PRIORITY = {location: index for index, location in enumerate(locations)}

# Longest location name, counted in words ("ABRAMOWICE KOŚCIELNE" = 2 words)
MAX_WORDS_IN_LOCATION = max(len(re.findall(r"\w+", location)) for location in locations)

# A few names start or end with a symbol (e.g. 'MAZEWO DWORSKIE"A"').
# Word lookup can't find them, so they are still checked with a regex.
IRREGULAR_LOCATIONS = [
    location for location in locations
    if not (re.match(r"\w", location) and re.search(r"\w$", location))
]
IRREGULAR_PATTERNS = [
    (location, re.compile(rf"\b{re.escape(location)}\b")) for location in IRREGULAR_LOCATIONS
]


def _candidate_phrases(text: str) -> set[str]:
    """
    Every fragment of `text` made of 1..MAX_WORDS_IN_LOCATION consecutive words,
    cut exactly at word boundaries. For "PIZZA STARE MIASTO" this gives:
    "PIZZA", "STARE", "MIASTO", "PIZZA STARE", "STARE MIASTO", "PIZZA STARE MIASTO".
    """
    words = list(re.finditer(r"\w+", text))
    phrases = set()
    for start_index, start_word in enumerate(words):
        last_index = min(start_index + MAX_WORDS_IN_LOCATION, len(words))
        for end_word in words[start_index:last_index]:
            phrases.add(text[start_word.start():end_word.end()])
    return phrases


def _matching_locations(text: str) -> set[str]:
    found = {phrase for phrase in _candidate_phrases(text) if phrase in LOCATION_PRIORITY}
    for location, pattern in IRREGULAR_PATTERNS:
        if pattern.search(text):
            found.add(location)
    return found


def extract_location(text: str, counterparty_name: str) -> str:
    """
    Return the first location (in locations.json order) that appears as a whole
    word/phrase in the description or the counterparty name.

    Instead of running ~57 000 regexes per transaction, we cut the text into
    short word phrases and look each one up in a dictionary (O(1) per lookup).
    """
    text = text.upper()

    found = _matching_locations(text) | _matching_locations(counterparty_name)
    if not found:
        return "Undefined location"
    return min(found, key=LOCATION_PRIORITY.__getitem__)
