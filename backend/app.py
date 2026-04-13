from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔐 Secret API Key
API_KEY = os.getenv("API_KEY")

# 🤖 Load ML model
model = pickle.load(open('../ml_model/model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():

    # 🔍 Debug: print headers
    print("HEADERS:", request.headers)

    # 🔐 1. API KEY CHECK (Network Security)
    client_key = request.headers.get("X-API-KEY") or request.headers.get("x-api-key")

    print("Received API Key:", client_key)

    if client_key != API_KEY:
        return jsonify({"error": "Unauthorized access"}), 401

    # 📥 2. Get data safely
    data = request.json

    if not data or "moisture" not in data or "temperature" not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        moisture = int(data['moisture'])
        temp = int(data['temperature'])
    except:
        return jsonify({"error": "Invalid data type"}), 400

    # 🤖 3. ML Prediction
    result = model.predict([[moisture, temp]])[0]

    return jsonify({
        "irrigation": "Yes" if result == 1 else "No"
    })

# 🌐 Home route
@app.route('/')
def home():
    return "Smart Farming Backend Running Securely 🚀"

if __name__ == "__main__":
    app.run(debug=True)