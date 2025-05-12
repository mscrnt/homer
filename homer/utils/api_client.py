# base/utils/api.py

import os
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from homer.utils.logger import get_module_logger, log_with_caller

log = get_module_logger()

class APIError(Exception):
    pass

class BaseAPIClient:
    def __init__(self, base_url=None, headers=None, token=None, timeout=10, verify=True):
        self.base_url = base_url or ""
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = verify  # 🔒 Secure by default

        if not verify:
            log.warning("⚠️ SSL verification disabled — using untrusted mode.")
            disable_warnings(InsecureRequestWarning)

        # Retry strategy
        retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update(headers or {})
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

        log.debug(f"🌐 API Client initialized: {self.base_url} (verify={verify})")

    def _url(self, path):
        return urljoin(self.base_url, path)

    def get(self, path, params=None, **kwargs):
        url = self._url(path)
        log_with_caller("debug", f"GET {url} with params={params}")
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
            return self._handle_response(resp)
        except requests.RequestException as e:
            raise APIError(f"GET {url} failed: {e}")

    def post(self, path, json=None, data=None, **kwargs):
        url = self._url(path)
        log_with_caller("debug", f"POST {url} with body={json or data}")
        try:
            resp = self.session.post(url, json=json, data=data, timeout=self.timeout, **kwargs)
            return self._handle_response(resp)
        except requests.RequestException as e:
            raise APIError(f"POST {url} failed: {e}")

    def put(self, path, json=None, **kwargs):
        url = self._url(path)
        log_with_caller("debug", f"PUT {url} with body={json}")
        try:
            resp = self.session.put(url, json=json, timeout=self.timeout, **kwargs)
            return self._handle_response(resp)
        except requests.RequestException as e:
            raise APIError(f"PUT {url} failed: {e}")

    def delete(self, path, **kwargs):
        url = self._url(path)
        log_with_caller("debug", f"DELETE {url}")
        try:
            resp = self.session.delete(url, timeout=self.timeout, **kwargs)
            return self._handle_response(resp)
        except requests.RequestException as e:
            raise APIError(f"DELETE {url} failed: {e}")

    def _handle_response(self, response):
        log.debug(f"📬 {response.status_code} {response.reason} — {response.url}")
        try:
            response.raise_for_status()
            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()
            return response.text
        except requests.HTTPError as e:
            log.error(f"❌ API Error: {response.status_code} — {response.text}")
            raise APIError(str(e))
