
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pynetbox.core.query import RequestError

from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.routes.ipam.prefixes")

router = APIRouter(tags=["ipam.prefixes"])


@router.get("/", response_model=List[Dict[str, Any]])
def list_prefixes(limit: int = 0, offset: Optional[int] = None):
    """Retrieve all prefixes."""
    try:
        nb = get_netbox_client()
        return [dict(p) for p in nb.ipam.prefixes.all(limit=limit, offset=offset)]
    except Exception:
        log.exception("Failed to list prefixes")
        raise HTTPException(status_code=500, detail="Failed to list prefixes")


@router.get("/search", response_model=List[Dict[str, Any]])
def search_prefixes(q: Optional[str] = None, **filters: Any):
    """Search or filter prefixes."""
    try:
        nb = get_netbox_client()
        results = nb.ipam.prefixes.filter(q, **filters) if q else nb.ipam.prefixes.filter(**filters)
        return [dict(p) for p in results]
    except Exception:
        log.exception("Failed to filter prefixes")
        raise HTTPException(status_code=500, detail="Prefix filter failed")


@router.get("/count", response_model=Dict[str, int])
def count_prefixes(**filters: Any):
    """Count matching prefixes."""
    try:
        nb = get_netbox_client()
        return {"count": nb.ipam.prefixes.count(**filters)}
    except Exception:
        log.exception("Failed to count prefixes")
        raise HTTPException(status_code=500, detail="Count operation failed")


@router.get("/{prefix_id}", response_model=Dict[str, Any])
def get_prefix(prefix_id: int):
    """Retrieve a single prefix by ID."""
    try:
        nb = get_netbox_client()
        prefix = nb.ipam.prefixes.get(prefix_id)
        if not prefix:
            raise HTTPException(status_code=404, detail="Prefix not found")
        return dict(prefix)
    except Exception:
        log.exception(f"Failed to retrieve prefix {prefix_id}")
        raise HTTPException(status_code=500, detail="Error fetching prefix")


@router.post("/", response_model=Union[Dict[str, Any], List[Dict[str, Any]]])
def create_prefix(payload: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Create one or more prefixes."""
    try:
        nb = get_netbox_client()
        result = nb.ipam.prefixes.create(payload)
        return [dict(p) for p in result] if isinstance(result, list) else dict(result)
    except RequestError as e:
        log.error(f"Prefix creation failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during prefix creation")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{prefix_id}", response_model=Dict[str, bool])
def patch_prefix(prefix_id: int, updates: Dict[str, Any]):
    """Patch an existing prefix by ID."""
    try:
        nb = get_netbox_client()
        prefix = nb.ipam.prefixes.get(prefix_id)
        if not prefix:
            raise HTTPException(status_code=404, detail="Prefix not found")
        return {"success": prefix.update(updates)}
    except RequestError as e:
        log.error(f"Prefix update failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during prefix update")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/", response_model=Dict[str, Any])
def delete_prefixes(ids: List[int] = Query(..., description="IDs of prefixes to delete")):
    """Delete one or more prefixes by ID."""
    try:
        nb = get_netbox_client()
        deleted = nb.ipam.prefixes.delete(ids)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Prefix deletion failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during prefix deletion")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/filter", response_model=Dict[str, Any])
def delete_prefixes_by_filter(**filters: Any):
    """Delete prefixes using filter criteria."""
    try:
        nb = get_netbox_client()
        records = list(nb.ipam.prefixes.filter(**filters))
        if not records:
            return {"deleted": False, "message": "No matching prefixes found"}
        deleted = nb.ipam.prefixes.delete(records)
        return {"deleted": deleted}
    except RequestError as e:
        log.error(f"Filtered prefix deletion failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during filtered prefix deletion")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/choices", response_model=Dict[str, Any])
def get_prefix_choices():
    """Get choices for prefix fields."""
    try:
        nb = get_netbox_client()
        return nb.ipam.prefixes.choices()
    except Exception:
        log.exception("Failed to retrieve prefix choices")
        raise HTTPException(status_code=500, detail="Unable to retrieve choices")


@router.get("/{prefix_id}/available-ips", response_model=List[str])
def get_available_ips(prefix_id: int):
    """List available IPs inside a prefix."""
    try:
        nb = get_netbox_client()
        prefix = nb.ipam.prefixes.get(prefix_id)
        if not prefix:
            raise HTTPException(status_code=404, detail="Prefix not found")
        return [ip.address for ip in prefix.available_ips.list()]
    except Exception:
        log.exception("Failed to fetch available IPs")
        raise HTTPException(status_code=500, detail="Unable to fetch available IPs")


@router.post("/{prefix_id}/available-ips", response_model=List[Dict[str, Any]])
def allocate_ips(prefix_id: int, count: int = 1):
    """Allocate one or more available IPs from a prefix."""
    try:
        nb = get_netbox_client()
        prefix = nb.ipam.prefixes.get(prefix_id)
        if not prefix:
            raise HTTPException(status_code=404, detail="Prefix not found")
        return [dict(ip) for ip in prefix.available_ips.create([{} for _ in range(count)])]
    except RequestError as e:
        log.error(f"IP allocation failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during IP allocation")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{prefix_id}/available-child-prefixes", response_model=List[str])
def get_child_prefixes(prefix_id: int):
    """List available child prefixes within a parent prefix."""
    try:
        nb = get_netbox_client()
        prefix = nb.ipam.prefixes.get(prefix_id)
        if not prefix:
            raise HTTPException(status_code=404, detail="Prefix not found")
        return [p.prefix for p in prefix.available_prefixes.list()]
    except Exception:
        log.exception("Failed to list child prefixes")
        raise HTTPException(status_code=500, detail="Unable to list child prefixes")


@router.post("/{prefix_id}/available-child-prefixes", response_model=Dict[str, Any])
def create_child_prefix(prefix_id: int, prefix_length: int):
    """Create a new child prefix of specified length."""
    try:
        nb = get_netbox_client()
        prefix = nb.ipam.prefixes.get(prefix_id)
        if not prefix:
            raise HTTPException(status_code=404, detail="Prefix not found")
        return dict(prefix.available_prefixes.create({"prefix_length": prefix_length}))
    except RequestError as e:
        log.error(f"Child prefix creation failed: {e.error}")
        raise HTTPException(status_code=400, detail=e.error)
    except Exception:
        log.exception("Unexpected error during child prefix creation")
        raise HTTPException(status_code=500, detail="Internal server error")
