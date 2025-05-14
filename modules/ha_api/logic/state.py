from datetime import datetime
from typing import Any, Dict, Optional

from homeassistant_api import State


# ──────────────────────────────────────────────────────────────────────────────
# 📦 State Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_state_value(state: State) -> str:
    """
    Returns the string state value (e.g. "on", "off", "75").
    """
    return state.state


def get_attribute(state: State, key: str, default: Any = None) -> Any:
    """
    Safely fetches an attribute from a State object.
    """
    return state.attributes.get(key, default)


def get_last_changed(state: State) -> Optional[datetime]:
    """
    Returns the timestamp of the last time the state changed.
    """
    return state.last_changed


def get_last_updated(state: State) -> Optional[datetime]:
    """
    Returns the timestamp of the last time the state was updated (even if not changed).
    """
    return state.last_updated


def get_entity_id(state: State) -> str:
    """
    Returns the entity ID from the state (e.g. 'light.living_room').
    """
    return state.entity_id


def get_context_id(state: State) -> Optional[str]:
    """
    Returns the context ID if available (used for tracing).
    """
    if state.context:
        return state.context.id
    return None


def to_dict(state: State) -> Dict[str, Any]:
    """
    Serializes a State object into a plain dict for export/logging.
    """
    return {
        "entity_id": state.entity_id,
        "state": state.state,
        "attributes": state.attributes,
        "last_changed": state.last_changed.isoformat() if state.last_changed else None,
        "last_updated": state.last_updated.isoformat() if state.last_updated else None,
        "context_id": get_context_id(state),
    }


def is_state_on(state: State) -> bool:
    """
    Returns True if the state is 'on', 'open', 'playing', etc.
    """
    return state.state.lower() in {"on", "open", "playing", "unlocked", "active"}


def is_state_off(state: State) -> bool:
    """
    Returns True if the state is 'off', 'closed', 'paused', etc.
    """
    return state.state.lower() in {"off", "closed", "paused", "locked", "idle"}
