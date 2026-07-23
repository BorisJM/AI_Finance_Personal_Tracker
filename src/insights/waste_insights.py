def waste_insights(df):
    # Insight waste detection, too many cheap transactions
    cheap_purchase_value = 20
    waste_data = df.copy()
    waste_transactions = waste_data[abs(waste_data["debit_amount"]) < cheap_purchase_value].groupby("transaction_category")["debit_amount"].count().reset_index(name="count")
    largest_waste_transaction = waste_transactions.iloc[waste_transactions["count"].idxmax()]

    insight_waste_detection = {
        "type": "warning",
        "title": f"Waste detection: {largest_waste_transaction['transaction_category']}",
        "message": f"You made {largest_waste_transaction["count"]} purchases below {cheap_purchase_value} zł."
    }

    return [insight_waste_detection]