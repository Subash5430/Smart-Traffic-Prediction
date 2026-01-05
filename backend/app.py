from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

# Load ML model and scaler
model = tf.keras.models.load_model(
    os.path.join(BASE_DIR, "../models/traffic_lstm.h5")
)
scaler = joblib.load(
    os.path.join(BASE_DIR, "../models/scaler.pkl")
)

# Serve frontend
@app.route("/")
def home():
    return send_from_directory(
        os.path.join(BASE_DIR, "../frontend"),
        "index.html"
    )

@app.route("/script.js")
def script():
    return send_from_directory(
        os.path.join(BASE_DIR, "../frontend"),
        "script.js"
    )

# Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        data["latitude"],
        data["longitude"],
        data["hour"],
        data["day"],
        data["traffic_volume"]
    ]])

    scaled = scaler.transform(features)
    reshaped = scaled.reshape((1, 1, 5))

    prediction = model.predict(reshaped)[0][0]

    # Hybrid decision logic
    risk_level = "High" if (
        prediction > 0.5 or
        data["traffic_volume"] > 700 or
        data["hour"] in [8, 9, 18, 19, 20]
    ) else "Low"

    return jsonify({
        "city": data["city"],
        "accident_risk": round(float(prediction), 2),
        "risk_level": risk_level
    })

if __name__ == "__main__":
    app.run(debug=True)
