

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from homer.utils.logger import get_module_logger
from modules.flow.logic import versions as version_logic

log = get_module_logger("flow-versions")
router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# 🧪 Request models
# ─────────────────────────────────────────────────────────────────────────────

class VersionCreateRequest(BaseModel):
    project_id: int
    code: str
    description: Optional[str] = None
    sg_path_to_frames: Optional[str] = None
    sg_status_list: Optional[str] = None
    shot_id: Optional[int] = None
    task_id: Optional[int] = None
    user_id: Optional[int] = None

# ─────────────────────────────────────────────────────────────────────────────
# 📦 Routes
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/")
def create_version(payload: VersionCreateRequest):
    """Create a new Version linked to Shot, Task, and/or User."""
    try:
        return version_logic.create_version(
            project_id=payload.project_id,
            code=payload.code,
            description=payload.description,
            sg_path_to_frames=payload.sg_path_to_frames,
            sg_status_list=payload.sg_status_list,
            shot_id=payload.shot_id,
            task_id=payload.task_id,
            user_id=payload.user_id
        )
    except Exception as e:
        log.exception("❌ Failed to create version")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{version_id}/thumbnail")
def upload_thumbnail(version_id: int, file: UploadFile = File(...)):
    """Upload a thumbnail image to an existing Version."""
    try:
        return version_logic.upload_version_thumbnail(version_id, file)
    except Exception as e:
        log.exception("❌ Failed to upload thumbnail")
        raise HTTPException(status_code=500, detail=str(e))
