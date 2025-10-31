# api_db.py
#Import necessary modules
import sqlite3
from flask import Flask, jsonify, request, g, abort

DATABASE = "data/contacts.db"
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
    


