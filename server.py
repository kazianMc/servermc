from flask import Flask, request, jsonify

app = Flask(__name__)

latest_command = None

@app.route("/send", methods=["POST"])
def send_command():
    global latest_command
    data = request.json
    latest_command = data.get("cmd")
    print(f"Received command: {latest_command}")
    return jsonify({"status": "ok", "received": latest_command})

@app.route("/get", methods=["GET"])
def get_command():
    global latest_command
    cmd = latest_command
    latest_command = None  # clear after reading
    return jsonify({"cmd": cmd})

@app.route("/", methods=["GET"])
def home():
    return "Command Server Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
