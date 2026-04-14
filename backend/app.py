from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import hashlib
import datetime
import json
from time import time

app = Flask(__name__)
CORS(app)

API_KEY = "12345"

model = pickle.load(open('../ml_model/model.pkl', 'rb'))

request_log = {}

# =========================
# 🔐 HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# 📥 LOAD JSON
# =========================
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

# =========================
# 💾 SAVE JSON
# =========================
def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# 📜 LOG SECURITY EVENTS
# =========================
def log_request(ip, status):
    with open("security_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | IP: {ip} | {status}\n")

# =========================
# 🔐 HASH RESPONSE
# =========================
def generate_hash(data):
    return hashlib.sha256(str(data).encode()).hexdigest()

# =========================
# 🚫 RATE LIMIT
# =========================
@app.before_request
def limit_requests():
    if request.method == "OPTIONS":
        return

    ip = request.remote_addr
    current_time = time()

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [t for t in request_log[ip] if current_time - t < 30]

    if len(request_log[ip]) > 20:
        log_request(ip, "Rate limit exceeded")
        return jsonify({"error": "Too many requests"}), 429

    request_log[ip].append(current_time)

# =========================
# 🔐 SIGNUP
# =========================
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    users = load_json("users.json")

    for user in users:
        if user["username"] == username:
            return jsonify({"error": "User exists"}), 400

    users.append({
        "username": username,
        "password": hash_password(password)
    })

    save_json("users.json", users)

    return jsonify({"message": "Signup successful"})

# =========================
# 🔐 LOGIN
# =========================
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_json("users.json")

    for user in users:
        if user["username"] == username and user["password"] == hash_password(password):
            return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid credentials"}), 401

# =========================
# 🌱 PREDICT
# =========================
@app.route('/predict', methods=['POST'])
def predict():
    ip = request.remote_addr

    client_key = request.headers.get("X-API-KEY")
    if client_key != API_KEY:
        log_request(ip, "Unauthorized")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    username = data.get("username")
    moisture = data.get("moisture")
    temp = data.get("temperature")

    if not username or moisture is None or temp is None:
        return jsonify({"error": "Invalid input"}), 400

    result = model.predict([[int(moisture), int(temp)]])[0]
    irrigation = "Yes" if result == 1 else "No"

    # 💾 Save user log
    logs = load_json("logs.json")
    logs.append({
        "username": username,
        "moisture": moisture,
        "temperature": temp,
        "result": irrigation,
        "time": str(datetime.datetime.now())
    })
    save_json("logs.json", logs)

    response = {
        "irrigation": irrigation
    }

    response["hash"] = generate_hash(response)

    log_request(ip, "Authorized")

    return jsonify(response)

# =========================
# 📊 VIEW LOGS
# =========================
@app.route('/logs', methods=['GET'])
def logs():
    return jsonify(load_json("logs.json"))

# =========================
@app.route('/')
def home():
    return "Backend Running 🚀"

if __name__ == "__main__":
    app.run(debug=True)