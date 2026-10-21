from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

def prepare_data_for_classification_ml(df):
    # Transactions count in each category
    transactions_count_category = df.groupby("transaction_category")
    # Min 5
    print("minimum 5:")
    transactions_count_category_min_5 = transactions_count_category.filter(lambda x: len(x) >= 5)
    df_ml = transactions_count_category_min_5.copy()
    x = df_ml["transaction_description"].tolist()
    y = df_ml["transaction_category"].tolist()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
    for category in ["Car", "Transport", "Food", "Groceries"]:
        print(f"\n--- {category} ---")
        for description, label in zip(x_train, y_train):
            if label == category:
                print(description)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
    x_train = vectorizer.fit_transform(x_train)
    clf = LogisticRegression().fit(x_train, y_train)
    x_test_desc = x_test
    x_test = vectorizer.transform(x_test)
    prediction = clf.predict(x_test)
    score = accuracy_score(y_test, prediction)
    predictions = clf.predict_proba(x_test)
    # Transactions to verify
    transactions_to_verify = []
    # Transactions classified automatically
    automatically_classified_transactions = []
    # Wrong predictons
    wrong_predictions = []
    for i, probabilities in enumerate(predictions):
        # print("Transakcja:",i)
        # print("Opis: ", x_test_desc[i])
        # print("Prawdopodobieństwa:", probabilities)
        sorted_probability_indexes = np.argsort(probabilities)
        top_class_index = sorted_probability_indexes[-1]
        second_class_index = sorted_probability_indexes[-2]
        difference_between_probabilities = probabilities[top_class_index] - probabilities[second_class_index]
        transaction_dict = {
            "description": x_test_desc[i],
            "suggested_category": clf.classes_[top_class_index],
            "confidence_gap": difference_between_probabilities,
            "correct": clf.classes_[top_class_index] == y_test[i],
        }
        if difference_between_probabilities < 0.10:
            print("Prediction is uncertain")
            # Add to array transactions description that category needs to be verified by user
            transactions_to_verify.append(transaction_dict)
        else:
            print("Prediction: ", clf.classes_[top_class_index])
            automatically_classified_transactions.append(transaction_dict)
        print(sorted_probability_indexes)
        print(top_class_index, second_class_index)
        if prediction[i] != y_test[i]:
            wrong_predictions.append({"description": x_test_desc[i],
                                      "true_category": y_test[i],
                                      "predicted_category": prediction[i],
                                      "confidence_gap": difference_between_probabilities})
        wrong_predictions = sorted(wrong_predictions, key=lambda x: x["confidence_gap"], reverse=True)
    for i, wrong_prediction in enumerate(wrong_predictions):
        print("Nieprawda")
        print(wrong_prediction["description"])
        print("True category:", wrong_prediction["true_category"])
        print("Predicted category:", wrong_prediction["predicted_category"])
        print("Confidence gap:", wrong_prediction["confidence_gap"])
    print("Transactions to verify:")
    print(transactions_to_verify)
    print("Transactions automatically classified:")
    print(automatically_classified_transactions)
    transactions_result = {
        "to_verify_transactions": transactions_to_verify,
        "automatically_classified_transactions": automatically_classified_transactions,
    }
    print(len(transactions_result["to_verify_transactions"]))
    print(len(transactions_result["automatically_classified_transactions"]))
    print(f"Percentage of transactions classified: {(len(transactions_result['automatically_classified_transactions']) / len(x_test_desc)) * 100:.2f}%")
    print(f"Percentage of transactions to be verified: {len(transactions_result['to_verify_transactions']) / len(x_test_desc)* 100:.2f}%")
    num_of_correctly_classified_automatically = 0
    for transaction in transactions_result["automatically_classified_transactions"]:
        if transaction["correct"]:
            num_of_correctly_classified_automatically += 1
    print(num_of_correctly_classified_automatically)
    if len(transactions_result['automatically_classified_transactions']) != 0:
        print(f"Auto-classification accuracy: {num_of_correctly_classified_automatically / len(transactions_result['automatically_classified_transactions']) * 100:.2f}%")
    print(f"Coverage: {len(transactions_result['automatically_classified_transactions']) / len(x_test_desc) * 100:.2f}%")
    print(f"Overall accuracy: {score * 100:.2f}%")
    return transactions_result
