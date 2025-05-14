from typing import Optional, Dict, Any
from homeassistant_api import LogbookEntry
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.logbook")

# ──────────────────────────────────────────────────────────────────────────────
# 📓 LogbookEntry Utilities
# ──────────────────────────────────────────────────────────────────────────────

def describe_entry(entry: LogbookEntry) -> Dict[str, Any]:
    """
    Returns a dictionary summary of a LogbookEntry.
    """
    summary = {
        "timestamp": entry.when.isoformat(),
        "name": entry.name,
        "message": entry.message,
        "entity_id": entry.entity_id,
        "state": entry.state,
        "domain": entry.domain,
        "context_id": entry.context_id,
        "icon": entry.icon,
    }
    log.debug(f"📝 Described logbook entry: {summary}")
    return summary


def is_entity_entry(entry: LogbookEntry, entity_id: str) -> bool:
    """
    Returns True if the log entry is related to the given entity_id.
    """
    result = entry.entity_id == entity_id
    log.debug(f"🔍 Entry for '{entry.entity_id}' matches '{entity_id}': {result}")
    return result


def has_message(entry: LogbookEntry) -> bool:
    """
    Checks if the log entry contains a non-empty message.
    """
    result = bool(entry.message and entry.message.strip())
    log.debug(f"💬 Logbook entry has message: {result}")
    return result
