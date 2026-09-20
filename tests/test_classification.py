from src.classification.detect_category import detect_transaction_category


def test_biedronka():
    assert detect_transaction_category("BIEDRONKA BYDGOSZCZ") == "Groceries"


def test_lidl():
    assert detect_transaction_category("LIDL BYDGOSZCZ") == "Groceries"


def test_bolt():
    assert detect_transaction_category("BOLT TALLINN EST") == "Transport"


def test_openai():
    assert detect_transaction_category("OPENAI CHATGPT") == "Subscriptions"


def test_udemy():
    assert detect_transaction_category("UDEMY") == "Education"


def test_wizzair():
    assert detect_transaction_category("WIZZAIR") == "Travel"


def test_salary():
    assert detect_transaction_category("WYNAGRODZENIE ZA MIESIĄC") == "Income"


def test_unknown_merchant():
    assert detect_transaction_category("XYZ RANDOM SHOP") == "Other"


def test_own_transfer():
    assert detect_transaction_category("PRZELEW WŁASNY") == "Transfers"

def test_lowercase_text():
    assert detect_transaction_category("biedronka bydgoszcz") == "Groceries"


def test_mixed_case_text():
    assert detect_transaction_category("Biedronka Bydgoszcz") == "Groceries"


def test_text_with_extra_information():
    assert detect_transaction_category(
        "TRANSAKCJA KARTĄ BIEDRONKA BYDGOSZCZ 123"
    ) == "Groceries"


def test_chatgpt_alias():
    assert detect_transaction_category("CHATGPT PLUS") == "Subscriptions"


def test_jeronimo_alias():
    assert detect_transaction_category("JERONIMO MARTINS") == "Groceries"


def test_blik_alias():
    assert detect_transaction_category("PRZELEW BLIK NA TELEFON") == "Transfers"


def test_unknown_text():
    assert detect_transaction_category(
        "RANDOM UNKNOWN TRANSACTION 123"
    ) == "Other"