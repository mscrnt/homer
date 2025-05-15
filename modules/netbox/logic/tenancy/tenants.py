
from typing import Any, Dict, List, Optional, Union
from pynetbox.core.response import Record
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.tenancy.tenants")


def get_all_tenants(limit: int = 0, offset: Optional[int] = None) -> List[Record]:
    """Retrieve all tenants."""
    nb = get_netbox_client()
    log.debug("Fetching all tenants")
    return list(nb.tenancy.tenants.all(limit=limit, offset=offset))


def filter_tenants(*args: str, **kwargs: Any) -> List[Record]:
    """Filter tenants with freeform or named arguments."""
    nb = get_netbox_client()
    log.debug(f"Filtering tenants with args={args}, kwargs={kwargs}")
    return list(nb.tenancy.tenants.filter(*args, **kwargs))


def get_tenant(id: Optional[int] = None, **kwargs) -> Optional[Record]:
    """Get a tenant by ID or unique filter (e.g., name)."""
    nb = get_netbox_client()
    if id:
        log.debug(f"Getting tenant by ID: {id}")
        return nb.tenancy.tenants.get(id)
    log.debug(f"Getting tenant with filters: {kwargs}")
    return nb.tenancy.tenants.get(**kwargs)


def count_tenants(*args: str, **kwargs: Any) -> int:
    """Return the count of tenants matching filters."""
    nb = get_netbox_client()
    log.debug(f"Counting tenants with args={args}, kwargs={kwargs}")
    return nb.tenancy.tenants.count(*args, **kwargs)


def create_tenants(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Record, List[Record]]:
    """Create one or more tenants."""
    nb = get_netbox_client()
    log.info("Creating tenant(s)")
    try:
        return nb.tenancy.tenants.create(data)
    except RequestError as e:
        log.error(f"Tenant creation failed: {e.error}")
        raise


def update_tenants(data: Union[List[Dict[str, Any]], List[Record]]) -> List[Record]:
    """Update one or more tenants (must include ID)."""
    nb = get_netbox_client()
    log.info("Updating tenants")
    try:
        return nb.tenancy.tenants.update(data)
    except RequestError as e:
        log.error(f"Tenant update failed: {e.error}")
        raise


def update_tenant_fields(tenant_id: int, updates: Dict[str, Any]) -> bool:
    """Patch a single tenant by ID."""
    tenant = get_tenant(id=tenant_id)
    if not tenant:
        log.error(f"Tenant with ID {tenant_id} not found")
        return False
    log.info(f"Updating tenant ID {tenant_id} with fields: {updates}")
    try:
        return tenant.update(updates)
    except RequestError as e:
        log.error(f"Tenant update failed: {e.error}")
        raise


def delete_tenants(tenants: Union[List[Record], List[int]]) -> bool:
    """Delete tenants by ID or Record."""
    nb = get_netbox_client()
    log.warning(f"Deleting {len(tenants)} tenant(s)")
    try:
        return nb.tenancy.tenants.delete(tenants)
    except RequestError as e:
        log.error(f"Tenant deletion failed: {e.error}")
        raise


def delete_tenants_by_filter(**kwargs) -> bool:
    """Delete all tenants matching filter criteria."""
    nb = get_netbox_client()
    tenants = list(nb.tenancy.tenants.filter(**kwargs))
    log.warning(f"Deleting {len(tenants)} tenants matching filter: {kwargs}")
    try:
        return nb.tenancy.tenants.delete(tenants)
    except RequestError as e:
        log.error(f"Filtered tenant deletion failed: {e.error}")
        raise


def get_tenant_choices() -> Dict[str, Any]:
    """Return tenant-related choice fields."""
    nb = get_netbox_client()
    log.debug("Fetching tenant choices")
    return nb.tenancy.tenants.choices()


def get_tenant_dict(tenant: Union[int, Record]) -> Optional[Dict[str, Any]]:
    """Return a tenant as a dictionary."""
    if isinstance(tenant, Record):
        return dict(tenant)
    record = get_tenant(id=tenant)
    return dict(record) if record else None
