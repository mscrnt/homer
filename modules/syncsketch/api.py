from fastapi import HTTPException, UploadFile, File
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from modules.syncsketch.client import get_syncsketch_client
from typing import List, Dict, Any
import os

log = get_module_logger("syncsketch-api")

class UploadRequest(BaseModel):
    project_id: str
    name: str = None

class CreateReviewRequest(BaseModel):
    project_id: str
    name: str
    description: str = ""

@register_api
class SyncSketchAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/syncsketch")

    def register_routes(self):
        # 🩺 Health check route
        @self.router.get("/ping")
        async def ping():
            """Simple health check for SyncSketch service."""
            try:
                has_key = bool(os.getenv("SYNCSKETCH_API_KEY"))
                has_workspace = bool(os.getenv("SYNCSKETCH_WORKSPACE"))
                return {
                    "status": "ok", 
                    "module": "syncsketch",
                    "api_key_configured": has_key,
                    "workspace_configured": has_workspace,
                    "workspace": os.getenv("SYNCSKETCH_WORKSPACE", "not set")
                }
            except Exception as e:
                log.exception("❌ SyncSketch ping failed")
                return {"status": "error", "message": str(e)}

        # 📋 List projects
        @self.router.get("/projects")
        async def list_projects():
            """List available SyncSketch projects."""
            try:
                client = get_syncsketch_client()
                projects = await client.get_projects()
                
                return {
                    "status": "success",
                    "projects": projects,
                    "count": len(projects)
                }
            except Exception as e:
                log.exception("❌ Failed to list SyncSketch projects")
                raise HTTPException(status_code=500, detail=str(e))

        # 📋 List reviews for a project
        @self.router.get("/projects/{project_id}/reviews")
        async def list_reviews(project_id: str):
            """List reviews for a specific project."""
            try:
                client = get_syncsketch_client()
                reviews = await client.get_reviews(project_id)
                
                return {
                    "status": "success",
                    "project_id": project_id,
                    "reviews": reviews,
                    "count": len(reviews)
                }
            except Exception as e:
                log.exception(f"❌ Failed to list reviews for project {project_id}")
                raise HTTPException(status_code=500, detail=str(e))

        # 🎬 Create review
        @self.router.post("/reviews")
        async def create_review(request: CreateReviewRequest):
            """Create a new review in SyncSketch."""
            try:
                client = get_syncsketch_client()
                result = await client.create_review(
                    request.project_id,
                    request.name,
                    request.description
                )
                
                return {
                    "status": "success",
                    "review": result
                }
            except Exception as e:
                log.exception("❌ Failed to create SyncSketch review")
                raise HTTPException(status_code=500, detail=str(e))

        # 📤 Upload media (simplified endpoint)
        @self.router.post("/upload")
        async def upload_media(
            project_id: str,
            name: str = None,
            file: UploadFile = File(...)
        ):
            """Upload media file to SyncSketch."""
            try:
                client = get_syncsketch_client()
                
                # In a real implementation, you'd handle the file upload properly
                # For now, we'll simulate it
                result = await client.upload_media(
                    file.filename,
                    project_id,
                    name or file.filename
                )
                
                return {
                    "status": "success",
                    "upload": result
                }
            except Exception as e:
                log.exception("❌ Failed to upload media to SyncSketch")
                raise HTTPException(status_code=500, detail=str(e))