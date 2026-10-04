import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "dataset", "cyberbullying_dataset.csv")
MODEL_DIR = os.path.join(BASE, "model")


def main():
    df = pd.read_csv(DATA).dropna(subset=["text", "label"])
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), max_features=12000, sublinear_tf=True)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    model = LogisticRegression(max_iter=2000, class_weight="balanced")
    model.fit(X_train_vec, y_train)
    pred = model.predict(X_test_vec)
    print("Accuracy:", round(accuracy_score(y_test, pred), 4))
    print(classification_report(y_test, pred, zero_division=0))
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "bullying_model.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))
    print("Saved model files to", MODEL_DIR)


if __name__ == "__main__":
    main()
