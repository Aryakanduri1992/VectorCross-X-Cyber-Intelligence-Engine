import pandas as pd
import random
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
OUT_PATH = os.path.join(MODELS_DIR, "sqli_dataset.csv")

os.makedirs(MODELS_DIR, exist_ok=True)

malicious = [
    "' OR '1'='1", "'; DROP TABLE users; --", "\" OR 1=1 --",
    "' OR 'x'='x'; --", "admin'--", "1 OR 1=1",
    "'; EXEC xp_cmdshell('dir'); --", "UNION SELECT password FROM users"
]

benign = [
    "john123", "email@example.com", "search product", "contact form",
    "feedback message", "order details", "login", "user registration"
]

def generate_dataset(n=500, out_path=OUT_PATH):
    data, labels = [], []
    for _ in range(n // 2):
        data.append(random.choice(malicious))
        labels.append(1)
    for _ in range(n // 2):
        data.append(random.choice(benign))
        labels.append(0)
    df = pd.DataFrame({"query": data, "label": labels})
    df.to_csv(out_path, index=False)
    print(f"✅ Dataset created and saved to: {out_path} (rows={len(df)})")

if __name__ == "__main__":
    generate_dataset()
