# server.py
from flask import Flask, request, jsonify
from queue import Queue
import os
from datetime import datetime

app = Flask(__name__)

# Queue thread-safe pentru comenzi
commands = Queue()

# Endpoint pentru a primi comenzi de la bot
@app.route("/send", methods=["POST"])
def send_command():
    data = request.json
    command = data.get("command")
    user = data.get("user")
    if command:
        commands.put((command, user))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Received command: {command} from {user}")
        return jsonify({"status": "ok", "received": command})
    else:
        return jsonify({"status": "error", "message": "No command received"}), 400

# Endpoint pentru a prelua comanda următoare
@app.route("/get", methods=["GET"])
def get_command():
    if commands.empty():
        return jsonify({"cmd": None})
    cmd, user = commands.get()
    return jsonify({"cmd": cmd, "user": user})

# Homepage simplu
@app.route("/", methods=["GET"])
def home():
    return "Command Server Running!"

# Pornire server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render setează PORT automat
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Server starting on port {port}...")
    app.run(host="0.0.0.0", port=port)
