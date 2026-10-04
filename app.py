import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "cyberbullying.db")
MODEL_PATH = os.path.join(BASE_DIR, "model", "bullying_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        label TEXT NOT NULL,
        confidence REAL NOT NULL,
        created_at TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()


def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        return None, None
    return joblib.load(MODEL_PATH), joblib.load(VECTORIZER_PATH)


def predict_text(text):
    model, vectorizer = load_model()
    if model is None:
        raise RuntimeError("Model files are missing. Run: python scripts/train_model.py")
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    if hasattr(model, "predict_proba"):
        confidence = float(max(model.predict_proba(X)[0]))
    else:
        confidence = 0.0
    return str(prediction), confidence


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/predict")
def predict():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", error="Please enter a message to analyze.")
    if len(text) > 2000:
        return render_template("index.html", error="Please keep the message below 2,000 characters.")
    try:
        label, confidence = predict_text(text)
    except RuntimeError as exc:
        return render_template("index.html", error=str(exc))
    conn = db()
    conn.execute("INSERT INTO analyses(text,label,confidence,created_at) VALUES(?,?,?,?)",
                 (text, label, confidence, datetime.utcnow().isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    return render_template("result.html", text=text, label=label, confidence=round(confidence * 100, 2))


@app.post("/api/predict")
def api_predict():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    if not text or len(text) > 2000:
        return jsonify({"error": "text is required and must be <= 2000 characters"}), 400
    try:
        label, confidence = predict_text(text)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    return jsonify({"text": text, "label": label, "confidence": round(confidence, 4)})


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        expected_user = os.environ.get("ADMIN_USERNAME", "admin")
        expected_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        if username == expected_user and password == expected_password:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.get("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))


@app.get("/dashboard")
@admin_required
def dashboard():
    conn = db()
    total = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
    bullying = conn.execute("SELECT COUNT(*) FROM analyses WHERE label != 'non-bullying'").fetchone()[0]
    severe = conn.execute("SELECT COUNT(*) FROM analyses WHERE label = 'severe-bullying'").fetchone()[0]
    recent = conn.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT 15").fetchall()
    conn.close()
    return render_template("dashboard.html", total=total, bullying=bullying, severe=severe, recent=recent)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "model_loaded": os.path.exists(MODEL_PATH)})


init_db()

if __name__ == "__main__":
    app.run(debug=True)
