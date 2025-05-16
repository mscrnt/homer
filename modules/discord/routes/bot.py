# routes/actions.py

from fastapi import APIRouter, HTTPException
from homer.utils.logger import get_module_logger
from modules.example.logic import actions as action_logic

log = get_module_logger("example-actions")
router = APIRouter()

@router.get("/trigger")
async def handle_example_action(action: str):
    """
    Handle incoming requests to perform example actions.
    This could support triggering jobs, workflows, or downstream services.
    """
    try:
        return action_logic.handle_action_trigger(action)
    except ValueError as ve:
        log.warning(f"⚠️ Invalid action request: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        log.exception("❌ Failed to process action request")
        raise HTTPException(status_code=500, detail=str(e))
