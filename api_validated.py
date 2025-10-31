# api_basic.py

# Import necessary modules
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
contacts =[]

def valid_contact(data):
    return isinstance(data, dict) and "name" in data and "phone" in data and isinstance(data["phone"], str)

@app.route("/contacts", methods=["POST"])
def add_contact():
    data = request.get_json()
    if not valid_contact(data):
        abort(400, description="Invalid contact data")
    contacts.append(data)
    return jsonify({"status": "ok", "added": data}), 201