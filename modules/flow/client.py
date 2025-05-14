

import os
from shotgun_api3 import Shotgun
from homer.utils.logger import get_module_logger

log = get_module_logger("flow-client")

_client: Shotgun | None = None

def get_sg_client() -> Shotgun:
    """Return a cached ShotGrid API client, initializing if needed."""
    global _client
    if _client is None:
        try:
            _client = Shotgun(
                os.environ["SG_SITE"],
                os.environ["SG_SCRIPT_NAME"],
                os.environ["SG_API_KEY"]
            )
            log.info("✅ ShotGrid client initialized")
        except Exception as e:
            log.exception("❌ Failed to initialize ShotGrid client")
            raise
    return _client
