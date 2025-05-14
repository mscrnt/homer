from typing import Optional, Dict, Any
from homeassistant_api import Event
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.event")

# ──────────────────────────────────────────────────────────────────────────────
# 🧠 Event Model Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_event_type(event: Event) -> str:
    """
    Returns the event name/type.
    """
    log.debug(f"🔍 Inspecting event type: {event.event}")
    return event.event


def get_listener_count(event: Event) -> int:
    """
    Returns the number of active listeners on the event.
    """
    log.debug(f"👂 Listener count for '{event.event}': {event.listener_count}")
    return event.listener_count


def fire_event(event: Event, **event_data) -> Optional[str]:
    """
    Fires the event synchronously.
    """
    log.info(f"🚨 Firing event '{event.event}' with data: {event_data}")
    return event.fire(**event_data)


async def async_fire_event(event: Event, **event_data) -> str:
    """
    Fires the event asynchronously.
    """
    log.info(f"⚡ Async firing event '{event.event}' with data: {event_data}")
    return await event.async_fire(**event_data)


def describe_event(event: Event) -> Dict[str, Any]:
    """
    Returns a dictionary summary of the event's metadata.
    """
    info = {
        "event": event.event,
        "listeners": event.listener_count
    }
    log.debug(f"📋 Event summary: {info}")
    return info
