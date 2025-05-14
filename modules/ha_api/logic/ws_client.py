from typing import Optional, Dict, Any, Tuple, Generator
import os

from homeassistant_api import WebsocketClient, State, Group, Domain, Context
from homer.utils.logger import get_module_logger
from modules.ha_api.config import HomeAssistantEnv

log = get_module_logger("ha_api.ws_client")


def get_env(required: bool = False, safe: bool = False) -> Optional[HomeAssistantEnv]:
    try:
        env = HomeAssistantEnv(**os.environ)
        if required and (not env.HA_API_URL or not env.HA_API_TOKEN):
            raise ValueError("HA_API_URL and HA_API_TOKEN are required but missing.")
        return env
    except Exception:
        if safe:
            return None
        raise


def _get_ws_client() -> WebsocketClient:
    env = get_env()
    if not env.HA_WS_URL:
        raise RuntimeError("HA_WS_URL must be set to use WebsocketClient.")
    return WebsocketClient(env.HA_WS_URL, env.HA_API_TOKEN.get_secret_value())


# ──────────────────────────────────────────────────────────────────────────────
# ⚡ WebSocket Client Utility Methods
# ──────────────────────────────────────────────────────────────────────────────

def get_states() -> Tuple[State, ...]:
    with _get_ws_client() as ws:
        states = ws.get_states()
        log.debug(f"📦 Fetched {len(states)} states via WS")
        return states

def get_state(entity_id: str) -> Optional[State]:
    with _get_ws_client() as ws:
        state = ws.get_state(entity_id=entity_id)
        log.debug(f"🔍 Fetched WS state for {entity_id}: {state}")
        return state

def get_entities() -> Dict[str, Group]:
    with _get_ws_client() as ws:
        entities = ws.get_entities()
        log.debug(f"📚 Fetched WS entities: {list(entities.keys())}")
        return entities

def get_entity(entity_id: str) -> Optional[Any]:
    with _get_ws_client() as ws:
        entity = ws.get_entity(entity_id=entity_id)
        log.debug(f"📦 Fetched WS entity {entity_id}: {entity}")
        return entity

def get_domains() -> Dict[str, Domain]:
    with _get_ws_client() as ws:
        domains = ws.get_domains()
        log.debug(f"📂 Fetched {len(domains)} WS domains")
        return domains

def get_rendered_template(template: str) -> str:
    with _get_ws_client() as ws:
        rendered = ws.get_rendered_template(template)
        log.debug(f"🧪 Rendered WS template: {template} → {rendered}")
        return rendered

def get_config() -> Dict[str, Any]:
    with _get_ws_client() as ws:
        config = ws.get_config()
        log.debug("⚙️ Fetched WS config")
        return config

def trigger_service(domain: str, service: str, **data) -> None:
    with _get_ws_client() as ws:
        ws.trigger_service(domain, service, **data)
        log.info(f"🚀 Triggered WS service {domain}.{service} with data: {data}")

def trigger_service_with_response(domain: str, service: str, **data) -> Dict[str, Any]:
    with _get_ws_client() as ws:
        response = ws.trigger_service_with_response(domain, service, **data)
        log.info(f"📬 WS service {domain}.{service} response: {response}")
        return response

def fire_event(event_type: str, **event_data) -> Context:
    with _get_ws_client() as ws:
        ctx = ws.fire_event(event_type, **event_data)
        log.info(f"🔥 Fired WS event '{event_type}' with data: {event_data}")
        return ctx

def listen_events(event_type: Optional[str] = None) -> Generator:
    ws = _get_ws_client()
    log.info(f"👂 Listening to WS events: {event_type or 'ALL'}")
    return ws.listen_events(event_type)

def listen_trigger(trigger: str, **trigger_fields) -> Generator:
    ws = _get_ws_client()
    log.info(f"🎯 Listening to WS trigger: {trigger} with filters: {trigger_fields}")
    return ws.listen_trigger(trigger, **trigger_fields)
