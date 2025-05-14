from typing import Dict, Optional, Any
from homeassistant_api import Domain, Service
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.domain")

# ──────────────────────────────────────────────────────────────────────────────
# 🔍 Domain Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_domain_id(domain: Domain) -> str:
    """
    Returns the ID of the domain (e.g. 'light', 'climate').
    """
    return domain.domain_id


def list_services(domain: Domain) -> Dict[str, Service]:
    """
    Returns all service definitions in a domain.
    """
    return domain.services


def get_service(domain: Domain, service_id: str) -> Optional[Service]:
    """
    Retrieve a single service by ID from a domain.
    """
    return domain.get_service(service_id)


def describe_service(service: Service) -> Dict[str, Any]:
    """
    Returns a detailed description of a service.
    """
    return {
        "service_id": service.service_id,
        "domain": service.domain.domain_id,
        "name": service.name,
        "description": service.description,
        "fields": describe_fields(service.fields)
    }


def describe_fields(fields: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Describes the service fields dictionary (parameters expected by the service).
    """
    if not fields:
        return {}

    described = {}
    for field_id, field in fields.items():
        described[field_id] = {
            "name": field.name,
            "description": field.description,
            "example": field.example,
            "required": field.required,
            "selector": field.selector,
        }

    return described
