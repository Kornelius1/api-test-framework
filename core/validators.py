from typing import Any, Dict, List

def assert_status(response, expected_status: int):
    """Cek status code, jika gagal tampilkan AI explanation."""
    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}. "
        f"Response: {response.text[:200]}"
    )

def assert_response_has_fields(response_json: Dict[str, Any], fields: List[str]):
    """Pastikan response memiliki field yang diberikan."""
    for field in fields:
        assert field in response_json, f"Missing field '{field}' in response"

def assert_response_data_has_fields(response_json: Dict[str, Any], fields: List[str]):
    """Pastikan response.data memiliki field yang diberikan."""
    data = response_json.get("data")
    assert data is not None, "Response data is None"
    for field in fields:
        assert field in data, f"Missing field '{field}' in response.data"

def assert_success(response_json: Dict[str, Any]):
    """Cek success = True (jika ada)."""
    if "success" in response_json:
        assert response_json["success"] is True, "Response success is False"