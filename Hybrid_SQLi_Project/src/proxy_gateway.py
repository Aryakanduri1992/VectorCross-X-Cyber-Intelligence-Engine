from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__, template_folder="../templates")

DETECTOR_URL = "http://127.0.0.1:9000/detect"

from secure_backend import safe_query

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("query", "")

        try:
            resp = requests.post(DETECTOR_URL, json={"value": user_input}, timeout=3)
            if resp.status_code != 200:
                return render_template("index.html", result=f"⚠️ Detector error (status {resp.status_code}). Request blocked."), 503
            det = resp.json()
        except Exception as e:
            return render_template("index.html", result=f"⚠️ Detector unavailable: {e}. Request blocked."), 503

        if det.get("decision") == "block":
            reason = det.get("reason", "detected_as_malicious")
            score = det.get("final_score", det.get("score", None))
            return render_template("index.html", result="🚫 Attack Blocked!", score=score, reason=reason), 403

        try:
            db_result = safe_query(user_input)
            return render_template("index.html", result="✅ Safe Query Executed", score=det.get("final_score"))
        except Exception as e:
            return render_template("index.html", result=f"⚠️ Backend error: {e}"), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
