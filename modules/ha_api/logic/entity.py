from typing import Optional
from datetime import datetime

from homeassistant_api import Entity, State, History
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.entity")

# ──────────────────────────────────────────────────────────────────────────────
# 📦 Entity Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_entity_id(entity: Entity) -> str:
    """
    Returns the full `entity_id`, constructed from group and slug (e.g. 'light.kitchen').
    """
    entity_id = entity.entity_id
    log.debug(f"🔎 Entity ID resolved: {entity_id}")
    return entity_id


def get_current_state(entity: Entity) -> State:
    """
    Refreshes and returns the current state of the entity.
    """
    state = entity.get_state()
    log.debug(f"📥 Refreshed state for {entity.entity_id}: {state.state}")
    return state


def update_state(entity: Entity) -> State:
    """
    Pushes the current local `State` object to Home Assistant.
    """
    state = entity.update_state()
    log.info(f"📤 Updated state pushed for {entity.entity_id}: {state.state}")
    return state


def get_history(
    entity: Entity,
    start_timestamp: Optional[datetime] = None,
    end_timestamp: Optional[datetime] = None,
    significant_changes_only: bool = False
) -> Optional[History]:
    """
    Returns the history of state changes for the given entity.
    """
    log.debug(f"📚 Fetching history for {entity.entity_id}")
    return entity.get_history(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        significant_changes_only=significant_changes_only
    )


# ──────────────────────────────────────────────────────────────────────────────
# ⚡ Async Versions
# ──────────────────────────────────────────────────────────────────────────────

async def async_get_current_state(entity: Entity) -> State:
    """
    Refreshes and returns the current state of the entity asynchronously.
    """
    state = await entity.async_get_state()
    log.debug(f"📥 [Async] Refreshed state for {entity.entity_id}: {state.state}")
    return state


async def async_update_state(entity: Entity) -> State:
    """
    Pushes the current local `State` object to Home Assistant asynchronously.
    """
    state = await entity.async_update_state()
    log.info(f"📤 [Async] Updated state pushed for {entity.entity_id}: {state.state}")
    return state


async def async_get_history(
    entity: Entity,
    start_timestamp: Optional[datetime] = None,
    end_timestamp: Optional[datetime] = None,
    significant_changes_only: bool = False
) -> Optional[History]:
    """
    Asynchronously returns the history of state changes for the given entity.
    """
    log.debug(f"📚 [Async] Fetching history for {entity.entity_id}")
    return await entity.async_get_history(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        significant_changes_only=significant_changes_only
    )
