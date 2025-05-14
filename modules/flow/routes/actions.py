

from fastapi import APIRouter, HTTPException
from homer.utils.logger import get_module_logger
from modules.flow.logic import actions as action_logic

log = get_module_logger("flow-actions")
router = APIRouter()

@router.get("/ami")
async def handle_action_menu(url: str):
    """
    Handle AMI-triggered HTTP calls (e.g. custom protocol).
    Supports action dispatching like 'package4client'.
    """
    try:
        return action_logic.handle_action_menu(url)
    except ValueError as ve:
        log.warning(f"⚠️ Invalid AMI request: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        log.exception("❌ Failed to handle AMI request")
        raise HTTPException(status_code=500, detail=str(e))
