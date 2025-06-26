"""
Flow-ResourceSpace-Slack Stack API

Robust API for seamless asset sharing between Flow, ResourceSpace, and Slack.
"""
from typing import Dict, Any, List
from fastapi import HTTPException
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from .logic.asset_bridge import AssetBridge

log = get_module_logger("flow_resourcespace_slack.api")

# Request/Response Models
class FlowToResourceSpaceRequest(BaseModel):
    flow_asset_id: int
    metadata_overrides: Dict[str, Any] = {}

class ResourceSpaceToSlackRequest(BaseModel):
    resource_id: str
    channel: str
    custom_message: str = None

class CompleteWorkflowRequest(BaseModel):
    flow_asset_id: int
    channel: str
    include_metadata: bool = True

class ProjectSyncRequest(BaseModel):
    project_id: int
    channel: str

class SearchAndShareRequest(BaseModel):
    query: str
    channel: str
    max_results: int = 5

@register_api
class FlowResourceSpaceSlackAPI(HomerAPI):
    """API endpoints for Flow-ResourceSpace-Slack asset sharing workflows."""
    
    def __init__(self):
        super().__init__()
        self._bridge = None
    
    async def _get_bridge(self) -> AssetBridge:
        """Get or create bridge instance."""
        if not self._bridge:
            self._bridge = AssetBridge()
        return self._bridge
    
    async def cleanup(self):
        """Cleanup bridge connections."""
        if self._bridge:
            await self._bridge.close()
            self._bridge = None

    async def get(self, path: str = "/ping") -> Dict[str, Any]:
        """Handle GET requests."""
        if path == "/ping":
            return {"status": "ok", "stack": "flow-resourcespace-slack"}
        
        elif path == "/health":
            bridge = await self._get_bridge()
            try:
                health = await bridge.health_check()
                return health
            except Exception as e:
                log.error(f"Health check failed: {e}")
                raise HTTPException(status_code=503, detail=str(e))
        
        elif path == "/status":
            bridge = await self._get_bridge()
            try:
                health = await bridge.health_check()
                return {
                    "stack": "flow-resourcespace-slack",
                    "description": "Asset sharing bridge between Flow production management, ResourceSpace digital assets, and Slack team communication",
                    "services": health,
                    "available_workflows": [
                        "flow_to_resourcespace",
                        "resourcespace_to_slack",
                        "complete_workflow",
                        "project_sync",
                        "search_and_share"
                    ],
                    "modules": ["flow", "resourcespace", "slack"]
                }
            except Exception as e:
                log.error(f"Status check failed: {e}")
                raise HTTPException(status_code=503, detail=str(e))
        
        else:
            raise HTTPException(status_code=404, detail="Endpoint not found")

    async def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST requests for asset workflows."""
        bridge = await self._get_bridge()
        
        try:
            if path == "/push/flow-to-resourcespace":
                request = FlowToResourceSpaceRequest(**data)
                result = await bridge.flow_to_resourcespace(
                    flow_asset_id=request.flow_asset_id,
                    metadata_overrides=request.metadata_overrides
                )
                return result
            
            elif path == "/share/resourcespace-to-slack":
                request = ResourceSpaceToSlackRequest(**data)
                result = await bridge.resourcespace_to_slack(
                    resource_id=request.resource_id,
                    channel=request.channel,
                    custom_message=request.custom_message
                )
                return result
            
            elif path == "/workflow/complete":
                request = CompleteWorkflowRequest(**data)
                result = await bridge.flow_to_slack_with_resourcespace(
                    flow_asset_id=request.flow_asset_id,
                    channel=request.channel,
                    include_metadata=request.include_metadata
                )
                return result
            
            elif path == "/workflow/sync-project":
                request = ProjectSyncRequest(**data)
                result = await bridge.sync_project_assets(
                    project_id=request.project_id,
                    channel=request.channel
                )
                return result
            
            elif path == "/search/and-share":
                request = SearchAndShareRequest(**data)
                result = await bridge.search_and_share(
                    search_query=request.query,
                    channel=request.channel,
                    max_results=request.max_results
                )
                return result
            
            else:
                raise HTTPException(status_code=404, detail="Workflow not found")
                
        except Exception as e:
            log.error(f"Workflow execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))