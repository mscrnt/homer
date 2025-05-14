

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from modules.flow.logic import shots as shots_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("flow-shots")
router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# 🧪 Request models
# ─────────────────────────────────────────────────────────────────────────────

class ShotCreateRequest(BaseModel):
    project_id: int
    code: str
    description: Optional[str] = None
    sg_status_list: Optional[str] = None
    task_template_id: Optional[int] = None


class ShotUpdateRequest(BaseModel):
    description: Optional[str] = None
    sg_status_list: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# 📦 Routes
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/by-project-name")
def get_shots_by_project_name(project: str):
    """Return all Shots for a given project name."""
    try:
        return shots_logic.get_shots_by_project_name(project)
    except Exception as e:
        log.exception("❌ Failed to retrieve shots")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{shot_id}")
def get_shot_by_id(shot_id: int):
    """Find a Shot by its ID."""
    try:
        return shots_logic.get_shot_by_id(shot_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Shot not found")
    except Exception as e:
        log.exception("❌ Failed to retrieve shot by ID")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_shot(payload: ShotCreateRequest):
    """Create a new Shot, with optional task template."""
    try:
        return shots_logic.create_shot(
            project_id=payload.project_id,
            code=payload.code,
            description=payload.description,
            sg_status_list=payload.sg_status_list,
            task_template_id=payload.task_template_id
        )
    except Exception as e:
        log.exception("❌ Failed to create shot")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{shot_id}")
def update_shot(shot_id: int, payload: ShotUpdateRequest):
    """Update fields on a Shot."""
    try:
        updates = payload.dict(exclude_none=True)
        return shots_logic.update_shot(shot_id, updates)
    except Exception as e:
        log.exception("❌ Failed to update shot")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{shot_id}")
def delete_shot(shot_id: int):
    """Delete a Shot by ID."""
    try:
        success = shots_logic.delete_shot(shot_id)
        return {"deleted": success}
    except Exception as e:
        log.exception("❌ Failed to delete shot")
        raise HTTPException(status_code=500, detail=str(e))
