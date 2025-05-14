from typing import Tuple
from homeassistant_api import History, State
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.history")

# ──────────────────────────────────────────────────────────────────────────────
# 📚 History Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_entity_id(history: History) -> str:
    """
    Returns the `entity_id` shared across all states in the history record.
    """
    if not history.states:
        log.warning("📭 No states found in history object.")
        return ""

    entity_id = history.entity_id
    log.debug(f"📜 History resolved for entity: {entity_id}")
    return entity_id


def get_all_states(history: History) -> Tuple[State, ...]:
    """
    Returns all past states from a `History` object.
    """
    log.debug(f"📘 History contains {len(history.states)} states.")
    return history.states


def get_last_state(history: History) -> State:
    """
    Returns the most recent state in the history sequence.
    """
    if not history.states:
        raise ValueError("⚠️ No states available in the history to retrieve last state.")
    
    last_state = history.states[-1]
    log.debug(f"🕓 Last state for {history.entity_id}: {last_state.state}")
    return last_state


def get_first_state(history: History) -> State:
    """
    Returns the earliest recorded state in the history.
    """
    if not history.states:
        raise ValueError("⚠️ No states available in the history to retrieve first state.")

    first_state = history.states[0]
    log.debug(f"🕘 First state for {history.entity_id}: {first_state.state}")
    return first_state
