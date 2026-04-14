from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import hashlib
import datetime
from time import time

app = Flask(__name__)
CORS(app)

# 🔐 API KEY
API_KEY = "12345"

# 🤖 Load ML model
model = pickle.load(open('../ml_model/model.pkl', 'rb'))

# 🛡️ Store request logs for rate limiting
request_log = {}

# 📜 Logging function
def log_request(ip, status):
    with open("security_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | IP: {ip} | {status}\n")

# 🔐 Hashing function (data integrity)
def generate_hash(data):
    return hashlib.sha256(str(data).encode()).hexdigest()

# 🚫 RATE LIMIT (FIXED)
@app.before_request
def limit_requests():
    # ✅ Ignore OPTIONS (CORS preflight)
    if request.method == "OPTIONS":
        return

    ip = request.remote_addr
    current_time = time()

    if ip not in request_log:
        request_log[ip] = []

    # Keep only last 30 seconds data
    request_log[ip] = [t for t in request_log[ip] if current_time - t < 30]

    # Increased limit
    if len(request_log[ip]) > 20:
        log_request(ip, "Rate limit exceeded")
        return jsonify({"error": "Too many requests. Try later."}), 429

    request_log[ip].append(current_time)

# 🌱 MAIN API
@app.route('/predict', methods=['POST'])
def predict():
    ip = request.remote_addr

    # 🔐 API KEY CHECK
    client_key = request.headers.get("X-API-KEY")

    if not client_key:
        log_request(ip, "Missing API key")
        return jsonify({"error": "API key missing"}), 401

    if client_key != API_KEY:
        log_request(ip, "Unauthorized access")
        return jsonify({"error": "Unauthorized access"}), 401

    # 📥 Get data
    data = request.json

    if not data:
        log_request(ip, "Empty request body")
        return jsonify({"error": "No data provided"}), 400

    if "moisture" not in data or "temperature" not in data:
        log_request(ip, "Missing fields")
        return jsonify({"error": "Missing required fields"}), 400

    if data["moisture"] == "" or data["temperature"] == "":
        log_request(ip, "Empty field values")
        return jsonify({"error": "Fields cannot be empty"}), 400

    try:
        moisture = int(data['moisture'])
        temp = int(data['temperature'])
    except:
        log_request(ip, "Invalid data type")
        return jsonify({"error": "Invalid data type"}), 400

    # 🤖 ML Prediction
    result = model.predict([[moisture, temp]])[0]

    response = {
        "irrigation": "Yes" if result == 1 else "No",
        "moisture": moisture,
        "temperature": temp
    }

    # 🔐 Add hash for data integrity
    response["hash"] = generate_hash(response)

    log_request(ip, "Authorized request")

    return jsonify(response)

# 🌐 Home route
@app.route('/')
def home():
    return "Smart Farming Backend Running Securely 🚀"

# 🚀 Run server
if __name__ == "__main__":
    app.run(debug=True)