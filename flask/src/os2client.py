import logging
import re

import requests
import urllib3
from typing import Optional, Dict, Any

from utils.config import OS2_DATA_TARGET_ID, OS2_DEVICE_PROFILE_ID

logger = logging.getLogger(__name__)


def _strip(s: str) -> str:
    """Strip leading/trailing whitespace and newlines from a string."""
    stripped = s.strip() if isinstance(s, str) else s
    if stripped == "":
        return None
    return stripped


class APIClient:
    def __init__(self, base_url: str, x_api_key: str | None = None, verify: bool | str = True):
        """Initialize the API client with a base URL.

        The `verify` parameter behaves like `requests`'s verify: it can be a
        boolean or a path to a CA bundle. Setting `verify=False` is useful for
        local testing when the remote server serves a chain that Python's
        cert bundle can't validate.
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.x_api_key = x_api_key
        self.verify = verify
        # Apply verification behavior to the session so all requests use it
        self.session.verify = verify
        # If verification is disabled, suppress the insecure request warning
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.get(url, params=params, headers=headers)
        return self._handle_response(response)

    def _post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.post(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def _put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.put(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def _patch(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a PATCH request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.patch(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def _delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.delete(url, headers=headers)
        return self._handle_response(response)

    def _close(self):
        """Close the session."""
        self.session.close()

    def _handle_response(self, response):
        """Process a requests.Response: return parsed JSON or text.

        If the response has an HTTP error status, raise an HTTPError
        that includes the response body (JSON or text) to help debugging.
        """
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            try:
                content = response.json()
            except Exception:
                content = response.text
            raise requests.HTTPError(f"{e}\nResponse content: {content}", response=response)

        try:
            return response.json()
        except Exception:
            return response.text


class OS2Client(APIClient):
    def __init__(self, base_url: str, application_id: int, x_api_key: str | None = None, verify: bool | str = True):
        """Initialize the OS2Client with a base URL.

        Forward `verify` to the base API client so callers may control SSL
        verification behavior.
        """
        self.application_id = application_id
        super().__init__(base_url, x_api_key=x_api_key, verify=verify)

    def get_health(self) -> Dict[str, Any]:
        """Get the health status of the OS2IoT API."""
        return self._get("/healthcheck")

    def _set_data_target(self, device_id: int, device_model: dict) -> Dict[str, Any]:
        """Set the data target for a device."""
        if not OS2_DATA_TARGET_ID:
            raise ValueError("OS2_DATA_TARGET_ID is not set in environment variables")
        if not device_model or not isinstance(device_model, dict):
            raise ValueError("device_model is required and must be a dictionary")

        # GET desired payload decoder from device model name
        decoders = self._get("/payload-decoder/minimal")
        decoder_string_id = str(device_model.get("body").get("id"))
        pattern = re.compile(rf"^Randers \[Ento\] .* <id:{re.escape(decoder_string_id)}>$")
        decoder = next((pd for pd in decoders.get("data", []) if pattern.match(str(pd.get("name", "")))), None)
        decoder_id = decoder.get("id") if decoder else None

        if not decoder_id:
            raise ValueError(f"No matching payload decoder found for device model ID {decoder_string_id}")

        # GET existing data target connections, and find an active connection for application if it exists
        device_connections = self._get(f"/iot-device-payload-decoder-data-target-connection/byIotDevice/{device_id}")
        active_device_connection = next((conn for conn in device_connections.get("data", []) if conn.get("dataTarget").get("id") == OS2_DATA_TARGET_ID), None)

        if active_device_connection:
            active_decoder_id = active_device_connection.get("payloadDecoder").get("id") if active_device_connection else None

            # If the active decoder is already correct, do nothing
            if active_decoder_id == decoder_id:
                logger.info(f"Data target connection for device {device_id} already has the correct decoder {decoder_id}; no update needed")
                return True

            # Otherwise, remove the device from the existing connection (if any)
            # First, refetch device connection to get entire device list for that payload decoder
            decoder_connections = self._get(f"/iot-device-payload-decoder-data-target-connection/byDataTarget/{OS2_DATA_TARGET_ID}")
            active_device_connection = next((conn for conn in decoder_connections.get("data", []) if conn.get("payloadDecoder").get("id") == active_decoder_id), None)

            iot_device_ids = [device.get("id") for device in active_device_connection.get("iotDevices", [])]
            iot_device_ids.remove(device_id)  # Remove the device from the existing connection's device list
            update_payload = {
                "dataTargetId": OS2_DATA_TARGET_ID,
                "payloadDecoderId": active_decoder_id,
                "iotDeviceIds": iot_device_ids
            }
            connection_id = active_device_connection.get("id")
            self._put(f"/iot-device-payload-decoder-data-target-connection/{connection_id}", json=update_payload)
            logger.info(f"Deleted existing data target connection {connection_id} for device {device_id} to prepare for decoder update")

        # Update the connection for the new decoder,
        # either by reusing the existing connection or creating a new one
        # First, GET existing connections to find an existing connection for the new decoder (decoder_id)
        decoder_connections = self._get(f"/iot-device-payload-decoder-data-target-connection/byDataTarget/{OS2_DATA_TARGET_ID}")
        existing_decoder_connection = next((conn for conn in decoder_connections.get("data", []) if conn.get("payloadDecoder").get("id") == decoder_id), None)

        if existing_decoder_connection:
            # If a connection already exists for the new decoder, reuse it
            iot_device_ids = [device.get("id") for device in existing_decoder_connection.get("iotDevices", [])]
            iot_device_ids.append(device_id)  # Add the new device to the existing connection's device list
            update_payload = {
                "dataTargetId": OS2_DATA_TARGET_ID,
                "payloadDecoderId": decoder_id,
                "iotDeviceIds": iot_device_ids
            }
            connection_id = existing_decoder_connection.get("id")
            self._put(f"/iot-device-payload-decoder-data-target-connection/{connection_id}", json=update_payload)
            logger.info(f"Updated existing data target connection {connection_id} to use device {device_id} and decoder {decoder_id}")

            return True

        # else:
            # If no connection exists for this application/device, create a new one
            # TODO: Implement logic

        return False  # Placeholder until decoder logic is implemented

    def get_devices(self) -> Dict[str, Any]:
        """Get a list of devices."""
        res = self._get(f"/application/{self.application_id}/iot-devices")
        return res.get("data", [])

    def patch_device(self, device: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch a device, overwrite fields from `device`, then PUT the result.

        The input `device` must contain an `id` key. The method will GET
        `/iot-device/{id}`, merge values from the provided `device` dict
        (overwriting any existing keys), then PUT the merged payload back
        to `/iot-device/{id}` and return the response.
        """
        if not isinstance(device, dict):
            raise TypeError("device must be a dict")

        required_keys = {"id"}

        if any(key not in device for key in required_keys):
            raise ValueError("device dict must include the following keys: " + ", ".join(required_keys))

        device_id = device["id"]

        # GET current device values
        current_payload = self._get(f"/iot-device/{device_id}")
        for key in current_payload.keys():
            current_payload[key] = _strip(current_payload[key])

        if not isinstance(current_payload, dict):
            # Device not found, raise error
            raise ValueError(f"Device with ID {device_id} was not found or OS2IoT API returned invalid data: {current_payload}")

        # TODO: Update data target if device-model has changed and OS2_DATA_TARGET_ID is set
        # if OS2_DATA_TARGET_ID and "deviceModelId" in current_payload and current_payload["deviceModelId"] != device.get("deviceModelId"):
        #     current_payload["dataTargetId"] = OS2_DATA_TARGET_ID

        # Overwrite with provided values
        merged = dict(current_payload)
        merged.update(device)

        # Check id and add applicationId
        if "id" not in merged:
            merged["id"] = device_id
        merged["applicationId"] = self.application_id

        # Move deviceModelId from deviceModel to top-level if missing
        if "deviceModelId" not in merged:
            if "deviceModel" in merged and isinstance(merged["deviceModel"], dict):
                device_model = merged["deviceModel"]
                if "id" in device_model:
                    merged["deviceModelId"] = device_model["id"]
                    del merged["deviceModel"]  # Remove nested deviceModel after extracting id
                else:
                    logger.error(f"deviceModel for device {device_id} does not contain an 'id' field")
            else:
                logger.error(f"No valid deviceModel found for device {device_id}; cannot extract deviceModelId")

        # Delete latest data from payload
        del merged["receivedMessagesMetadata"]

        # PUT the merged device back to the same endpoint
        res = self._put(f"/iot-device/{device_id}", json=merged)
        return res

    def create_device(self, device: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new device.

        This method will POST the `device` payload to
        `/application/{application_id}/iot-device` and return the response.
        """
        if not isinstance(device, dict):
            raise TypeError("device must be a dict")

        required_keys = {"name", "OTAAapplicationKey", "deviceEUI"}

        if any(key not in device for key in required_keys):
            raise ValueError("device dict must include the following keys: " + ", ".join(required_keys))

        # Build payload
        device["name"] = device["name"]
        device["applicationId"] = self.application_id
        device["type"] = "LORAWAN"
        device["lorawanSettings"] = {
            "activationType": "OTAA",
            "devEUI": device["deviceEUI"],
            "OTAAapplicationKey": device["OTAAapplicationKey"],
            "skipFCntCheck": False,
            "isDisabled": False,
            "deviceProfileID": OS2_DEVICE_PROFILE_ID
        }
        device["comment"] = device.get("comment", "")
        device["commentOnLocation"] = device.get("commentOnLocation", "")
        device["deviceModelId"] = device.get("deviceModelId", None)

        res = self._post("/iot-device", json=device)
        return res

    def get_device_models(self) -> Dict[str, Any]:
        """Get a list of device models."""
        res = self._get("/device-model")
        return res.get("data", [])
