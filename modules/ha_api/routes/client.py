from typing import Optional, Union, Dict, Any, Tuple, Generator, AsyncGenerator
from homeassistant_api import State, Event, Domain, Group, LogbookEntry, History

from modules.ha_api.client import build_client  # ✅ Use the shared client builder


# ──────────────────────────────────────────────────────────────────────────────
# 📦 Sync methods
# ──────────────────────────────────────────────────────────────────────────────

def get_states() -> Tuple[State, ...]:
    with build_client() as client:
        return client.get_states()

def get_state(entity_id: str) -> Optional[State]:
    with build_client() as client:
        return client.get_state(entity_id=entity_id)

def get_entities() -> Dict[str, Group]:
    with build_client() as client:
        return client.get_entities()

def get_entity(entity_id: str) -> Optional[Any]:
    with build_client() as client:
        return client.get_entity(entity_id=entity_id)

def get_domain(domain_id: str) -> Optional[Domain]:
    with build_client() as client:
        return client.get_domain(domain_id)

def get_domains() -> Dict[str, Domain]:
    with build_client() as client:
        return client.get_domains()

def get_config() -> Dict[str, Any]:
    with build_client() as client:
        return client.get_config()

def get_components() -> Tuple[str, ...]:
    with build_client() as client:
        return client.get_components()

def get_error_log() -> str:
    with build_client() as client:
        return client.get_error_log()

def get_event(name: str) -> Optional[Event]:
    with build_client() as client:
        return client.get_event(name)

def get_events() -> Tuple[Event, ...]:
    with build_client() as client:
        return client.get_events()

def get_logbook_entries(*args, **kwargs) -> Generator[LogbookEntry, None, None]:
    with build_client() as client:
        return client.get_logbook_entries(*args, **kwargs)

def get_entity_histories(
    entities: Optional[list] = None,
    start_timestamp: Optional[str] = None,
    end_timestamp: Optional[str] = None,
    significant_changes_only: bool = False
) -> Generator[History, None, None]:
    with build_client() as client:
        return client.get_entity_histories(
            entities=entities,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            significant_changes_only=significant_changes_only
        )

def get_rendered_template(template: str) -> str:
    with build_client() as client:
        return client.get_rendered_template(template)

def trigger_service(domain: str, service: str, **data) -> Tuple[State, ...]:
    with build_client() as client:
        return client.trigger_service(domain, service, **data)

def trigger_service_with_response(domain: str, service: str, **data) -> Tuple[Tuple[State, ...], Dict[str, Any]]:
    with build_client() as client:
        return client.trigger_service_with_response(domain, service, **data)

def fire_event(event_type: str, **event_data) -> Optional[str]:
    with build_client() as client:
        return client.fire_event(event_type, **event_data)

def set_state(state: State) -> State:
    with build_client() as client:
        return client.set_state(state)

def check_api_config() -> bool:
    with build_client() as client:
        return client.check_api_config()

def check_api_running() -> bool:
    with build_client() as client:
        return client.check_api_running()

# ──────────────────────────────────────────────────────────────────────────────
# ⚡ Async methods
# ──────────────────────────────────────────────────────────────────────────────

async def async_get_states() -> Tuple[State, ...]:
    async with build_client(use_async=True) as client:
        return await client.async_get_states()

async def async_get_state(entity_id: str) -> Optional[State]:
    async with build_client(use_async=True) as client:
        return await client.async_get_state(entity_id=entity_id)

async def async_trigger_service(domain: str, service: str, **data) -> Tuple[State, ...]:
    async with build_client(use_async=True) as client:
        return await client.async_trigger_service(domain, service, **data)

async def async_get_config() -> Dict[str, Any]:
    async with build_client(use_async=True) as client:
        return await client.async_get_config()
