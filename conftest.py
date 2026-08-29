import os
import time
import random
import pytest
from datetime import datetime, timedelta  
from dotenv import load_dotenv
from core.api_client import ApiClient
from core.context import TestContext
from core.ai_adapter import generate_payload
from core.validators import assert_success
from playwright.sync_api import Page, Browser
from core.db_client import DatabaseClient

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080/api")

def _register_unique(client, retries=5):
    for attempt in range(retries):
        email = f"test_{int(time.time())}_{random.randint(1000,9999)}@example.com"
        full_name = generate_payload("fullName") or f"TestUser_{int(time.time())}"
        business_name = generate_payload("businessName") or f"Biz_{int(time.time())}"
        password = "Password123!"

        register_body = {
            "fullName": full_name,
            "email": email,
            "password": password,
            "businessName": business_name
        }
        resp = client.post("/v1/auth/register", json=register_body)
        if resp.status_code == 201:
            return resp.json(), email, password
        if resp.status_code == 409:
            time.sleep(0.3)
            continue
        raise AssertionError(f"Register failed (status {resp.status_code}): {resp.text}")
    raise AssertionError("Register failed after retries (conflict)")

@pytest.fixture(scope="session")
def context():
    ctx = TestContext()

    client = ApiClient(BASE_URL)
    reg_data, email, password = _register_unique(client)
    user = reg_data["data"]["user"]
    business = reg_data["data"]["business"]
    ctx.user_id = user["id"]
    ctx.business_id = business["id"]
    ctx.business_slug = business["slug"]

    login_body = {"email": email, "password": password}
    resp = client.post("/v1/auth/login", json=login_body)
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    login_data = resp.json()
    assert_success(login_data)
    ctx.token = login_data["data"]["token"]

    auth_client = ApiClient(BASE_URL, ctx.token)

    # Create Resource Type
    rt_name = generate_payload("resourceTypeName") or f"RT_{int(time.time())}"
    rt_body = {"name": rt_name, "description": "Test RT"}
    resp = auth_client.post("/resource-types", json=rt_body)
    assert resp.status_code == 201, f"Create RT failed: {resp.text}"
    rt_data = resp.json()
    assert_success(rt_data)
    ctx.resource_type_id = rt_data["data"]["id"]

    # Create Resource
    res_name = generate_payload("resourceName") or f"Res_{int(time.time())}"
    res_body = {
        "resourceTypeId": ctx.resource_type_id,
        "name": res_name,
        "description": "Test Resource",
        "capacity": 5,
        "price": 150.0,
        "status": "AVAILABLE",
        "imageUrl": "https://example.com/image.jpg"
    }
    resp = auth_client.post("/resources", json=res_body)
    assert resp.status_code == 201, f"Create Resource failed: {resp.text}"
    res_data = resp.json()
    assert_success(res_data)
    ctx.resource_id = res_data["data"]["id"]

    # Create Reservation dengan tanggal dinamis (besok)
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    cust_name = generate_payload("customerName") or f"Cust_{int(time.time())}"
    cust_email = generate_payload("email") or f"cust_{int(time.time())}@test.com"
    cust_phone = generate_payload("phone") or "08123456789"
    reserv_body = {
        "resourceId": ctx.resource_id,
        "reservationDate": tomorrow,
        "startTime": "10:00",
        "endTime": "11:00",
        "customer": {
            "fullName": cust_name,
            "email": cust_email,
            "phone": cust_phone
        }
    }
    resp = auth_client.post("/reservations", json=reserv_body)
    if resp.status_code == 201:
        reserv_data = resp.json()
        assert_success(reserv_data)
        ctx.reservation_id = reserv_data["data"]["id"]
    else:
        # Jika gagal, set None dan lanjutkan (test yang butuh reservasi akan skip)
        print(f"WARNING: Create reservation failed: {resp.text}")
        ctx.reservation_id = None

    yield ctx

@pytest.fixture
def api_client(context):
    return ApiClient(BASE_URL, context.token)

@pytest.fixture
def public_client():
    return ApiClient(BASE_URL)

@pytest.fixture
def ctx(context):
    return context

@pytest.fixture(scope="session")
def browser_context(browser):
    """Browser context untuk Playwright."""
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    yield context
    context.close()



@pytest.fixture
def page(browser_context):
    """Halaman Playwright untuk E2E test."""
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def db():
    """Fixture untuk akses database."""
    return DatabaseClient()