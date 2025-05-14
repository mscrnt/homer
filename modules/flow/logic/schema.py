

from typing import Dict, Any
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.schema.logic")


def get_entity_types() -> Dict[str, Any]:
    """
    Return all active ShotGrid entity types and display names.
    """
    sg = get_sg_client()
    log.debug("📘 Reading ShotGrid schema entity types")
    return sg.schema_entity_read()


def get_entity_fields(entity: str) -> Dict[str, Any]:
    """
    Return all fields for a given ShotGrid entity type.
    """
    sg = get_sg_client()
    log.debug(f"📘 Reading schema fields for entity: {entity}")
    return sg.schema_field_read(entity)
