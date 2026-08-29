import pytest
from core.validators import assert_status

pytestmark = pytest.mark.skip(reason="Google Calendar credentials not configured and webhook not implemented yet")

class TestGoogle:
    def test_google_01_connect_authenticated(self, api_client):
        resp = api_client.get("/v1/integrations/google/calendar/connect")
        assert_status(resp, 200)
        data = resp.json()
        assert "authorizationUrl" in data

    def test_google_01_connect_unauthenticated(self, public_client):
        resp = public_client.get("/v1/integrations/google/calendar/connect")
        assert resp.status_code == 401

    def test_google_02_webhook_no_channel_id(self, public_client):
        resp = public_client.post("/v1/integrations/google/calendar/webhook")
        assert_status(resp, 200)

    def test_google_02_webhook_valid_headers(self, public_client):
        headers = {"X-Goog-Channel-ID": "test", "X-Goog-Resource-ID": "res", "X-Goog-Resource-State": "sync"}
        resp = public_client.post("/v1/integrations/google/calendar/webhook", headers=headers)
        assert_status(resp, 200)

    def test_google_02_webhook_invalid_channel(self, public_client):
        headers = {"X-Goog-Channel-ID": "unknown"}
        resp = public_client.post("/v1/integrations/google/calendar/webhook", headers=headers)
        assert resp.status_code in (200, 400)

    def test_google_03_callback_valid(self, public_client):
        params = {"code": "testcode", "state": "teststate"}
        resp = public_client.get("/v1/integrations/google/calendar/callback", params=params, allow_redirects=False)
        assert_status(resp, 302)

    def test_google_03_callback_cancelled(self, public_client):
        params = {"error": "access_denied"}
        resp = public_client.get("/v1/integrations/google/calendar/callback", params=params, allow_redirects=False)
        assert_status(resp, 302)

    def test_google_03_callback_missing_state(self, public_client):
        params = {"code": "testcode"}
        resp = public_client.get("/v1/integrations/google/calendar/callback", params=params, allow_redirects=False)
        assert resp.status_code == 302

    def test_google_03_callback_missing_code(self, public_client):
        params = {"state": "teststate"}
        resp = public_client.get("/v1/integrations/google/calendar/callback", params=params, allow_redirects=False)
        assert resp.status_code == 302

    def test_google_03_callback_invalid_state(self, public_client):
        params = {"code": "testcode", "state": "invalid"}
        resp = public_client.get("/v1/integrations/google/calendar/callback", params=params, allow_redirects=False)
        assert resp.status_code == 302

    def test_google_04_status_connected(self, api_client):
        resp = api_client.get("/v1/integrations/google/calendar/status")
        assert_status(resp, 200)
        data = resp.json()
        assert "connected" in data

    def test_google_04_status_unauthenticated(self, public_client):
        resp = public_client.get("/v1/integrations/google/calendar/status")
        assert resp.status_code == 401

    def test_google_05_disconnect_connected(self, api_client):
        resp = api_client.delete("/v1/integrations/google/calendar/disconnect")
        assert resp.status_code in (200, 204)

    def test_google_05_disconnect_already_disconnected(self, api_client):
        resp = api_client.delete("/v1/integrations/google/calendar/disconnect")
        assert resp.status_code in (200, 204, 400)

    def test_google_05_disconnect_unauthenticated(self, public_client):
        resp = public_client.delete("/v1/integrations/google/calendar/disconnect")
        assert resp.status_code == 401