from src.classification.extract_location import extract_location


def test_finds_city_in_description():
    assert extract_location("LIDL BYDGOSZCZ", "") == "BYDGOSZCZ"


def test_description_is_case_insensitive():
    assert extract_location("lidl bydgoszcz", "") == "BYDGOSZCZ"


def test_first_city_in_list_order_wins():
    # Current behaviour: the earlier entry in locations.json wins, so the shorter
    # "ABRAMOWICE" beats the more specific "ABRAMOWICE KOŚCIELNE".
    # Known limitation - preferring the longest match would be more accurate.
    assert extract_location("ZABKA ABRAMOWICE KOŚCIELNE", "") == "ABRAMOWICE"


def test_does_not_match_part_of_a_word():
    # "RADOMSKO" must not be recognised as "RADOM"
    assert extract_location("SKLEP RADOMSKOX", "") == "Undefined location"


def test_falls_back_to_counterparty_name():
    assert extract_location("PRZELEW", "FIRMA TESTOWA WARSZAWA") == "WARSZAWA"


def test_returns_undefined_when_no_city():
    assert extract_location("OPENAI CHATGPT", "") == "Undefined location"


def test_empty_text():
    assert extract_location("", "") == "Undefined location"
