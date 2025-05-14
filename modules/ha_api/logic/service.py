from typing import Optional, Dict, Any, Tuple, Union
from homeassistant_api import Service, State
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.service")

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Service Metadata Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_service_id(service: Service) -> str:
    """
    Returns the service ID string (e.g. 'turn_on', 'set_temperature').
    """
    return service.service_id


def get_service_domain(service: Service) -> str:
    """
    Returns the domain name this service belongs to (e.g. 'light', 'climate').
    """
    return service.domain.domain_id


def describe_service(service: Service) -> Dict[str, Any]:
    """
    Returns a structured dictionary with full details of a service.
    """
    return {
        "service_id": service.service_id,
        "domain": get_service_domain(service),
        "name": service.name,
        "description": service.description,
        "fields": describe_fields(service.fields),
    }


def describe_fields(fields: Optional[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Returns detailed info about each field used by the service.
    """
    if not fields:
        return {}

    result = {}
    for key, field in fields.items():
        result[key] = {
            "name": field.name,
            "description": field.description,
            "required": field.required,
            "example": field.example,
            "selector": field.selector,
        }
    return result

# ──────────────────────────────────────────────────────────────────────────────
# 🚀 Triggering Services
# ──────────────────────────────────────────────────────────────────────────────

def trigger(service: Service, entity_id: Optional[str] = None, **service_data) -> Union[
    Tuple[State, ...],
    Tuple[Tuple[State, ...], Dict[str, Any]],
    Dict[str, Any],
    None
]:
    """
    Synchronously trigger the service.
    """
    log.debug(f"🔁 Triggering service '{service.service_id}' on entity '{entity_id}' with data: {service_data}")
    return service.trigger(entity_id=entity_id, **service_data)


async def async_trigger(service: Service, entity_id: Optional[str] = None, **service_data) -> Union[
    Tuple[State, ...],
    Tuple[Tuple[State, ...], Dict[str, Any]]
]:
    """
    Asynchronously trigger the service.
    """
    log.debug(f"⚡ Async triggering service '{service.service_id}' on entity '{entity_id}' with data: {service_data}")
    return await service.async_trigger(entity_id=entity_id, **service_data)
