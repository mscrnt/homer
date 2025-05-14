

from fastapi import APIRouter, HTTPException
from typing import Optional
from homer.utils.logger import get_module_logger
from modules.flow.logic import activity as activity_logic

log = get_module_logger("flow-activity")
router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# 📊 Activity Stream
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/activity/{entity_type}/{entity_id}")
def get_activity_stream(
    entity_type: str,
    entity_id: int,
    min_id: Optional[int] = None,
    max_id: Optional[int] = None,
    limit: Optional[int] = 50,
):
    """Fetch activity stream for an entity."""
    try:
        return activity_logic.get_activity_stream(
            entity_type=entity_type,
            entity_id=entity_id,
            min_id=min_id,
            max_id=max_id,
            limit=limit
        )
    except Exception as e:
        log.exception("❌ Failed to retrieve activity stream")
        raise HTTPException(status_code=500, detail=str(e))

# ─────────────────────────────────────────────────────────────────────────────
# 👤 Follower Management
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/follow")
def follow_entity(user_id: int, entity_type: str, entity_id: int):
    """Follow an entity as a specific user."""
    try:
        return activity_logic.follow_entity(user_id, entity_type, entity_id)
    except Exception as e:
        log.exception("❌ Failed to follow entity")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unfollow")
def unfollow_entity(user_id: int, entity_type: str, entity_id: int):
    """Unfollow an entity as a specific user."""
    try:
        return activity_logic.unfollow_entity(user_id, entity_type, entity_id)
    except Exception as e:
        log.exception("❌ Failed to unfollow entity")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/followers/{entity_type}/{entity_id}")
def get_followers(entity_type: str, entity_id: int):
    """Get all followers of a specific entity."""
    try:
        return activity_logic.get_followers(entity_type, entity_id)
    except Exception as e:
        log.exception("❌ Failed to retrieve followers")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/following/{user_id}")
def get_following(user_id: int, project_id: Optional[int] = None, entity_type: Optional[str] = None):
    """Get all entities a user is following."""
    try:
        return activity_logic.get_following(user_id, project_id, entity_type)
    except Exception as e:
        log.exception("❌ Failed to retrieve followed entities")
        raise HTTPException(status_code=500, detail=str(e))
