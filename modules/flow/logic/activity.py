

from typing import Optional
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.activity.logic")


def get_activity_stream(entity_type: str, entity_id: int, min_id: Optional[int] = None,
                        max_id: Optional[int] = None, limit: Optional[int] = 50) -> dict:
    sg = get_sg_client()
    return sg.activity_stream_read(
        entity_type=entity_type,
        entity_id=entity_id,
        min_id=min_id,
        max_id=max_id,
        limit=limit
    )


def follow_entity(user_id: int, entity_type: str, entity_id: int) -> dict:
    sg = get_sg_client()
    return sg.follow(
        {"type": "HumanUser", "id": user_id},
        {"type": entity_type, "id": entity_id}
    )


def unfollow_entity(user_id: int, entity_type: str, entity_id: int) -> dict:
    sg = get_sg_client()
    return sg.unfollow(
        {"type": "HumanUser", "id": user_id},
        {"type": entity_type, "id": entity_id}
    )


def get_followers(entity_type: str, entity_id: int) -> list:
    sg = get_sg_client()
    return sg.followers({"type": entity_type, "id": entity_id})


def get_following(user_id: int, project_id: Optional[int] = None,
                  entity_type: Optional[str] = None) -> list:
    sg = get_sg_client()
    user = {"type": "HumanUser", "id": user_id}
    project = {"type": "Project", "id": project_id} if project_id else None
    return sg.following(user, project=project, entity_type=entity_type)
