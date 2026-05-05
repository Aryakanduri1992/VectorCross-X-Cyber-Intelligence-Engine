import os
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from collections import Counter
import math
from scipy.sparse import hstack

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

CANDIDATES = ["sqli_dataset.csv", "dataset.csv", "models_dataset.csv"]

def find_dataset():
    if not os.path.exists(MODELS_DIR):
        print("Models directory does not exist yet:", MODELS_DIR)
        return None
    files = os.listdir(MODELS_DIR)
    print("Files in models/:", files)
    for name in CANDIDATES:
        path = os.path.join(MODELS_DIR, name)
        if os.path.exists(path):
            return path
    return None

def entropy(s: str):
    if not s:
        return 0.0
    counts = Counter(s)
    probs = [c/len(s) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def extract_numeric_features(texts):
    out = []
    for s in texts:
        s = str(s)
        L = len(s)
        special = sum(1 for ch in s if not ch.isalnum() and not ch.isspace())
        digits = sum(1 for ch in s if ch.isdigit())
        cnt_quotes = s.count("'") + s.count('"') + s.count("`")
        ent = entropy(s)
        out.append([L, special, digits, cnt_quotes, ent])
    return np.array(out)

def main():
    dataset_path = find_dataset()
    if dataset_path is None:
        print("\nERROR: No dataset found in models/.")
        print("Put your CSV into the 'models' folder (names tried):", CANDIDATES)
        print("Or run the dataset generator first: python src/dataset_generator.py\n")
        return

    print("Using dataset:", dataset_path)
    df = pd.read_csv(dataset_path)
    if 'query' not in df.columns or 'label' not in df.columns:
        print("ERROR: dataset must have columns 'query' and 'label'. Found columns:", list(df.columns))
        return

    X_text = df['query'].astype(str).values
    y = df['label'].values

    vect = TfidfVectorizer(analyzer='char_wb', ngram_range=(3,5), max_features=4000)
    X_tfidf = vect.fit_transform(X_text)

    X_num = extract_numeric_features(X_text)
    X = hstack([X_tfidf, X_num])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))
    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    vect_path = os.path.join(MODELS_DIR, "vectorizer.joblib")
    model_path = os.path.join(MODELS_DIR, "model.joblib")
    joblib.dump(vect, vect_path)
    joblib.dump(model, model_path)
    print(f"\n✅ Saved vectorizer -> {vect_path}")
    print(f"✅ Saved model -> {model_path}\n")
    print("Training complete. You can now run the detector service.")

if __name__ == "__main__":
    main()
