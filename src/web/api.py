"""
REST API for the Vision-Impaired Shopping Assistant.

This module provides HTTP endpoints for managing application settings
and barcode database operations. The API allows external clients to:
- Get/update configuration settings
- CRUD operations for barcode entries
- Integration with the main application

Endpoints:
    GET /api/settings - Retrieve current settings
    POST /api/settings - Update settings
    GET /api/barcodes - Get all barcodes
    POST /api/barcodes - Add new barcode
    GET /api/barcodes/<id> - Get specific barcode
    DELETE /api/barcodes/<id> - Delete barcode
"""

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
    """
    Get all current configuration settings.

    Returns:
        JSON response containing all configuration settings
    """
    return jsonify(Config.get_all_settings())


@app.route("/api/settings", methods=["POST"])
def update_settings():
    """
    Update configuration settings.

    Expects JSON payload with setting key-value pairs.

    Returns:
        JSON response with successfully updated settings

    Raises:
        400: If no settings provided in request body
    """
    settings = request.get_json()
    if not settings:
        return jsonify({"error": "No settings provided"}), 400

    updated = Config.update_settings(settings)
    print("Settings:", Config.get_all_settings())
    return jsonify({"updated": updated})


@app.route("/api/barcodes", methods=["GET"])
def get_barcodes():
    """
    Retrieve all barcode entries from the database.

    Returns:
        JSON array containing all barcode entries with their details
    """
    barcodes = db_manager.get_all_barcodes()
    return jsonify(
        [
            {
                "barcode": b.barcode,
                "product_name": b.product_name,
                "brand": b.brand,
                "allergies": b.allergies,
            }
            for b in barcodes
        ]
    )


@app.route("/api/barcodes/<barcode>", methods=["GET"])
def get_barcode(barcode):
    """
    Retrieve a specific barcode entry by its ID.

    Args:
        barcode (str): The barcode identifier to lookup

    Returns:
        JSON object containing barcode details

    Raises:
        404: If barcode is not found in database
    """
    result = db_manager.get_barcode(barcode)
    if not result:
        return jsonify({"error": "Barcode not found"}), 404
    return jsonify(
        {
            "barcode": result.barcode,
            "product_name": result.product_name,
            "brand": result.brand,
            "allergies": result.allergies,
        }
    )


@app.route("/api/barcodes", methods=["POST"])
def add_barcode():
    """
    Add a new barcode entry to the database.

    Expects JSON payload with required fields: barcode, product_name, brand.
    Optional field: allergies.

    Returns:
        JSON object containing the created barcode entry

    Raises:
        400: If required fields are missing
        409: If barcode already exists
        400: For other database errors
    """
    data = request.get_json()
    if not data or not all(k in data for k in ["barcode", "product_name", "brand"]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        barcode_data = db_manager.add_barcode(
            data["barcode"],
            data["product_name"],
            data["brand"],
            data.get("allergies"),  # Optional field
        )
        return jsonify(barcode_data), 201
    except BarcodeExistsError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/barcodes/<barcode>", methods=["DELETE"])
def delete_barcode(barcode):
    """
    Delete a barcode entry from the database.

    Args:
        barcode (str): The barcode identifier to delete

    Returns:
        JSON confirmation message if successful

    Raises:
        404: If barcode is not found
    """
    if db_manager.delete_barcode(barcode):
        return jsonify({"message": "Barcode deleted"}), 200
    return jsonify({"error": "Barcode not found"}), 404


def run_api(host="0.0.0.0", port=5001):
    """
    Start the Flask API server.

    Args:
        host (str): Host address to bind to, defaults to all interfaces
        port (int): Port number to listen on, defaults to 5001
    """
    app.run(host=host, port=port, debug=False, threaded=True)


def start_server():
    """
    Start the API server in a background daemon thread.

    This allows the API to run alongside the main application
    without blocking the main execution thread.
    """
    Thread(target=run_api, daemon=True).start()
