from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
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