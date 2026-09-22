import pandas as pd

from src.insights.savings_insights import saving_insights


def test_saving_insights_savings_rate():
    df = pd.DataFrame({
        "transaction_date": pd.to_datetime([
            "2026-01-10",
            "2026-02-20",
        ]),
        "debit_amount": [
            -800.00,
            -600.00,
        ],
        "credit_amount": [
            2000.00,
            3000.00,
        ],
    })

    result = saving_insights(df)

    savings_rate_insight = result[0]

    # Total income = 5000
    # Total savings = (-800 + 2000) + (-600 + 3000) = 3600
    # Savings rate = 3600 / 5000 * 100 = 72%

    assert savings_rate_insight["title"] == "Your savings rate is 72.00%"
    assert savings_rate_insight["type"] == "success"


def test_saving_insights_best_savings_month():
    df = pd.DataFrame({
        "transaction_date": pd.to_datetime([
            "2026-01-10",
            "2026-02-20",
            "2026-03-10",
        ]),
        "debit_amount": [
            -800.00,
            -500.00,
            -1000.00,
        ],
        "credit_amount": [
            2000.00,
            3000.00,
            2500.00,
        ],
    })

    result = saving_insights(df)

    best_month_insight = result[1]

    # January savings = 1200
    # February savings = 2500
    # March savings = 1500

    assert best_month_insight["title"] == "Best savings month"
    assert "2026-02" in best_month_insight["message"]
    assert "2500.0" in best_month_insight["message"]