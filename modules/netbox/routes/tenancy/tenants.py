
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pynetbox.core.query import RequestError
from pynetbox.core.response import Record

from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.routes.tenancy.tenants")

router = APIRouter(tags=["tenancy.tenants"])

@router.get("/", response_model=List[Dict[str, Any]])
def list_tenants(limit: int = 0, offset: Optional[int] = None):
    """List all tenants."""
    nb = get_netbox_client()
    try:
        return [dict(t) for t in nb.tenancy.tenants.all(limit=limit, offset=offset)]
    except Exception as e:
        log.error(f"Failed to list tenants: {e}")
        raise HTTPException(status_code=500, detail="Unable to list tenants")


@router.get("/search", response_model=List[Dict[str, Any]])
def search_tenants(q: Optional[str] = None, **filters):
    """Search or filter tenants."""
    nb = get_netbox_client()
    try:
        return [dict(t) for t in nb.tenancy.tenants.filter(q, **filters)]
    except Exception as e:
        log.error(f"Tenant filter failed: {e}")
        raise HTTPException(status_code=500, detail="Tenant filter failed")


@router.get("/count")
def count_tenants(**filters):
    """Count tenants matching filters."""
    nb = get_netbox_client()
    try:
        return {"count": nb.tenancy.tenants.count(**filters)}
    except Exception as e:
        log.error(f"Count failed: {e}")
        raise HTTPException(status_code=500, detail="Count failed")


@router.get("/{tenant_id}", response_model=Dict[str, Any])
def get_tenant_by_id(tenant_id: int):
    """Get tenant by ID."""
    nb = get_netbox_client()
    tenant = nb.tenancy.tenants.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return dict(tenant)


@router.post("/", response_model=Union[Dict[str, Any], List[Dict[str, Any]]])
def create_tenant(payload: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Create one or more tenants."""
    nb = get_netbox_client()
    try:
        result = nb.tenancy.tenants.create(payload)
        return [dict(t) for t in result] if isinstance(result, list) else dict(result)
    except RequestError as e:
        log.error(f"Tenant creation failed: {e.error}")
        raise HTTPException(status_code=400, detail=str(e.error))


@router.patch("/{tenant_id}")
def patch_tenant(tenant_id: int, updates: Dict[str, Any]):
    """Patch tenant by ID."""
    nb = get_netbox_client()
    tenant = nb.tenancy.tenants.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    try:
        return {"success": tenant.update(updates)}
    except RequestError as e:
        log.error(f"Update failed: {e.error}")
        raise HTTPException(status_code=400, detail=str(e.error))


@router.delete("/", response_model=Dict[str, Any])
def delete_tenants_by_ids(ids: List[int] = Query(...)):
    """Delete tenants by ID list."""
    nb = get_netbox_client()
    try:
        return {"deleted": nb.tenancy.tenants.delete(ids)}
    except RequestError as e:
        log.error(f"Deletion failed: {e.error}")
        raise HTTPException(status_code=400, detail=str(e.error))


@router.delete("/filter")
def delete_tenants_by_filter(**filters):
    """Delete tenants matching filters."""
    nb = get_netbox_client()
    tenants = list(nb.tenancy.tenants.filter(**filters))
    if not tenants:
        return {"deleted": False, "message": "No matching tenants"}
    try:
        return {"deleted": nb.tenancy.tenants.delete(tenants)}
    except RequestError as e:
        log.error(f"Filter-based deletion failed: {e.error}")
        raise HTTPException(status_code=400, detail=str(e.error))


@router.get("/choices", response_model=Dict[str, Any])
def get_tenant_choices():
    """Get tenant choice values."""
    nb = get_netbox_client()
    return nb.tenancy.tenants.choices()
