import pytest
from core.api_client import ApiClient
from core.validators import assert_status

class TestPublicReservation:
    def test_public_res_01_create_valid(self, public_client, ctx):
        import time
        body = {
            "resourceId": ctx.resource_id,
            "reservationDate": "2026-09-02",
            "startTime": "09:00",
            "endTime": "10:00",
            "customer": {
                "fullName": f"Public_{int(time.time())}",
                "email": f"pub_{int(time.time())}@test.com",
                "phone": "08123456789"
            },
            "note": "test note"
        }
        resp = public_client.post(f"/public/{ctx.business_slug}/reservations", json=body)
        assert_status(resp, 201)
        data = resp.json()
        assert "data" in data

    def test_public_res_01_business_not_found(self, public_client):
        body = {"resourceId": 1, "reservationDate": "2026-09-01", "startTime": "10:00", "endTime": "11:00", "customer": {"fullName": "x", "phone": "x"}}
        resp = public_client.post("/public/invalid-slug/reservations", json=body)
        assert resp.status_code == 404

    def test_public_res_01_invalid_request(self, public_client, ctx):
        body = {"resourceId": ctx.resource_id, "reservationDate": "invalid"}
        resp = public_client.post(f"/public/{ctx.business_slug}/reservations", json=body)
        assert resp.status_code in (400, 422)

    def test_public_res_01_missing_field(self, public_client, ctx):
        resp = public_client.post(f"/public/{ctx.business_slug}/reservations", json={})
        assert resp.status_code in (400, 422)

    def test_public_res_01_resource_not_found(self, public_client, ctx):
        body = {"resourceId": 99999, "reservationDate": "2026-09-01", "startTime": "10:00", "endTime": "11:00", "customer": {"fullName": "x", "phone": "x"}}
        resp = public_client.post(f"/public/{ctx.business_slug}/reservations", json=body)
        assert resp.status_code == 404

    def test_public_res_01_resource_unavailable(self, public_client, ctx):
        api_client = ApiClient("http://localhost:8080/api", ctx.token)
        api_client.put(f"/resources/{ctx.resource_id}", json={"status": "UNAVAILABLE"})
        body = {"resourceId": ctx.resource_id, "reservationDate": "2026-09-01", "startTime": "10:00", "endTime": "11:00", "customer": {"fullName": "x", "phone": "x"}}
        resp = public_client.post(f"/public/{ctx.business_slug}/reservations", json=body)
        assert resp.status_code in (400, 409)
        api_client.put(f"/resources/{ctx.resource_id}", json={"status": "AVAILABLE"})

    def test_public_res_01_reservation_conflict(self, public_client, ctx):
        body = {
            "resourceId": ctx.resource_id,
            "reservationDate": "2026-09-03",
            "startTime": "10:00",
            "endTime": "11:00",
            "customer": {"fullName": "Conflict", "phone": "081234"}
        }
        public_client.post(f"/public/{ctx.business_slug}/reservations", json=body)
        resp = public_client.post(f"/public/{ctx.business_slug}/reservations", json=body)
        assert resp.status_code in (400, 409)