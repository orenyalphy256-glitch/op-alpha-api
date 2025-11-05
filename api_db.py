# api_db.py
#Import necessary modules
import os
import sqlite3
from flask import Flask, jsonify, request, g, abort
from time import time
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "99-Logs"
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "contacts.db"

LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "api.log"
logging.basicConfig(
    filename=str(LOG_FILE), 
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %"
    "(message)s",
    )

DATABASE = str(DB_PATH)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMAY KEY, name TEXT, phone TEXT, created_at TEXT)")
        conn.commit()
        logging.info("Database initialized (or already exists): %s", DATABASE)


req_times = {}

def require_api_key():
    key = request.headers.get("X-API-KEY")
    if key != "secret123":
        abort(401)

def rate_limit(client="global", limit=6, period=60):
    now = int(time())
    window = now // period
    key = f"{client}:{window}"
    req_times.setdefault(key, 0)
    req_times[key] += 1
    if req_times[key] > limit:
        abort(429, "Too many requests")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE = os.path.join(DATA_DIR, "contacts.db")
app = Flask(__name__)

def get_db():
    db = getattr(g, "database", None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        return db
    
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
        
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    db = get_db()
    row = db.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if row is None:
        abort(404)
        return jsonify(dict(row))
    
@app.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    data = request.get_json()
    db = get_db()
    db.execute(
        "UPDATE contacts SET name = ?, phone = ? WHERE id = ?",
        (data.get("name"), data.get("phone"), contact_id)
    )
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
    if not isinstance(data, dict) or "phone" not in data:
        abort(400)
    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO contacts (name, phone) VALUES (?, ?)",
            (data["name"], data["phone"])
        )
        db.commit()
        return jsonify({"status": "ok", "id": cursor.lastrowid}), 201
    except sqlite3.IntegrityError:
        abort(400, description="Phone already exists")

logging.basicConfig(
    filename="99-Logs/api.log", 
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
    )
logging.info("API starting")
    


