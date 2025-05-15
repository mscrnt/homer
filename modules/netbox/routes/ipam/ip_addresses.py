
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pynetbox.core.query import RequestError

from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.routes.ipam.ip_addresses")

router = APIRouter(tags=["ipam.ip_addresses"])


@router.get("/", response_model=List[Dict[str, Any]])
def list_ip_addresses(limit: int = 0, offset: Optional[int] = None):
    """Retrieve all IP addresses."""
    try:
        nb = get_netbox_client()
        return [dict(ip) for ip in nb.ipam.ip_addresses.all(limit=limit, offset=offset)]
    except Exception:
        log.exception("Failed to list IP addresses")
        raise HTTPException(status_code=500, detail="Unable to fetch IP addresses")


@router.get("/search", response_model=List[Dict[str, Any]])
def search_ip_addresses(q: Optional[str] = None, **filters: Any):
    """Filter IP addresses by query or keyword filters."""
    try:
        nb = get_netbox_client()
        results = nb.ipam.ip_addresses.filter(q, **filters) if q else nb.ipam.ip_addresses.filter(**filters)
        return [dict(ip) for ip in results]
    except Exception:
        log.exception("Failed to filter IP addresses")
        raise HTTPException(status_code=500, detail="IP address filter failed")


@router.get("/count", response_model=Dict[str, int])
def count_ip_addresses(**filters: Any):
    """Return count of IP addresses matching query."""
    try:
        nb = get_netbox_client()
        return {"count": nb.ipam.ip_addresses.count(**filters)}
    except Exception:
        log.exception("Failed to count IP addresses")
        raise HTTPException(status_code=500, detail="Count operation failed")


@router.get("/{ip_id}", response_model=Dict[str, Any])
def get_ip_by_id(ip_id: int):
    """Get an IP address by ID."""
    try:
        nb = get_netbox_client()
        record = nb.ipam.ip_addresses.get(ip_id)
        if not record:
            raise HTTPException(status_code=404, detail="IP address not found")
        return dict(record)
    except HTTPException:
        raise
    except Exception:
        log.exception(f"Failed to retrieve IP address {ip_id}")
        raise HTTPException(status_code=500, detail="Error retrieving IP address")


@router.post("/", response_model=Union[Dict[str, Any], List[Dict[str, Any]]])
def create_ip(payload: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Create one or more IP addresses."""
    try:
        nb = get_netbox_client()
        result = nb.ipam.ip_addresses.create(payload)
        return [dict(r) for r in result] if isinstance(result, list) else dict(result)
    except RequestError as e:
        log.error(f"IP address creation failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during IP address creation")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{address}", response_model=Dict[str, bool])
def update_ip_fields(address: str, updates: Dict[str, Any]):
    """Patch a single IP address using its address string."""
    try:
        nb = get_netbox_client()
        ip = nb.ipam.ip_addresses.get(address=address)
        if not ip:
            raise HTTPException(status_code=404, detail="IP address not found")
        return {"success": ip.update(updates)}
    except RequestError as e:
        log.error(f"Update failed for IP '{address}': {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during IP update")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/", response_model=Dict[str, Any])
def delete_ips(ids: List[int] = Query(..., description="List of IP IDs to delete")):
    """Delete IPs by list of IDs."""
    try:
        nb = get_netbox_client()
        deleted = nb.ipam.ip_addresses.delete(ids)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Delete failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during IP deletion")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/filter", response_model=Dict[str, Any])
def delete_ips_by_filter(**filters: Any):
    """Delete IP addresses by filter."""
    try:
        nb = get_netbox_client()
        records = list(nb.ipam.ip_addresses.filter(**filters))
        if not records:
            return {"deleted": False, "message": "No matching IPs found"}
        deleted = nb.ipam.ip_addresses.delete(records)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Filtered delete failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during filtered delete")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/choices", response_model=Dict[str, Any])
def get_ip_choices():
    """Get choices for IP address fields (status, role, etc.)."""
    try:
        nb = get_netbox_client()
        return nb.ipam.ip_addresses.choices()
    except Exception:
        log.exception("Failed to retrieve IP address choices")
        raise HTTPException(status_code=500, detail="Unable to retrieve choices")
