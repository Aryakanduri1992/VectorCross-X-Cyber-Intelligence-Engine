import os
import re
import math
import joblib
import csv
from collections import Counter
from datetime import datetime
from flask import Flask, request, jsonify
import numpy as np
from scipy.sparse import hstack

THRESHOLD = 0.6
ML_WEIGHT = 0.7
ANOMALY_WEIGHT = 0.3
ANOMALY_SPECIAL_WEIGHT = 0.6
ANOMALY_ENTROPY_WEIGHT = 0.4

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
VECT_FILE = os.path.join(MODELS_DIR, "vectorizer.joblib")
MODEL_FILE = os.path.join(MODELS_DIR, "model.joblib")
LOG_PATH = os.path.join(MODELS_DIR, "predictions.csv")

os.makedirs(MODELS_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return 'Detector running. POST /detect with JSON {"value":"..."}', 200

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

print("Looking for model files in:", MODELS_DIR)
print("Expected vectorizer:", VECT_FILE)
print("Expected model:", MODEL_FILE)

if not os.path.exists(VECT_FILE) or not os.path.exists(MODEL_FILE):
    raise FileNotFoundError("Model artifacts not found. Ensure vectorizer.joblib and model.joblib are in models/")

VECT = joblib.load(VECT_FILE)
MODEL = joblib.load(MODEL_FILE)

RULES = [
    re.compile(r"(\bUNION\b\s+\bSELECT\b)", re.IGNORECASE),
    re.compile(r"(--|;|/\*|\*/|xp_cmdshell|DROP\s+TABLE|SLEEP|WAITFOR|EXEC|;--)", re.IGNORECASE),
    re.compile(r"(\bOR\b\s+1=1|\bOR\b\s+'1'='1')", re.IGNORECASE)
]

def rule_check(s: str):
    for r in RULES:
        if r.search(s):
            return True, r.pattern
    return False, ""

def entropy(s: str):
    if not s:
        return 0.0
    counts = Counter(s)
    probs = [c/len(s) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def numeric_features(s: str):
    s = str(s)
    L = len(s)
    special = sum(1 for ch in s if not ch.isalnum() and not ch.isspace())
    digits = sum(1 for ch in s if ch.isdigit())
    quotes = s.count("'") + s.count('"') + s.count("`")
    ent = entropy(s)
    return [L, special, digits, quotes, ent]

def log_decision(value: str, result: dict):
    os.makedirs(MODELS_DIR, exist_ok=True)
    header = ["timestamp","value","decision","reason","rule","ml_prob","anomaly_score","final_score"]
    exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        store_value = value if len(value)<=120 else value[:120] + "...[TRUNC]"
        writer.writerow([
            datetime.utcnow().isoformat(),
            store_value,
            result.get("decision"),
            result.get("reason",""),
            result.get("rule",""),
            result.get("ml_prob",""),
            result.get("anomaly_score",""),
            result.get("final_score","")
        ])

def predict_query(value: str):
    value = str(value or "").strip()
    matched, rule = rule_check(value)
    if matched:
        out = {"decision":"block", "reason":"rule_match", "rule": str(rule), "score": 1.0}
        return out

    tf = VECT.transform([value])
    num = np.array(numeric_features(value)).reshape(1, -1)
    X = hstack([tf, num])
    ml_prob = float(MODEL.predict_proba(X)[0][1])

    L = len(value) if len(value)>0 else 1
    special = sum(1 for ch in value if not ch.isalnum() and not ch.isspace()) / L
    ent = entropy(value) / 8.0
    anomaly = min(1.0, ANOMALY_SPECIAL_WEIGHT*special + ANOMALY_ENTROPY_WEIGHT*ent)

    final_score = ML_WEIGHT * ml_prob + ANOMALY_WEIGHT * anomaly
    decision = "block" if final_score >= THRESHOLD else "allow"

    return {
        "decision": decision,
        "ml_prob": round(ml_prob,4),
        "anomaly_score": round(anomaly,4),
        "final_score": round(final_score,4)
    }

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json(force=True)
    value = str(data.get("value","")).strip()
    result = predict_query(value)

    if result.get("decision") == "block" and "rule" in result:
        resp = {
            "decision": result.get("decision"),
            "reason": result.get("reason"),
            "rule": result.get("rule"),
            "score": float(result.get("score", 1.0))
        }
        log_decision(value, resp)
        return jsonify(resp), 200

    out = {
        "decision": result.get("decision"),
        "ml_prob": result.get("ml_prob"),
        "anomaly_score": result.get("anomaly_score"),
        "final_score": result.get("final_score")
    }
    log_decision(value, out)
    return jsonify(out), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
