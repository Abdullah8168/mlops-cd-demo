import os
from flask import Flask, jsonify, request

app = Flask(__name__)

MODEL_VERSION = "model-7"
APP_VERSION = os.getenv("APP_VERSION") or open("VERSION").read().strip()
GIT_COMMIT = os.getenv("GIT_COMMIT", "local")


@app.route("/")
def home():
    return jsonify({"service": "mlops-demo", "status": "running"})


@app.route("/health")
def health():
    return jsonify({
        "application_version": APP_VERSION,
        "model_version": MODEL_VERSION,
        "git_commit": GIT_COMMIT,
        "status": "healthy",
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    value = float(data["value"])
    prediction = value * 2  # dummy model
    return jsonify({
        "input": value,
        "prediction": prediction,
        "model_version": MODEL_VERSION,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
