import time
import random
import pytest
from core.validators import assert_status, assert_success

class TestAuthDBIntegration:
    def test_register_saves_user_to_db(self, public_client, db):
        email = f"test_db_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        password = "Password123!"
        full_name = "Integration Test User"
        business_name = "Integration Biz"

        # 1. Register via API
        register_body = {
            "fullName": full_name,
            "email": email,
            "password": password,
            "businessName": business_name
        }
        resp = public_client.post("/v1/auth/register", json=register_body)
        assert resp.status_code == 201, f"Register failed: {resp.text}"
        data = resp.json()
        assert_success(data)

        # 2. Verifikasi langsung ke database
        user = db.get_user_by_email(email)
        assert user is not None, f"User with email {email} not found in DB"
        # user adalah tuple/row, index tergantung struktur tabel.
        # Asumsikan kolom ke-2 adalah full_name, sesuaikan dengan tabel Anda.
        # Alternatif: gunakan SQLAlchemy ORM jika mau lebih rapi.
        print(f"User found in DB: {user}")

        # 3. Verifikasi Business juga tersimpan
        business = db.get_business_by_name(business_name)
        assert business is not None, f"Business {business_name} not found in DB"
        print(f"Business found in DB: {business}")

    def test_login_uses_valid_user_from_db(self, public_client, db):
        # Buat user via API dulu
        email = f"test_login_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        password = "Password123!"
        register_body = {
            "fullName": "Login Test",
            "email": email,
            "password": password,
            "businessName": "Login Biz"
        }
        public_client.post("/v1/auth/register", json=register_body)

        # Cek user ada di DB
        user = db.get_user_by_email(email)
        assert user is not None

        # Login via API
        login_body = {"email": email, "password": password}
        resp = public_client.post("/v1/auth/login", json=login_body)
        assert_status(resp, 200)
        assert_success(resp.json())