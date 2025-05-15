
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.routes.dcim.interfaces")

router = APIRouter(tags=["dcim.interfaces"])


@router.get("/", response_model=List[Dict[str, Any]])
def list_interfaces(limit: int = 0, offset: Optional[int] = None):
    """Get all interfaces."""
    try:
        nb = get_netbox_client()
        return [dict(i) for i in nb.dcim.interfaces.all(limit=limit, offset=offset)]
    except Exception:
        log.exception("Failed to list interfaces")
        raise HTTPException(status_code=500, detail="Unable to fetch interfaces")


@router.get("/search", response_model=List[Dict[str, Any]])
def search_interfaces(q: Optional[str] = None, **filters: Any):
    """Filter interfaces using query or keyword filters."""
    try:
        nb = get_netbox_client()
        results = nb.dcim.interfaces.filter(q, **filters) if q else nb.dcim.interfaces.filter(**filters)
        return [dict(i) for i in results]
    except Exception:
        log.exception("Failed to filter interfaces")
        raise HTTPException(status_code=500, detail="Interface filter failed")


@router.get("/count", response_model=Dict[str, int])
def count_interfaces(**filters: Any):
    """Count interfaces matching filters."""
    try:
        nb = get_netbox_client()
        return {"count": nb.dcim.interfaces.count(**filters)}
    except Exception:
        log.exception("Interface count failed")
        raise HTTPException(status_code=500, detail="Count operation failed")


@router.get("/{interface_id}", response_model=Dict[str, Any])
def get_interface_by_id(interface_id: int):
    """Fetch a single interface by ID."""
    try:
        nb = get_netbox_client()
        interface = nb.dcim.interfaces.get(interface_id)
        if not interface:
            raise HTTPException(status_code=404, detail="Interface not found")
        return dict(interface)
    except HTTPException:
        raise
    except Exception:
        log.exception(f"Failed to fetch interface {interface_id}")
        raise HTTPException(status_code=500, detail="Error retrieving interface")


@router.post("/", response_model=Union[Dict[str, Any], List[Dict[str, Any]]])
def create_interfaces(payload: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Create one or more interfaces."""
    try:
        nb = get_netbox_client()
        result = nb.dcim.interfaces.create(payload)
        if isinstance(result, list):
            return [dict(i) for i in result]
        return dict(result)
    except RequestError as e:
        log.error(f"Interface creation failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during interface creation")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{interface_id}", response_model=Dict[str, bool])
def update_interface(interface_id: int, updates: Dict[str, Any]):
    """Patch an interface by ID."""
    try:
        nb = get_netbox_client()
        interface = nb.dcim.interfaces.get(interface_id)
        if not interface:
            raise HTTPException(status_code=404, detail="Interface not found")
        success = interface.update(updates)
        return {"success": success}
    except RequestError as e:
        log.error(f"Update failed for interface {interface_id}: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during interface update")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/", response_model=Dict[str, bool])
def delete_interfaces_by_ids(ids: List[int] = Query(..., description="List of interface IDs")):
    """Bulk delete interfaces by IDs."""
    try:
        nb = get_netbox_client()
        deleted = nb.dcim.interfaces.delete(ids)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Bulk delete failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during bulk delete")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/filter", response_model=Dict[str, Any])
def delete_interfaces_by_filter(**filters: Any):
    """Delete interfaces using filter criteria."""
    try:
        nb = get_netbox_client()
        records = list(nb.dcim.interfaces.filter(**filters))
        if not records:
            return {"deleted": False, "message": "No matching interfaces"}
        deleted = nb.dcim.interfaces.delete(records)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Filtered delete failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during filtered delete")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/choices", response_model=Dict[str, Any])
def get_interface_choices():
    """Get choices for interface fields (type, mode, etc.)."""
    try:
        nb = get_netbox_client()
        return nb.dcim.interfaces.choices()
    except Exception:
        log.exception("Failed to fetch interface choices")
        raise HTTPException(status_code=500, detail="Unable to retrieve choices")
