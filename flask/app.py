from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
from config import OS2_API_BASE_URL, OS2_APPLICATION_ID, OS2_API_KEY, OS2_VERIFY
from os2client import OS2Client
import time

app = Flask(__name__)

# Allow cross-origin requests during development
# Restrict origins in production as appropriate
CORS(app)

# Initialize OS2Client using environment variables with sensible defaults
try:
    os2_client = OS2Client(
        base_url=OS2_API_BASE_URL,
        application_id=OS2_APPLICATION_ID,
        x_api_key=OS2_API_KEY,
        verify=OS2_VERIFY,
    )
    logging.getLogger(__name__).info("OS2Client initialized")
except Exception:
    logging.exception("Failed to initialize OS2Client; continuing with os2_client=None")
    os2_client = None


@app.route("/health", methods=["GET"])
def health():
    os2_status = "ok" if os2_client else "error"
    return jsonify({
        "status": "ok",
        "os2_client_status": os2_status,
        "os2_verify": OS2_VERIFY,
        "os2_health": os2_client.get_health() if os2_client else None
    }), 200

@app.route("/api/devices", methods=["GET"])
def get_devices():
    if not os2_client:
        return jsonify({"error": "OS2Client not initialized"}), 500
    try:
        devices = os2_client.get_devices()
        return jsonify({"devices": devices}), 200
    except Exception as e:
        logging.exception("Error fetching devices from OS2Client")
        return jsonify({"error": str(e)}), 500

@app.route("/api/devices/<int:device_id>", methods=["PATCH"])
def patch_device(device_id: int):
    if not os2_client:
        return jsonify({"error": "OS2Client not initialized"}), 500

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    # Ensure the payload contains the id expected by the client library
    payload["id"] = device_id

    try:
        result = os2_client.patch_device(payload)
        return jsonify(result), 200
    except Exception as e:
        logging.exception("Error patching device via OS2Client")
        return jsonify({"error": str(e)}), 500

@app.route("/api/devices", methods=["POST"])
def add_device():
    return request.get_json(silent=True) or {}, 201
    if not os2_client:
        return jsonify({"error": "OS2Client not initialized"}), 500

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    try:
        result = os2_client.add_device(payload)
        return jsonify(result), 201
    except Exception as e:
        logging.exception("Error adding device via OS2Client")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Enable development features when running directly:
    # - debug=True enables the interactive debugger and sets logging to DEBUG
    # - use_reloader=True restarts the process when source files change
    # - TEMPLATES_AUTO_RELOAD makes template changes reload without restart
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
