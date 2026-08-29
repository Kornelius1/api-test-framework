import requests
from typing import Optional, Dict, Any

class ApiClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        headers.update(self._headers())
        return self.session.request(method, url, headers=headers, **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)