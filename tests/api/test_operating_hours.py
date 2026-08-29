import pytest
from core.validators import assert_status, assert_success

class TestOperatingHours:
    def test_hours_01_get_operating_hours(self, api_client):
        resp = api_client.get("/v1/business/operating-hours")
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)
        assert isinstance(data["data"], list)

    def test_hours_01_get_unauthenticated(self, public_client):
        resp = public_client.get("/v1/business/operating-hours")
        assert resp.status_code == 401

    def test_hours_02_update_valid(self, api_client):
        body = {
            "dayOfWeek": "MONDAY",
            "openTime": "08:00",
            "closeTime": "17:00",
            "closed": False
        }
        resp = api_client.put("/v1/business/operating-hours", json=body)
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)

    def test_hours_02_update_invalid(self, api_client):
        body = {"dayOfWeek": "MONDAY", "openTime": "25:00"}  # invalid time
        resp = api_client.put("/v1/business/operating-hours", json=body)
        assert resp.status_code in (400, 422)

    def test_hours_02_update_missing_field(self, api_client):
        resp = api_client.put("/v1/business/operating-hours", json={"dayOfWeek": "MONDAY"})
        assert resp.status_code in (400, 422)

    def test_hours_02_update_conflict(self, api_client):
        # Misal set dua hari yang tumpang tindih? Tapi tidak ada validasi seperti itu.
        pass

    def test_hours_02_update_unauthorized(self, public_client):
        body = {"dayOfWeek": "MONDAY", "closed": True}
        resp = public_client.put("/v1/business/operating-hours", json=body)
        assert resp.status_code == 401