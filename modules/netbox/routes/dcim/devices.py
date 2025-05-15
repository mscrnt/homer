
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.routes.dcim.devices")

router = APIRouter(tags=["dcim.devices"])


@router.get("/", response_model=List[Dict[str, Any]])
def list_devices(limit: int = 0, offset: Optional[int] = None):
    """Get all devices."""
    try:
        nb = get_netbox_client()
        devices = nb.dcim.devices.all(limit=limit, offset=offset)
        return [dict(d) for d in devices]
    except Exception:
        log.exception("Failed to list devices")
        raise HTTPException(status_code=500, detail="Unable to fetch devices")


@router.get("/search", response_model=List[Dict[str, Any]])
def search_devices(q: Optional[str] = None, **filters: Any):
    """Filter devices with freeform q or keyword filters."""
    try:
        nb = get_netbox_client()
        if q:
            results = nb.dcim.devices.filter(q, **filters)
        else:
            results = nb.dcim.devices.filter(**filters)
        return [dict(d) for d in results]
    except Exception:
        log.exception("Failed to filter devices")
        raise HTTPException(status_code=500, detail="Device filter failed")


@router.get("/count", response_model=Dict[str, int])
def count_devices(**filters: Any):
    """Count devices matching filters."""
    try:
        nb = get_netbox_client()
        return {"count": nb.dcim.devices.count(**filters)}
    except Exception:
        log.exception("Count failed")
        raise HTTPException(status_code=500, detail="Count operation failed")


@router.get("/{device_id}", response_model=Dict[str, Any])
def get_device_by_id(device_id: int):
    """Fetch a single device by ID."""
    try:
        nb = get_netbox_client()
        device = nb.dcim.devices.get(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return dict(device)
    except HTTPException:
        raise
    except Exception:
        log.exception(f"Failed to fetch device {device_id}")
        raise HTTPException(status_code=500, detail="Error retrieving device")


@router.post("/", response_model=Union[Dict[str, Any], List[Dict[str, Any]]])
def create_devices(payload: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Create one or more devices."""
    try:
        nb = get_netbox_client()
        result = nb.dcim.devices.create(payload)
        if isinstance(result, list):
            return [dict(d) for d in result]
        return dict(result)
    except RequestError as e:
        log.error(f"Device creation failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during device creation")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{device_id}", response_model=Dict[str, bool])
def update_device(device_id: int, updates: Dict[str, Any]):
    """Patch a device by ID."""
    try:
        nb = get_netbox_client()
        device = nb.dcim.devices.get(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        success = device.update(updates)
        return {"success": success}
    except RequestError as e:
        log.error(f"Update failed for device {device_id}: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during update")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/", response_model=Dict[str, bool])
def delete_devices_by_ids(ids: List[int] = Query(..., description="List of device IDs")):
    """Bulk delete devices by IDs."""
    try:
        nb = get_netbox_client()
        deleted = nb.dcim.devices.delete(ids)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Bulk delete failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during bulk delete")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/filter", response_model=Dict[str, Any])
def delete_devices_by_filter(**filters: Any):
    """Delete devices using filter criteria."""
    try:
        nb = get_netbox_client()
        records = list(nb.dcim.devices.filter(**filters))
        if not records:
            return {"deleted": False, "message": "No matching devices"}
        deleted = nb.dcim.devices.delete(records)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Filtered delete failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during filtered delete")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/choices", response_model=Dict[str, Any])
def get_device_choices():
    """Get choices for device fields (status, role, etc.)."""
    try:
        nb = get_netbox_client()
        return nb.dcim.devices.choices()
    except Exception:
        log.exception("Failed to fetch device choices")
        raise HTTPException(status_code=500, detail="Unable to retrieve choices")
