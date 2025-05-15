
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.routes.dcim.racks")

router = APIRouter(tags=["dcim.racks"])


@router.get("/", response_model=List[Dict[str, Any]])
def list_racks(limit: int = 0, offset: Optional[int] = None):
    """Retrieve all racks."""
    try:
        nb = get_netbox_client()
        return [dict(r) for r in nb.dcim.racks.all(limit=limit, offset=offset)]
    except Exception:
        log.exception("Failed to list racks")
        raise HTTPException(status_code=500, detail="Unable to fetch racks")


@router.get("/search", response_model=List[Dict[str, Any]])
def search_racks(q: Optional[str] = None, **filters: Any):
    """Filter racks using query or keyword arguments."""
    try:
        nb = get_netbox_client()
        results = nb.dcim.racks.filter(q, **filters) if q else nb.dcim.racks.filter(**filters)
        return [dict(r) for r in results]
    except Exception:
        log.exception("Failed to filter racks")
        raise HTTPException(status_code=500, detail="Rack filter failed")


@router.get("/count", response_model=Dict[str, int])
def count_racks(**filters: Any):
    """Count racks matching filters."""
    try:
        nb = get_netbox_client()
        return {"count": nb.dcim.racks.count(**filters)}
    except Exception:
        log.exception("Rack count failed")
        raise HTTPException(status_code=500, detail="Count operation failed")


@router.get("/{rack_id}", response_model=Dict[str, Any])
def get_rack_by_id(rack_id: int):
    """Fetch a single rack by ID."""
    try:
        nb = get_netbox_client()
        rack = nb.dcim.racks.get(rack_id)
        if not rack:
            raise HTTPException(status_code=404, detail="Rack not found")
        return dict(rack)
    except HTTPException:
        raise
    except Exception:
        log.exception(f"Failed to fetch rack {rack_id}")
        raise HTTPException(status_code=500, detail="Error retrieving rack")


@router.post("/", response_model=Union[Dict[str, Any], List[Dict[str, Any]]])
def create_rack(payload: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Create one or more racks."""
    try:
        nb = get_netbox_client()
        result = nb.dcim.racks.create(payload)
        return [dict(r) for r in result] if isinstance(result, list) else dict(result)
    except RequestError as e:
        log.error(f"Rack creation failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during rack creation")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{rack_id}", response_model=Dict[str, bool])
def update_rack(rack_id: int, updates: Dict[str, Any]):
    """Update a single rack by ID."""
    try:
        nb = get_netbox_client()
        rack = nb.dcim.racks.get(rack_id)
        if not rack:
            raise HTTPException(status_code=404, detail="Rack not found")
        return {"success": rack.update(updates)}
    except RequestError as e:
        log.error(f"Rack update failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during rack update")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/", response_model=Dict[str, bool])
def delete_racks_by_ids(ids: List[int] = Query(..., description="Rack IDs to delete")):
    """Bulk delete racks by ID."""
    try:
        nb = get_netbox_client()
        deleted = nb.dcim.racks.delete(ids)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Bulk rack delete failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during bulk delete")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/filter", response_model=Dict[str, Any])
def delete_racks_by_filter(**filters: Any):
    """Delete racks using filter criteria."""
    try:
        nb = get_netbox_client()
        records = list(nb.dcim.racks.filter(**filters))
        if not records:
            return {"deleted": False, "message": "No matching racks found"}
        deleted = nb.dcim.racks.delete(records)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Delete by filter failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during filtered delete")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/choices", response_model=Dict[str, Any])
def get_rack_choices():
    """Get available rack field choices."""
    try:
        nb = get_netbox_client()
        return nb.dcim.racks.choices()
    except Exception:
        log.exception("Failed to retrieve rack choices")
        raise HTTPException(status_code=500, detail="Unable to retrieve choices")
