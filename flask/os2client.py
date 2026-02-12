import requests
import urllib3
from typing import Optional, Dict, Any

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
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return response.text

    def _post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.post(url, data=data, json=json, headers=headers)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return response.text

    def _put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.put(url, data=data, json=json, headers=headers)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return response.text

    def _patch(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a PATCH request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.patch(url, data=data, json=json, headers=headers)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return response.text

    def _delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        if self.x_api_key:
            headers["X-API-Key"] = self.x_api_key
        response = self.session.delete(url, headers=headers)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return response.text

    def _close(self):
        """Close the session."""
        self.session.close()


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

    def get_devices(self) -> Dict[str, Any]:
        """Get a list of devices."""
        res = self._get(f"/application/{self.application_id}/iot-devices")
        return res.get("data", [])
