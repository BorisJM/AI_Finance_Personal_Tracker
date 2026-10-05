from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def prepare_data_for_classification_ml(df):
    # Transactions count in each category
    transactions_count_category = df.groupby("transaction_category")
    # Min 5
    print("minimum 5:")
    transactions_count_category_min_5 = transactions_count_category.filter(lambda x: len(x) >= 5)
    df_ml = transactions_count_category_min_5.copy()
    x = df_ml["transaction_description"].tolist()
    y = df_ml["transaction_category"].tolist()
    print(x[:10])
    print(y[:10])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    vectorizer = TfidfVectorizer()
    x_train = vectorizer.fit_transform(x_train)
    clf = LogisticRegression().fit(x_train, y_train)
    x_test_desc = x_test
    x_test = vectorizer.transform(x_test)
    prediction = clf.predict(x_test)
    score = accuracy_score(y_test, prediction)
    print("accuracy:", score)
    # Classification report
    print("Classification report")
    print(classification_report(y_test, prediction))
    # Confusion matrix
    print(clf.classes_)
    cm = confusion_matrix(y_test, prediction)
    print("Confusion matrix")
    print(cm)
    for i, y in enumerate(y_test):
        if y != prediction[i]:
            print(x_test_desc[i])
            print("True: " + y)
            print("Predicted: " + prediction[i])