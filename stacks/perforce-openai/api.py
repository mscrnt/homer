"""
Perforce-OpenAI Stack API
"""
from typing import Dict, Any, List
from fastapi import HTTPException
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from .logic.ai_code_analysis import AICodeAnalysis

log = get_module_logger("perforce_openai.api")

# Request/Response Models
class AnalyzeChangelistRequest(BaseModel):
    changelist_id: str
    include_files: bool = False

class GenerateReleaseNotesRequest(BaseModel):
    changelists: List[str]
    target_audience: str = "technical"

class CodeReviewRequest(BaseModel):
    changelist_id: str
    focus_areas: List[str] = []

class SmartCommitRequest(BaseModel):
    files: List[str]
    diff_summary: str = ""

@register_api
class PerforceOpenAIAPI(HomerAPI):
    """API endpoints for Perforce-OpenAI AI-powered code analysis."""
    
    def __init__(self):
        super().__init__()
        self._analyzer = None
    
    async def _get_analyzer(self) -> AICodeAnalysis:
        """Get or create analyzer instance."""
        if not self._analyzer:
            self._analyzer = AICodeAnalysis()
        return self._analyzer

    async def get(self, path: str = "/ping") -> Dict[str, Any]:
        """Handle GET requests."""
        if path == "/ping":
            return {"status": "ok", "stack": "perforce-openai"}
        
        elif path == "/health":
            analyzer = await self._get_analyzer()
            try:
                health = await analyzer.health_check()
                return health
            except Exception as e:
                log.error(f"Health check failed: {e}")
                raise HTTPException(status_code=503, detail=str(e))
        
        elif path == "/status":
            analyzer = await self._get_analyzer()
            try:
                health = await analyzer.health_check()
                return {
                    "stack": "perforce-openai",
                    "description": "AI-powered code analysis combining Perforce version control with OpenAI insights",
                    "services": health,
                    "available_features": [
                        "changelist_analysis",
                        "release_notes_generation",
                        "code_review_assistant",
                        "smart_commit_messages"
                    ]
                }
            except Exception as e:
                log.error(f"Status check failed: {e}")
                raise HTTPException(status_code=503, detail=str(e))
        
        else:
            raise HTTPException(status_code=404, detail="Endpoint not found")

    async def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST requests for AI analysis workflows."""
        analyzer = await self._get_analyzer()
        
        try:
            if path == "/analyze/changelist":
                request = AnalyzeChangelistRequest(**data)
                result = await analyzer.analyze_changelist(
                    changelist_id=request.changelist_id,
                    include_files=request.include_files
                )
                return result
            
            elif path == "/generate/release-notes":
                request = GenerateReleaseNotesRequest(**data)
                result = await analyzer.generate_release_notes(
                    changelists=request.changelists,
                    target_audience=request.target_audience
                )
                return result
            
            elif path == "/review/code":
                request = CodeReviewRequest(**data)
                result = await analyzer.code_review_assistant(
                    changelist_id=request.changelist_id,
                    focus_areas=request.focus_areas
                )
                return result
            
            elif path == "/generate/commit-message":
                request = SmartCommitRequest(**data)
                result = await analyzer.smart_commit_message(
                    files=request.files,
                    diff_summary=request.diff_summary
                )
                return result
            
            else:
                raise HTTPException(status_code=404, detail="Analysis workflow not found")
                
        except Exception as e:
            log.error(f"AI analysis failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))