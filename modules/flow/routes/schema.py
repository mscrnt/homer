

from fastapi import APIRouter, HTTPException
from homer.utils.logger import get_module_logger
from modules.flow.logic import schema as schema_logic

log = get_module_logger("flow-schema")
router = APIRouter()

@router.get("/entities")
def get_entity_types():
    """Return all active entity types and display names."""
    try:
        return schema_logic.get_entity_types()
    except Exception as e:
        log.exception("❌ Failed to get entity types")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{entity}/fields")
def get_entity_fields(entity: str):
    """Return all fields for a given entity type."""
    try:
        return schema_logic.get_entity_fields(entity)
    except Exception as e:
        log.exception(f"❌ Failed to get fields for {entity}")
        raise HTTPException(status_code=500, detail=str(e))
