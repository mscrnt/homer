# modules/resourcespace/client.py

import hashlib
import os
import requests
from urllib.parse import urlencode, quote
from typing import Optional, Union
from pathlib import Path
import mimetypes
from homer.utils.logger import get_module_logger

log = get_module_logger("resourcespace-client")

class ResourceSpaceClient:
    def __init__(self):
        self.username = os.getenv("RS_API_USER")
        self.private_key = os.getenv("RS_API_KEY")
        self.base_url = os.getenv("RS_API_URL", "").rstrip("/")

        if not self.username or not self.private_key or not self.base_url:
            raise RuntimeError("❌ Missing RS_API_URL, RS_API_USER, or RS_API_KEY")

        log.debug(f"🔐 ResourceSpaceClient initialized for {self.username} @ {self.base_url}")

    def _sign(self, query: str) -> str:
        return hashlib.sha256((self.private_key + query).encode()).hexdigest()

    def _make_url(self, query: str) -> str:
        return f"{self.base_url}/api/?{query}&sign={self._sign(query)}"

    def call(self, function: str, params: dict = None, method: str = "POST") -> Union[dict, list]:
        """Make a signed ResourceSpace API request."""
        params = params or {}
        params = {"user": self.username, "function": function, **params}
        query_str = urlencode(params)
        url = self._make_url(query_str)

        try:
            log.debug(f"🌐 RS API [{method}] {url}")
            response = requests.post(url, timeout=15) if method.upper() == "POST" else requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log.exception(f"❌ RS API call failed: {function}")
            raise

    def call_multipart(self, function: str, params: dict, file_path: str) -> dict:
        """POST file using multipart/form-data (file is excluded from the signature)."""
        if not Path(file_path).exists():
            raise FileNotFoundError(f"🚫 File not found: {file_path}")

        full_params = {"user": self.username, "function": function, **params}
        query_str = urlencode(full_params)
        sign = self._sign(query_str)

        post_payload = {
            "query": query_str,
            "sign": sign,
            "user": self.username
        }

        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        files = {
            "file": (Path(file_path).name, open(file_path, "rb"), mime_type)
        }

        try:
            response = requests.post(f"{self.base_url}/api/", data=post_payload, files=files, timeout=30)
            response.raise_for_status()
            try:
                return response.json()
            except Exception:
                return {"status": "ok", "message": response.text}
        except Exception as e:
            log.exception("❌ Multipart upload failed")
            raise

# ──────────────────────────────────────────────────────────────────────────────
# 🔄 Global singleton client and wrappers for API use
# ──────────────────────────────────────────────────────────────────────────────

# 🔄 Lazy-loaded global client
_client: Optional["ResourceSpaceClient"] = None  # Forward reference

def get_client() -> "ResourceSpaceClient":
    """Lazily initialize and return the global ResourceSpaceClient."""
    global _client
    if _client is None:
        from modules.resourcespace.client import ResourceSpaceClient  # Delayed import
        _client = ResourceSpaceClient()
    return _client

def call_api(function: str, params: dict = None, method: str = "POST"):
    return get_client().call(function, params, method)

def call_api_multipart(function: str, params: dict, file_path: str):
    return get_client().call_multipart(function, params, file_path)