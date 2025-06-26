"""
Slack-SyncSketch Stack API
"""
from typing import Dict, Any, List
from fastapi import HTTPException
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from .logic.creative_workflow import CreativeWorkflowAutomation

log = get_module_logger("slack_syncsketch.api")

# Request/Response Models
class UploadNotifyRequest(BaseModel):
    media_path: str
    project_id: int
    channel: str = "#creative"
    custom_message: str = None

class CreateReviewRequest(BaseModel):
    project_id: int
    review_name: str
    description: str = ""
    channel: str = "#creative"

class DailySummaryRequest(BaseModel):
    project_ids: List[int]
    channel: str = "#daily-updates"

class ReviewCompleteRequest(BaseModel):
    project_id: int
    review_id: int
    channel: str = "#creative"

@register_api
class SlackSyncSketchAPI(HomerAPI):
    """API endpoints for Slack-SyncSketch creative workflow automation."""
    
    def __init__(self):
        super().__init__()
        self._workflow = None
    
    async def _get_workflow(self) -> CreativeWorkflowAutomation:
        """Get or create workflow instance."""
        if not self._workflow:
            self._workflow = CreativeWorkflowAutomation()
        return self._workflow
    
    async def cleanup(self):
        """Cleanup workflow connections."""
        if self._workflow:
            await self._workflow.close()
            self._workflow = None

    async def get(self, path: str = "/ping") -> Dict[str, Any]:
        """Handle GET requests."""
        if path == "/ping":
            return {"status": "ok", "stack": "slack-syncsketch"}
        
        elif path == "/health":
            workflow = await self._get_workflow()
            try:
                health = await workflow.health_check()
                return health
            except Exception as e:
                log.error(f"Health check failed: {e}")
                raise HTTPException(status_code=503, detail=str(e))
        
        elif path == "/status":
            workflow = await self._get_workflow()
            try:
                health = await workflow.health_check()
                return {
                    "stack": "slack-syncsketch",
                    "description": "Creative workflow automation combining Slack notifications with SyncSketch operations",
                    "services": health,
                    "available_workflows": [
                        "upload_notify",
                        "create_review", 
                        "daily_summary",
                        "review_completion"
                    ]
                }
            except Exception as e:
                log.error(f"Status check failed: {e}")
                raise HTTPException(status_code=503, detail=str(e))
        
        else:
            raise HTTPException(status_code=404, detail="Endpoint not found")

    async def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST requests for workflow automation."""
        workflow = await self._get_workflow()
        
        try:
            if path == "/upload-notify":
                request = UploadNotifyRequest(**data)
                result = await workflow.notify_new_upload(
                    project_id=request.project_id,
                    media_path=request.media_path,
                    channel=request.channel,
                    custom_message=request.custom_message
                )
                return result
            
            elif path == "/create-review":
                request = CreateReviewRequest(**data)
                result = await workflow.notify_review_created(
                    project_id=request.project_id,
                    review_name=request.review_name,
                    description=request.description,
                    channel=request.channel
                )
                return result
            
            elif path == "/daily-summary":
                request = DailySummaryRequest(**data)
                result = await workflow.daily_project_summary(
                    project_ids=request.project_ids,
                    channel=request.channel
                )
                return result
            
            elif path == "/review-complete":
                request = ReviewCompleteRequest(**data)
                result = await workflow.review_completion_workflow(
                    project_id=request.project_id,
                    review_id=request.review_id,
                    channel=request.channel
                )
                return result
            
            else:
                raise HTTPException(status_code=404, detail="Workflow not found")
                
        except Exception as e:
            log.error(f"Workflow execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))