# api.py

from fastapi import HTTPException
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger

# 🧩 Import route files (these should define FastAPI routers)
from modules.example.routes import (
    connection,
    items,
    actions,
    metadata,
)

from modules.example.routes.connection import get_server_info

log = get_module_logger("example-api")

@register_api
class ExampleAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/example")

    def register_routes(self):
        # 🩺 Health check route
        @self.router.get("/ping")
        async def ping():
            """Simple health check for Example service."""
            try:
                info = get_server_info()
                return {"status": "ok", "version": info.get("version", "unknown")}
            except HTTPException as e:
                return {"status": "error", "message": e.detail}
            except Exception as e:
                log.exception("❌ Example ping failed")
                return {"status": "error", "message": str(e)}

        # 📦 Register all modular routers
        self.router.include_router(connection.router, prefix="/connection")
        self.router.include_router(items.router, prefix="/items")
        self.router.include_router(actions.router, prefix="/actions")
        self.router.include_router(metadata.router, prefix="/metadata")
