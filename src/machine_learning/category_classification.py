from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
<<<<<<< HEAD
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
=======
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sqlalchemy.orm import Session

from repositories.transaction_repository import TransactionRepository
from src.data.transaction_dataframe import transaction_to_dataframe


class CategoryClassificationService:
    def __init__(self, session: Session):
        self.session = session
        self.transaction_repo = TransactionRepository(session)
    def prepare_data_for_classification_ml(self, df):
        with self.session.begin():
            # Transactions count in each category
            print(df.columns.tolist())
            transactions_count_category = df.groupby("transaction_category")
            # Min 5
            print("minimum 5:")
            transactions_count_category_min_5 = transactions_count_category.filter(lambda x: len(x) >= 5)
            df_ml = transactions_count_category_min_5.copy()
            print(df_ml.columns.tolist())
            transaction_identifiers = [x for x in df_ml["transaction_identifier"].tolist()]
            print(transaction_identifiers)
            transactions = self.transaction_repo.get_by_identifiers(transaction_identifiers)
            df_ml = transaction_to_dataframe(transactions)
            # df_ml["train_data"] = df_ml["merchant"] + " " + df_ml["cleaned_description"] + " " + df_ml["transaction_type"]
            df_ml["train_data"] = df_ml["cleaned_description"] + " " + df_ml["transaction_type"]
            print(df_ml[df_ml.duplicated(subset=["merchant", "cleaned_description"])]["category"])
            x = df_ml["train_data"].tolist()
            y = df_ml["category"].tolist()
            print(x[:10])
            print(y[:10])
            skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            print(skf)
            scores = []
            f1_scores = []
            for i, (train_index, test_index) in enumerate(skf.split(x, y)):
                print("Fold:", i)
                x_train = [x[i] for i in train_index]
                x_test = [x[i] for i in test_index]
                y_train = [y[i] for i in train_index]
                y_test = [y[i] for i in test_index]
                vectorizer = TfidfVectorizer()
                x_train = vectorizer.fit_transform(x_train)
                clf = LogisticRegression().fit(x_train, y_train)
                x_test = vectorizer.transform(x_test)
                prediction = clf.predict(x_test)
                score = accuracy_score(y_test, prediction)
                f1_score_macro = f1_score(y_test, prediction, average="macro")
                print("accuracy:", score)
                print("F1 macro: ", f1_score_macro)
                scores.append(score)
                f1_scores.append(f1_score_macro)
                clf_report = classification_report(y_test, prediction, zero_division=1)
                print(clf_report)
            print("-----------------")
            print(scores)
            print("Mean score: " + str(np.mean(scores)))
            print("Mean F1 score macro: " + str(np.mean(f1_scores)))
>>>>>>> cf825d31e952adcbd93d9708739c797d53afa028
