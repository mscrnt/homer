from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger

from modules.flow.routes import shots, playlists, versions, tasks, actions, connection, schema, crud, files, activity, tools
from modules.flow.routes.connection import get_server_info 
from fastapi import HTTPException

log = get_module_logger("flow-api")

@register_api
class FlowAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/flow")

    def register_routes(self):
        @self.router.get("/ping")
        async def ping():
            """Quick ShotGrid health check using sg.info()."""
            try:
                info = get_server_info()
                return {"status": "ok", "version": info.get("version")}
            except HTTPException as e:
                return {"status": "error", "message": e.detail}
            except Exception as e:
                log.exception("❌ Unexpected ShotGrid ping failure")
                return {"status": "error", "message": str(e)}

        self.router.include_router(shots.router, prefix="/shots")
        self.router.include_router(playlists.router, prefix="/playlists")
        self.router.include_router(versions.router, prefix="/versions")
        self.router.include_router(tasks.router, prefix="/tasks")
        self.router.include_router(actions.router, prefix="/actions")
        self.router.include_router(connection.router, prefix="/connection")
        self.router.include_router(schema.router, prefix="/schema")
        self.router.include_router(crud.router, prefix="/crud")
        self.router.include_router(files.router, prefix="/files")
        self.router.include_router(activity.router, prefix="/activity")
        self.router.include_router(tools.router, prefix="/tools")
