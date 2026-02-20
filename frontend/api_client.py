import os
import requests


class APIError(Exception):
    def __init__(self, status_code: int, detail):
        super().__init__(f"APIError {status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail


class APIClient:
    def __init__(self, base_url: str | None = None):
        base = base_url or os.getenv(
            "PROPERTY_PORTAL_API_URL", "http://127.0.0.1:8000")
        self.base_url = base.rstrip("/")

    def _request(self, method: str, path: str, token: str | None = None, **kwargs):
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {}) or {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        res = requests.request(
            method, url, headers=headers, timeout=20, **kwargs)

        if res.status_code >= 400:
            try:
                detail = res.json()
            except Exception:
                detail = res.text
            raise APIError(res.status_code, detail)

        if res.status_code == 204:
            return None

        # FastAPI usually returns JSON
        return res.json()

    # ---------- Auth ----------
    def register(self, email: str, password: str, role: str):
        return self._request(
            "POST",
            "/auth/register",
            json={"email": email, "password": password, "role": role},
        )

    def login(self, email: str, password: str):
        return self._request(
            "POST",
            "/auth/login",
            json={"email": email, "password": password},
        )

    # ---------- Properties ----------
    def list_properties(self, token: str):
        return self._request("GET", "/properties/", token=token)

    def my_properties(self, token: str):
        return self._request("GET", "/properties/my-properties", token=token)

    def search_properties(self, location: str | None = None, min_price: float | None = None, max_price: float | None = None):
        params = {}
        if location:
            params["location"] = location
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price

        return self._request("GET", "/properties/search", params=params)

    def create_property(self, token: str, title: str, location: str, price: float, status: str = "available"):
        return self._request(
            "POST",
            "/properties/",
            token=token,
            json={"title": title, "location": location,
                  "price": price, "status": status},
        )

    def update_property(self, token: str, property_id: int, title: str, location: str, price: float, status: str):
        return self._request(
            "PUT",
            f"/properties/{property_id}",
            token=token,
            json={"title": title, "location": location,
                  "price": price, "status": status},
        )

    def delete_property(self, token: str, property_id: int):
        return self._request("DELETE", f"/properties/{property_id}", token=token)

    def stats(self):
        return self._request("GET", "/properties/stats")
