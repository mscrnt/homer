from fastapi import HTTPException, Query
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from modules.perforce.client import get_perforce_client
from typing import List, Dict, Any, Optional
import os

log = get_module_logger("perforce-api")

class ChangelistResponse(BaseModel):
    id: str
    user: str
    date: str
    description: str
    files: List[Dict[str, str]]

class ChangelistSummary(BaseModel):
    id: str
    user: str
    date: str
    description: str

class StreamInfo(BaseModel):
    name: str
    type: str
    parent: Optional[str]
    description: str

class SyncRequest(BaseModel):
    filespec: str = "..."

@register_api
class PerforceAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/perforce")

    def register_routes(self):
        # 🩺 Health check route
        @self.router.get("/ping")
        async def ping():
            """Simple health check for Perforce service."""
            try:
                has_port = bool(os.getenv("P4PORT"))
                has_user = bool(os.getenv("P4USER"))
                return {
                    "status": "ok", 
                    "module": "perforce",
                    "p4port_configured": has_port,
                    "p4user_configured": has_user,
                    "p4client": os.getenv("P4CLIENT", "not set")
                }
            except Exception as e:
                log.exception("❌ Perforce ping failed")
                return {"status": "error", "message": str(e)}

        # 📋 Get changelist details
        @self.router.get("/changelist/{changelist_id}", response_model=ChangelistResponse)
        async def get_changelist(changelist_id: str):
            """Get details of a specific changelist."""
            try:
                client = get_perforce_client()
                changelist = await client.get_changelist(changelist_id)
                
                return ChangelistResponse(
                    id=changelist["id"],
                    user=changelist["user"],
                    date=changelist["date"],
                    description=changelist["description"],
                    files=changelist["files"]
                )
            except Exception as e:
                log.exception(f"❌ Failed to get changelist {changelist_id}")
                raise HTTPException(status_code=500, detail=str(e))

        # 📋 List changelists
        @self.router.get("/changelists", response_model=List[ChangelistSummary])
        async def list_changelists(
            user: Optional[str] = Query(None, description="Filter by user"),
            max_results: int = Query(20, description="Maximum number of results")
        ):
            """List recent changelists."""
            try:
                client = get_perforce_client()
                changelists = await client.list_changelists(user, max_results)
                
                return [
                    ChangelistSummary(
                        id=cl["id"],
                        user=cl["user"],
                        date=cl["date"],
                        description=cl["description"]
                    )
                    for cl in changelists
                ]
            except Exception as e:
                log.exception("❌ Failed to list changelists")
                raise HTTPException(status_code=500, detail=str(e))

        # 🌊 List streams
        @self.router.get("/streams", response_model=List[StreamInfo])
        async def list_streams():
            """List available streams."""
            try:
                client = get_perforce_client()
                streams = await client.get_streams()
                
                return [
                    StreamInfo(
                        name=stream["name"],
                        type=stream["type"],
                        parent=stream["parent"],
                        description=stream["description"]
                    )
                    for stream in streams
                ]
            except Exception as e:
                log.exception("❌ Failed to list streams")
                raise HTTPException(status_code=500, detail=str(e))

        # 🔄 Sync files
        @self.router.post("/sync")
        async def sync_files(request: SyncRequest):
            """Sync files from the depot."""
            try:
                client = get_perforce_client()
                result = await client.sync_files(request.filespec)
                
                return {
                    "status": "success",
                    "filespec": request.filespec,
                    "result": result
                }
            except Exception as e:
                log.exception(f"❌ Failed to sync files: {request.filespec}")
                raise HTTPException(status_code=500, detail=str(e))

        # 🏢 Workspace info
        @self.router.get("/info")
        async def get_workspace_info():
            """Get information about the current workspace."""
            try:
                client = get_perforce_client()
                info = await client.get_workspace_info()
                
                return {
                    "status": "success",
                    "workspace_info": info
                }
            except Exception as e:
                log.exception("❌ Failed to get workspace info")
                raise HTTPException(status_code=500, detail=str(e))

        # 🔍 Search changelists by keyword
        @self.router.get("/search")
        async def search_changelists(
            query: str = Query(..., description="Search query"),
            max_results: int = Query(10, description="Maximum number of results")
        ):
            """Search changelists by description keyword."""
            try:
                client = get_perforce_client()
                changelists = await client.list_changelists(max_results=max_results * 2)
                
                # Simple keyword search in descriptions
                query_lower = query.lower()
                filtered = [
                    cl for cl in changelists 
                    if query_lower in cl["description"].lower()
                ][:max_results]
                
                return {
                    "status": "success",
                    "query": query,
                    "results": filtered,
                    "total_found": len(filtered)
                }
            except Exception as e:
                log.exception(f"❌ Failed to search changelists: {query}")
                raise HTTPException(status_code=500, detail=str(e))