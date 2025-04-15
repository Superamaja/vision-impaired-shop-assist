from threading import Thread

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.config import Config
from src.db.models import BarcodeExistsError, DatabaseManager

app = Flask(__name__)
CORS(app)
db_manager = DatabaseManager()
db_manager.init_db()


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


@app.route("/api/barcodes", methods=["GET"])
def get_barcodes():
    barcodes = db_manager.get_all_barcodes()
    return jsonify(
        [
            {"barcode": b.barcode, "product_name": b.product_name, "brand": b.brand}
            for b in barcodes
        ]
    )


@app.route("/api/barcodes/<barcode>", methods=["GET"])
def get_barcode(barcode):
    result = db_manager.get_barcode(barcode)
    if not result:
        return jsonify({"error": "Barcode not found"}), 404
    return jsonify(
        {
            "barcode": result.barcode,
            "product_name": result.product_name,
            "brand": result.brand,
        }
    )


@app.route("/api/barcodes", methods=["POST"])
def add_barcode():
    data = request.get_json()
    if not data or not all(k in data for k in ["barcode", "product_name", "brand"]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        barcode_data = db_manager.add_barcode(
            data["barcode"], data["product_name"], data["brand"]
        )
        return jsonify(barcode_data), 201
    except BarcodeExistsError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/barcodes/<barcode>", methods=["DELETE"])
def delete_barcode(barcode):
    if db_manager.delete_barcode(barcode):
        return jsonify({"message": "Barcode deleted"}), 200
    return jsonify({"error": "Barcode not found"}), 404


def run_api(host="0.0.0.0", port=5001):
    app.run(host=host, port=port, debug=False, threaded=True)


def start_server():
    Thread(target=run_api, daemon=True).start()
