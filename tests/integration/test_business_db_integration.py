import time
import random
import pytest
from core.validators import assert_success

class TestBusinessDBIntegration:

    def test_business_created_during_register_has_correct_data(self, public_client, db):
        # Buat user baru via register
        full_name = "User Business Test"
        business_name = f"Biz {int(time.time())} {random.randint(1000,9999)}"
        email = f"test_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        password = "Password123!"

        register_body = {
            "fullName": full_name,
            "email": email,
            "password": password,
            "businessName": business_name
        }

        resp = public_client.post("/v1/auth/register", json=register_body)
        assert resp.status_code == 201, f"Register gagal: {resp.text}"
        data = resp.json()
        assert_success(data)

        # Verifikasi di database
        business = db.get_business_by_name(business_name)
        assert business is not None, f"Business '{business_name}' tidak ditemukan di DB!"

        assert business["name"] == business_name
        assert business["slug"] is not None
        assert business["status"] == "ACTIVE"

        print(f"✅ Business berhasil diverifikasi: {business}")

    def test_business_has_unique_slug(self, public_client, db):
        # Buat business pertama
        name1 = f"Biz {int(time.time())} {random.randint(1000,9999)}"
        email1 = f"test_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        reg1 = {
            "fullName": "User One",
            "email": email1,
            "password": "Password123!",
            "businessName": name1
        }
        resp1 = public_client.post("/v1/auth/register", json=reg1)
        assert resp1.status_code == 201, f"Register 1 gagal: {resp1.text}"
        biz1 = db.get_business_by_name(name1)
        slug1 = biz1["slug"]

        # Buat business kedua
        time.sleep(0.1)
        name2 = f"Biz {int(time.time())} {random.randint(1000,9999)}"
        email2 = f"test_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        reg2 = {
            "fullName": "User Two",
            "email": email2,
            "password": "Password123!",
            "businessName": name2
        }
        resp2 = public_client.post("/v1/auth/register", json=reg2)
        assert resp2.status_code == 201, f"Register 2 gagal: {resp2.text}"
        biz2 = db.get_business_by_name(name2)
        slug2 = biz2["slug"]

        assert slug1 != slug2, f"Slug harus unik, tapi '{slug1}' dan '{slug2}' sama!"
        print(f"✅ Slug unik: {slug1} vs {slug2}")

    def test_business_from_context_matches_database(self, ctx, db):
        """
        Verifikasi bahwa data business yang tersimpan di context
        (dari response register/login) cocok dengan database.
        """
        # Ambil data dari context
        business_id = ctx.business_id
        business_slug = ctx.business_slug

        # Query database berdasarkan ID
        rows = db.execute_query("SELECT * FROM businesses WHERE id = :id", {"id": business_id})
        assert rows, f"Business dengan ID {business_id} tidak ditemukan di DB"
        business = rows[0]

        # Bandingkan
        assert business["id"] == business_id
        assert business["slug"] == business_slug
        # Name tidak ada di context, tapi kita bisa ambil dari database jika perlu
        # Kita hanya verifikasi field yang ada di context

        print(f"✅ Business dari context cocok dengan DB: {business['name']} (slug: {business['slug']})")