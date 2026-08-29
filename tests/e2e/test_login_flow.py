import time
import random
import pytest
from playwright.sync_api import Page, expect

class TestLoginFlowE2E:
    def test_user_can_login_via_ui(self, page: Page, public_client):
        # 1. Buat user via API (supaya cepat, tidak perlu isi form register)
        email = f"e2e_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        password = "Password123!"
        full_name = "E2E Tester"
        register_body = {
            "fullName": full_name,
            "email": email,
            "password": password,
            "businessName": "E2E Business"
        }
        resp = public_client.post("/v1/auth/register", json=register_body)
        assert resp.status_code == 201, "Setup register failed"

        # 2. Buka halaman login (asumsi frontend di port 5173)
        page.goto("http://localhost:5173/login")  # Sesuaikan dengan URL frontend Anda

        # 3. Isi form login
        page.fill('input[name="email"]', email)  # Sesuaikan selector
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')

        # 4. Tunggu redirect ke dashboard
        page.wait_for_url("http://localhost:5173/dashboard", timeout=10000)

        # 5. Verifikasi elemen di dashboard (misal judul atau nama user)
        # Misal dashboard menampilkan "Welcome, E2E Tester"
        expect(page.locator("h1")).to_contain_text("Dashboard")
        # atau cek nama user muncul di navbar
        expect(page.locator("text=E2E Tester")).to_be_visible()

    def test_login_failed_shows_error(self, page: Page):
        page.goto("http://localhost:5173/login")
        page.fill('input[name="email"]', "wrong@example.com")
        page.fill('input[name="password"]', "wrongpass")
        page.click('button[type="submit"]')

        # Tunggu error muncul
        expect(page.locator(".error-message")).to_be_visible()  # Sesuaikan class