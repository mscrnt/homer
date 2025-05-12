# modules/resourcespace/api.py

from fastapi import Request
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from .client import call_api
from typing import Optional

log = get_module_logger("resourcespace-api")

@register_api
class ResourceSpaceAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/resourcespace")

    def register_routes(self):
        @self.router.get("/ping")
        async def ping():
            """
            Perform a test call to verify ResourceSpace connectivity.
            """
            try:
                result = call_api("get_system_status")
                return {
                    "status": "ok",
                    "result": result
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e)
                }

        @self.router.post("/raw")
        async def passthrough(request: Request):
            """
            Generic passthrough for calling arbitrary ResourceSpace functions.
            Expects JSON like: { "function": "do_search", "params": { "search": "cat" } }
            """
            body = await request.json()
            function = body.get("function")
            params = body.get("params", {})

            if not function:
                return {"error": "Missing 'function' in request body"}

            try:
                result = call_api(function, params)
                return {
                    "function": function,
                    "result": result
                }
            except Exception as e:
                log.exception("❌ Passthrough failed")
                return {
                    "error": str(e)
                }
