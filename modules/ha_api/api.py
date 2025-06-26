"""
Home Assistant API routes for HOMER
"""
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_logger
from .client import HAClient

logger = get_logger(__name__)


@register_api
class HomeAssistantAPI(HomerAPI):
    """Home Assistant API endpoints"""
    
    def __init__(self):
        super().__init__()
        self.client = HAClient()
    
    def get(self, path: str = "/ping"):
        """Health check endpoint"""
        if path == "/ping":
            return {"status": "ok", "module": "ha_api"}
        elif path == "/health":
            return self.client.health_check()
        else:
            return {"error": "Not found"}, 404