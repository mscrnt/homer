

from fastapi import APIRouter, HTTPException
from homer.utils.logger import get_module_logger
from modules.flow.logic import tasks as task_logic

log = get_module_logger("flow-tasks")
router = APIRouter()

@router.get("/by-shot/{shot_id}")
def get_tasks_for_shot(shot_id: int):
    """Return all Tasks linked to a specific Shot."""
    try:
        return task_logic.get_tasks_for_shot(shot_id)
    except Exception as e:
        log.exception("❌ Failed to retrieve tasks for shot")
        raise HTTPException(status_code=500, detail=str(e))
