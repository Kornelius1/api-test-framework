import time
import random
import pytest
from core.api_client import ApiClient
from core.validators import assert_status, assert_success, assert_response_has_fields

class TestAuth:
    def test_auth_01_login_valid(self, public_client):
        email = f"test_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        password = "Password123!"
        register_body = {
            "fullName": "Test User",
            "email": email,
            "password": password,
            "businessName": "Test Business"
        }
        resp = public_client.post("/v1/auth/register", json=register_body)
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
        login_body = {"email": email, "password": password}
        resp = public_client.post("/v1/auth/login", json=login_body)
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)
        assert_response_has_fields(data["data"], ["token", "user", "business"])

    def test_auth_01_login_invalid_credentials(self, public_client):
        login_body = {"email": "wrong@example.com", "password": "wrong"}
        resp = public_client.post("/v1/auth/login", json=login_body)
        assert resp.status_code in (400, 401)

    def test_auth_01_login_invalid_body(self, public_client):
        resp = public_client.post("/v1/auth/login", json={"email": "x"})
        assert resp.status_code in (400, 422)

    def test_auth_01_login_missing_fields(self, public_client):
        resp = public_client.post("/v1/auth/login", json={})
        assert resp.status_code in (400, 422)

    def test_auth_02_register_valid(self, public_client):
        email = f"test_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        body = {
            "fullName": "New User",
            "email": email,
            "password": "Password123!",
            "businessName": "New Business"
        }
        resp = public_client.post("/v1/auth/register", json=body)
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
        data = resp.json()
        assert_success(data)
        assert_response_has_fields(data["data"], ["user", "business"])

    def test_auth_02_register_duplicate_email(self, public_client):
        email = f"test_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        body = {
            "fullName": "User A",
            "email": email,
            "password": "Password123!",
            "businessName": "Business A"
        }
        # Register pertama harus sukses
        resp1 = public_client.post("/v1/auth/register", json=body)
        assert resp1.status_code == 201, f"First register failed: {resp1.text}"
        # Register kedua dengan email yang sama harus conflict
        resp2 = public_client.post("/v1/auth/register", json=body)
        assert resp2.status_code in (400, 409), f"Expected 400/409, got {resp2.status_code}"

    def test_auth_02_register_invalid_email(self, public_client):
        body = {
            "fullName": "User",
            "email": "not-an-email",
            "password": "Password123!",
            "businessName": "Business"
        }
        resp = public_client.post("/v1/auth/register", json=body)
        assert resp.status_code in (400, 422)

    def test_auth_02_register_missing_fields(self, public_client):
        resp = public_client.post("/v1/auth/register", json={"email": "x@x.com"})
        assert resp.status_code in (400, 422)

    def test_auth_02_register_invalid_password(self, public_client):
        body = {
            "fullName": "User",
            "email": "valid@example.com",
            "password": "short",
            "businessName": "Business"
        }
        resp = public_client.post("/v1/auth/register", json=body)
        assert resp.status_code in (400, 422)

    def test_auth_03_current_user_valid(self, api_client):
        resp = api_client.get("/v1/auth/me")
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)
        assert_response_has_fields(data["data"], ["user", "business"])

    def test_auth_03_current_user_no_jwt(self, public_client):
        resp = public_client.get("/v1/auth/me")
        # Bisa 401 atau 403 tergantung implementasi
        assert resp.status_code == 401

    def test_auth_03_current_user_invalid_jwt(self, public_client):
        # Gunakan base_url dari public_client
        client = ApiClient(public_client.base_url, "invalid.token.here")
        resp = client.get("/v1/auth/me")
        assert resp.status_code in (401, 403)