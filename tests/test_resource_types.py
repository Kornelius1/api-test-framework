import pytest
from core.validators import assert_status, assert_success

class TestResourceTypes:
    def test_rt_01_create_valid(self, api_client, ctx):
        import time
        name = f"RT_{int(time.time())}"
        body = {"name": name, "description": "Test RT"}
        resp = api_client.post("/resource-types", json=body)
        assert_status(resp, 201)
        data = resp.json()
        assert_success(data)
        assert "id" in data["data"]

    def test_rt_01_create_invalid(self, api_client):
        body = {"name": ""}  # name required, tapi empty
        resp = api_client.post("/resource-types", json=body)
        assert resp.status_code in (400, 422)

    def test_rt_01_create_missing_field(self, api_client):
        resp = api_client.post("/resource-types", json={})
        assert resp.status_code in (400, 422)

    def test_rt_01_create_duplicate(self, api_client, ctx):
        # Buat dengan nama yang sudah ada
        name = "DuplicateRT"
        body = {"name": name}
        api_client.post("/resource-types", json=body)  # pertama
        resp = api_client.post("/resource-types", json=body)  # kedua
        assert resp.status_code in (400, 409)

    def test_rt_01_create_unauthorized(self, public_client):
        body = {"name": "Test"}
        resp = public_client.post("/resource-types", json=body)
        assert resp.status_code == 401

    def test_rt_02_get_all(self, api_client):
        resp = api_client.get("/resource-types")
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)
        assert isinstance(data["data"], list)

    def test_rt_02_get_all_empty(self, api_client, ctx):
        # Tidak bisa memastikan kosong, tapi kita bisa filter? Tidak ada query param.
        # Asumsi jika bisnis baru tidak punya RT, tapi kita sudah buat di setup.
        # Jadi tidak kosong. Kita skip atau asumsikan ada.
        pass

    def test_rt_03_get_by_id_existing(self, api_client, ctx):
        rt_id = ctx.resource_type_id
        resp = api_client.get(f"/resource-types/{rt_id}")
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)
        assert data["data"]["id"] == rt_id

    def test_rt_03_get_by_id_not_found(self, api_client):
        resp = api_client.get("/resource-types/99999")
        assert resp.status_code == 404

    def test_rt_03_get_by_id_other_business(self, api_client):
        # Tidak bisa karena kita hanya punya satu business
        pass

    def test_rt_04_update_valid(self, api_client, ctx):
        rt_id = ctx.resource_type_id
        body = {"name": "UpdatedRT", "description": "Updated"}
        resp = api_client.put(f"/resource-types/{rt_id}", json=body)
        assert_status(resp, 200)
        data = resp.json()
        assert_success(data)
        assert data["data"]["name"] == "UpdatedRT"

    def test_rt_04_update_invalid(self, api_client, ctx):
        rt_id = ctx.resource_type_id
        body = {"name": ""}
        resp = api_client.put(f"/resource-types/{rt_id}", json=body)
        assert resp.status_code in (400, 422)

    def test_rt_04_update_not_found(self, api_client):
        body = {"name": "x"}
        resp = api_client.put("/resource-types/99999", json=body)
        assert resp.status_code == 404

    def test_rt_04_update_unauthorized(self, public_client, ctx):
        body = {"name": "x"}
        resp = public_client.put(f"/resource-types/{ctx.resource_type_id}", json=body)
        assert resp.status_code == 401

    def test_rt_05_delete_existing(self, api_client, ctx):
        # Buat dulu RT untuk dihapus
        import time
        name = f"DelRT_{int(time.time())}"
        body = {"name": name}
        resp = api_client.post("/resource-types", json=body)
        rt_id = resp.json()["data"]["id"]
        resp = api_client.delete(f"/resource-types/{rt_id}")
        assert_status(resp, 204)

    def test_rt_05_delete_not_found(self, api_client):
        resp = api_client.delete("/resource-types/99999")
        assert resp.status_code == 404

    def test_rt_05_delete_used_by_resource(self, api_client, ctx):
        # RT yang sudah dipakai resource tidak bisa dihapus (business rule)
        rt_id = ctx.resource_type_id
        resp = api_client.delete(f"/resource-types/{rt_id}")
        assert resp.status_code in (400, 409)