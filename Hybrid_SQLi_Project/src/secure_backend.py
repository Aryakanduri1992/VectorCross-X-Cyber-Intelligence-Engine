import sqlite3
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
DB_PATH = os.path.join(MODELS_DIR, "test.db")

def setup_database():
    os.makedirs(MODELS_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()
    print("Database created/verified at:", DB_PATH)

def safe_query(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    setup_database()
close