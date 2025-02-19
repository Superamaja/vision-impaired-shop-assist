from threading import Thread

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.config import Config

app = Flask(__name__)
CORS(app)


@app.route("/api/settings", methods=["GET"])
def get_settings():
    return jsonify(Config.get_all_settings())


@app.route("/api/settings", methods=["POST"])
def update_settings():
    settings = request.get_json()
    if not settings:
        return jsonify({"error": "No settings provided"}), 400

    updated = Config.update_settings(settings)
    print("Settings:", Config.get_all_settings())
    return jsonify({"updated": updated})


def run_api(host="0.0.0.0", port=5000):
    app.run(host=host, port=port, debug=False, threaded=True)


def start_server():
    Thread(target=run_api, daemon=True).start()
