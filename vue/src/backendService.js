const API_BASE_URL = 'http://localhost:3000/api';

class BackendService {
    async _handleResponse(response) {
        const contentType = response.headers?.get?.('content-type') || '';
        const isJson = contentType.includes('application/json');

        let body;
        try {
            body = isJson ? await response.json() : await response.text();
        } catch {
            body = null;
        }

        if (!response.ok) {
            const backendMessage =
                body && typeof body === 'object'
                    ? (body.error || body.message || body.detail || null)
                    : (typeof body === 'string' && body.trim() ? body.trim() : null);

            const message = backendMessage || `HTTP error! status: ${response.status}`;
            const err = new Error(message);
            err.status = response.status;
            err.body = body;
            throw err;
        }

        return body;
    }

    async _get(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        return this._handleResponse(response);
    }

    async _post(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return this._handleResponse(response);
    }

    async _put(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return this._handleResponse(response);
    }

    async _patch(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return this._handleResponse(response);
    }

    async _delete(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE'
        });
        return this._handleResponse(response);
    }
}

class OS2IoTService extends BackendService {
    getHealth() {
        return this._get('/status');
    }
    getDevices() {
        return this._get('/devices');
    }
    patchDevice(id, data) {
        return this._patch(`/devices/${id}`, data);
    }
    addDevice(data) {
        return this._post('/devices', data);
    }
}

export default new OS2IoTService();