
import os
from typing import Optional
from pynetbox.core.api import Api  
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox-client")

_client: Optional[Api] = None  


def get_netbox_client() -> Api:
    """Return a cached NetBox API client, initializing if needed."""
    global _client
    if _client is None:
        try:
            url = os.environ["NETBOX_URL"]
            token = os.environ["NETBOX_TOKEN"]
            _client = Api(url, token=token)
            log.info("✅ NetBox client initialized")
        except KeyError as e:
            missing = e.args[0]
            log.error(f"❌ Missing required environment variable: {missing}")
            raise
        except Exception as e:
            log.exception("❌ Failed to initialize NetBox client")
            raise
    return _client
