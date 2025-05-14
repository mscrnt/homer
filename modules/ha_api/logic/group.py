from typing import Dict, Optional
from homeassistant_api import Group, Entity
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.group")

# ──────────────────────────────────────────────────────────────────────────────
# 📦 Group Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_group_id(group: Group) -> str:
    """
    Returns the group ID (e.g. 'light', 'sensor').
    """
    return group.group_id


def list_entities(group: Group) -> Dict[str, Entity]:
    """
    Returns all entities in the group, indexed by their entity_id.
    """
    log.debug(f"📋 Listing entities for group '{group.group_id}'")
    return group.entities


def get_entity(group: Group, slug: str) -> Optional[Entity]:
    """
    Returns the entity from the group by slug (e.g. 'living_room_light') or None if not found.
    """
    log.debug(f"🔍 Looking up entity slug '{slug}' in group '{group.group_id}'")
    return group.get_entity(slug)
