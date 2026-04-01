import logging

from flask import Blueprint, jsonify, request
from utils.config import OS2_API_BASE_URL, OS2_APPLICATION_ID, OS2_API_KEY, OS2_VERIFY, DEVELOPER_MODE
from os2client import OS2Client

logger = logging.getLogger(__name__)
api_endpoints = Blueprint('api', __name__, url_prefix='/api')

# Initialize OS2Client using environment variables
try:
    os2_client = OS2Client(
        base_url=OS2_API_BASE_URL,
        application_id=OS2_APPLICATION_ID,
        x_api_key=OS2_API_KEY,
        verify=OS2_VERIFY,
    )
    logger.info("OS2Client initialized")
except Exception:
    logger.exception("Failed to initialize OS2Client; continuing with os2_client=None")
    os2_client = None


@api_endpoints.route('/status', methods=['GET'])
def status():
    os2_status = "ok" if os2_client else "error"
    return jsonify({
        "success": True, "message":
        "API is up and running",
        "os2_client_status": os2_status,
        "os2_verify": OS2_VERIFY,
        "os2_health": os2_client.get_health() if os2_client else None}), 200


@api_endpoints.route("/settings", methods=["GET"])
def get_settings():
    if not os2_client:
        return jsonify({"error": "OS2Client not initialized"}), 500
    try:
        device_models = os2_client.get_device_models()
        return jsonify({
            "deviceModels": device_models,
            "developerMode": DEVELOPER_MODE
        }), 200
    except Exception as e:
        logger.exception("Error fetching device models from OS2Client")
        return jsonify({"error": str(e)}), 500


@api_endpoints.route("/devices", methods=["GET"])
def get_devices():
    if not os2_client:
        return jsonify({"error": "OS2Client not initialized"}), 500
    try:
        devices = os2_client.get_devices()
        return jsonify({"devices": devices}), 200
    except Exception as e:
        logger.exception("Error fetching devices from OS2Client")
        return jsonify({"error": str(e)}), 500


@api_endpoints.route("/devices/<int:device_id>", methods=["PATCH"])
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
        logger.exception("Error patching device via OS2Client")
        return jsonify({"error": str(e)}), 500


@api_endpoints.route("/devices", methods=["POST"])
def add_device():
    if not os2_client:
        return jsonify({"error": "OS2Client not initialized"}), 500

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    try:
        result = os2_client.create_device(payload)
        return jsonify(result), 201
    except Exception as e:
        logger.exception("Error adding device via OS2Client")
        return jsonify({"error": str(e)}), 500
