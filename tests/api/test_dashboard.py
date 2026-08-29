import pytest
from core.validators import assert_status, assert_success, assert_response_has_fields

class TestDashboard:
    def test_dash_01_get_dashboard_authenticated(self, api_client):
        resp = api_client.get("/v1/business/dashboard")
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)
        assert_response_has_fields(data["data"], ["summary", "recentActivities", "todayReservations", "resourceAvailability"])

    def test_dash_01_get_dashboard_unauthenticated(self, public_client):
        resp = public_client.get("/v1/business/dashboard")
        assert resp.status_code == 401

    def test_dash_01_get_dashboard_business_isolation(self, api_client):
        # Hanya bisa test dengan satu business
        pass