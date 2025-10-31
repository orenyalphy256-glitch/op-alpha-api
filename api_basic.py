# api_basic.py

# Import necessary modules
from flask import Flask, jsonify, request

app = Flask(__name__)
contacts =[]

@app.route("/contacts", methods=["GET"])
def list_contacts():
    return jsonify(contacts)

@app.route("/contacts", methods=["POST"])
def add_contact():
    data = request.get_json()
    contacts.append(data)
    return jsonify({"status": "ok", "added": data}), 201

if __name__=="__main__":
    app.run(debug=True, port=5000)