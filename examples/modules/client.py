# client.py

import os
from homer.utils.logger import get_module_logger

log = get_module_logger("example-client")

_client = None  # Cache for the external API client


def get_example_client():
    """Return a cached API client, initializing it if needed."""
    global _client
    if _client is None:
        try:
            # Replace with your actual client init logic
            # For example: _client = SomeApiClient(api_url, api_key)
            _client = {
                "api_url": os.environ["EXAMPLE_API_URL"],
                "api_key": os.environ["EXAMPLE_API_KEY"],
                "mode": os.getenv("EXAMPLE_MODE", "demo")
            }
            log.info("✅ Example API client initialized")
        except Exception as e:
            log.exception("❌ Failed to initialize Example API client")
            raise
    return _client
