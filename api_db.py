# api_db.py
# Import necessary modules
import os
import sqlite3
import logging
from flask import g, Flask, jsonify, request, abort, render_template
from time import time
from pathlib import Path

# Paths, dir, constants
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR/"data"
LOG_DIR = BASE_DIR/"99-Logs"
DB_PATH = DATA_DIR/"contacts.db"
LOG_FILE = LOG_DIR/"api.log"

# Ensure data directory and files exist
DATA_DIR.mkdir(exist_ok=True)
DB_PATH.touch(exist_ok=True)
LOG_FILE.touch(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
DATABASE = str(DB_PATH)

# Logging configuration
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Flask app setup
app = Flask(__name__)
req_times = {}

# Helpers: authentication & rate limiting
def require_api_key():
    expected = os.environ.get("API_KEY", "Correctly.1")
    api_key = request.headers.get("X-API-KEY")
    if api_key != expected:
        logging.warning("Unauthorized access attempt.")
        abort(401, description="Unauthorized")

def rate_limit(client="global", limit=5, period=60):
    now = int(time())
    window = now // period
    key = f"{client}:{window}"
    req_times.setdefault(key, 0)
    req_times[key] += 1
    if req_times[key] > limit:
        logging.warning(f"Rate limit exceeded for {client}.")
        abort(429, description="Too Many Requests")

# Database connection
def get_db():
    db = getattr(g, "database", None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        g.database = db
    return db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "database", None)
    if db is not None:
        db.close()

# Routes - CRUD operations
@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    db = get_db()
    row = db.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,),).fetchone()
    if row is None:
        abort(404, description="Contact not found")
    return jsonify(dict(row))

@app.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    data = request.get_json()
    db = get_db()
    db.execute(
        "UPDATE contacts SET name = ?, phone = ? WHERE id = ?", (data.get("name"), data.get("phone"), contact_id),)
    db.commit()
    return jsonify({"status": "ok"})

@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    db = get_db()
    db.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    db.commit()
    return jsonify({"status": "deleted"})

@app.route("/contacts", methods=["POST"])
def add_contact():
    data = request.get_json()
    if not isinstance(data, dict) or "phone" not in data or "name" not in data:
        abort(400, description="Invalid input")
    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO contacts (name, phone) VALUES (?, ?)", (data["name"], data["phone"]),
        )
        db.commit()
        return jsonify({"status": "ok", "id": cursor.lastrowid}), 201
    except sqlite3.IntegrityError:
        abort(400, description="Contact with this phone already exists")

# Dashboard route
@app.route("/")
def dashboard():
    db = get_db()
    cur = db.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    rows = cur.fetchall()
    rows = [dict(r) for r in rows]
    return render_template("contacts.html", rows=rows)

# Run app
if __name__ == "__main__":
    logging.info("Starting API server...")
    app.run(debug=False)