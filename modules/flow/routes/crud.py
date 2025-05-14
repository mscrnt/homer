

from fastapi import APIRouter, HTTPException, Body, Query
from typing import Optional, List, Dict, Any

from modules.flow.logic import crud as crud_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("flow-crud")
router = APIRouter()

@router.post("/create")
def create_entity(
    entity_type: str = Query(...),
    data: Dict[str, Any] = Body(...)
):
    """Create a new ShotGrid entity."""
    try:
        return crud_logic.create_entity(entity_type, data)
    except Exception as e:
        log.exception("❌ Create failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/find")
def find_entities(
    entity_type: str = Query(...),
    filters: List = Body(...),
    fields: Optional[List[str]] = Body(default=["id", "type"]),
    order: Optional[List[Dict[str, str]]] = None,
    limit: int = 0
):
    """Find ShotGrid entities using filters."""
    try:
        return crud_logic.find_entities(entity_type, filters, fields, order, limit)
    except Exception as e:
        log.exception("❌ Find failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/find-one")
def find_one_entity(
    entity_type: str = Query(...),
    filters: List = Body(...),
    fields: Optional[List[str]] = Body(default=["id", "type"])
):
    """Find a single entity matching filters."""
    try:
        return crud_logic.find_one_entity(entity_type, filters, fields)
    except Exception as e:
        log.exception("❌ Find one failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update")
def update_entity(
    entity_type: str = Query(...),
    entity_id: int = Query(...),
    data: Dict[str, Any] = Body(...),
    multi_entity_update_modes: Optional[Dict[str, str]] = Body(default=None)
):
    """Update a ShotGrid entity."""
    try:
        return crud_logic.update_entity(entity_type, entity_id, data, multi_entity_update_modes)
    except Exception as e:
        log.exception("❌ Update failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete")
def delete_entity(
    entity_type: str = Query(...),
    entity_id: int = Query(...)
):
    """Soft-delete (retire) a ShotGrid entity."""
    try:
        return crud_logic.delete_entity(entity_type, entity_id)
    except Exception as e:
        log.exception("❌ Delete failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/revive")
def revive_entity(
    entity_type: str = Query(...),
    entity_id: int = Query(...)
):
    """Revive a previously deleted entity."""
    try:
        return crud_logic.revive_entity(entity_type, entity_id)
    except Exception as e:
        log.exception("❌ Revive failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
def batch_operations(
    requests: List[Dict[str, Any]] = Body(...)
):
    """Execute batch operations (create/update/delete)."""
    try:
        return crud_logic.batch_operations(requests)
    except Exception as e:
        log.exception("❌ Batch failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize")
def summarize_entity(
    entity_type: str = Query(...),
    filters: List = Body(...),
    summary_fields: List[Dict[str, str]] = Body(...),
    grouping: Optional[List[Dict[str, str]]] = Body(default=None)
):
    """Summarize a ShotGrid query by field(s)."""
    try:
        return crud_logic.summarize_entity(entity_type, filters, summary_fields, grouping)
    except Exception as e:
        log.exception("❌ Summarize failed")
        raise HTTPException(status_code=500, detail=str(e))
