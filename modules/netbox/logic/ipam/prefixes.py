
from typing import Any, Dict, List, Optional, Union
from pynetbox.core.response import Record
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.ipam.prefixes")


def get_all_prefixes(limit: int = 0, offset: Optional[int] = None) -> List[Record]:
    """Retrieve all prefixes from NetBox."""
    nb = get_netbox_client()
    log.debug("Fetching all prefixes")
    return list(nb.ipam.prefixes.all(limit=limit, offset=offset))


def filter_prefixes(*args: str, **kwargs: Any) -> List[Record]:
    """Filter prefixes with keyword or freeform search."""
    nb = get_netbox_client()
    log.debug(f"Filtering prefixes with args={args}, kwargs={kwargs}")
    return list(nb.ipam.prefixes.filter(*args, **kwargs))


def get_prefix(id: Optional[int] = None, **kwargs) -> Optional[Record]:
    """Get a prefix by ID or named search."""
    nb = get_netbox_client()
    if id:
        log.debug(f"Fetching prefix by ID: {id}")
        return nb.ipam.prefixes.get(id)
    log.debug(f"Fetching prefix with filters: {kwargs}")
    return nb.ipam.prefixes.get(**kwargs)


def count_prefixes(*args: str, **kwargs: Any) -> int:
    """Count the number of prefixes that match given filters."""
    nb = get_netbox_client()
    log.debug(f"Counting prefixes with args={args}, kwargs={kwargs}")
    return nb.ipam.prefixes.count(*args, **kwargs)


def create_prefixes(
    prefix_data: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> Union[Record, List[Record]]:
    """Create one or more prefixes."""
    nb = get_netbox_client()
    log.info("Creating prefix(es)")
    try:
        return nb.ipam.prefixes.create(prefix_data)
    except RequestError as e:
        log.error(f"Prefix creation failed: {e.error}")
        raise


def update_prefixes(
    updates: Union[List[Record], List[Dict[str, Any]]]
) -> List[Record]:
    """Update one or more existing prefixes."""
    nb = get_netbox_client()
    log.info("Updating prefixes")
    try:
        return nb.ipam.prefixes.update(updates)
    except RequestError as e:
        log.error(f"Prefix update failed: {e.error}")
        raise


def delete_prefixes(
    prefix_objs: Union[List[Record], List[int]]
) -> bool:
    """Delete one or more prefixes."""
    nb = get_netbox_client()
    log.warning(f"Deleting {len(prefix_objs)} prefix(es)")
    try:
        return nb.ipam.prefixes.delete(prefix_objs)
    except RequestError as e:
        log.error(f"Prefix deletion failed: {e.error}")
        raise


def delete_prefixes_by_filter(**kwargs) -> bool:
    """Delete prefixes that match a given filter query."""
    nb = get_netbox_client()
    records = list(nb.ipam.prefixes.filter(**kwargs))
    log.warning(f"Deleting {len(records)} prefix(es) by filter: {kwargs}")
    try:
        return nb.ipam.prefixes.delete(records)
    except RequestError as e:
        log.error(f"Filtered prefix deletion failed: {e.error}")
        raise


def get_prefix_choices() -> Dict[str, Any]:
    """Return available field choices for prefixes (e.g., status)."""
    nb = get_netbox_client()
    log.debug("Fetching prefix choices")
    return nb.ipam.prefixes.choices()


def get_available_ips(prefix_id: int) -> List[str]:
    """List available IPs within a given prefix."""
    nb = get_netbox_client()
    prefix = nb.ipam.prefixes.get(prefix_id)
    if not prefix:
        log.error(f"Prefix with ID {prefix_id} not found")
        return []
    log.debug(f"Listing available IPs in prefix {prefix.prefix}")
    return [ip.address for ip in prefix.available_ips.list()]


def create_available_ips(prefix_id: int, count: int = 1) -> List[Record]:
    """Allocate one or more new IP addresses within a prefix."""
    nb = get_netbox_client()
    prefix = nb.ipam.prefixes.get(prefix_id)
    if not prefix:
        log.error(f"Prefix with ID {prefix_id} not found")
        return []
    log.info(f"Creating {count} new IP(s) in prefix {prefix.prefix}")
    return prefix.available_ips.create([{} for _ in range(count)])


def get_available_child_prefixes(prefix_id: int) -> List[str]:
    """List available sub-prefixes inside a parent prefix."""
    nb = get_netbox_client()
    prefix = nb.ipam.prefixes.get(prefix_id)
    if not prefix:
        log.error(f"Prefix with ID {prefix_id} not found")
        return []
    log.debug(f"Listing available child prefixes in {prefix.prefix}")
    return [p.prefix for p in prefix.available_prefixes.list()]


def create_child_prefix(
    prefix_id: int,
    prefix_length: int
) -> Optional[Record]:
    """Create a child prefix from a parent prefix by specifying desired prefix length."""
    nb = get_netbox_client()
    prefix = nb.ipam.prefixes.get(prefix_id)
    if not prefix:
        log.error(f"Prefix with ID {prefix_id} not found")
        return None
    log.info(f"Creating child prefix in {prefix.prefix} with length /{prefix_length}")
    try:
        return prefix.available_prefixes.create({"prefix_length": prefix_length})
    except RequestError as e:
        log.error(f"Child prefix allocation failed: {e.error}")
        raise


def update_prefix_fields(prefix_id: int, updates: Dict[str, Any]) -> bool:
    """Patch a single prefix by its ID."""
    prefix = get_prefix(id=prefix_id)
    if not prefix:
        log.error(f"Prefix with ID {prefix_id} not found")
        return False
    log.info(f"Updating prefix ID {prefix_id} with fields: {updates}")
    try:
        return prefix.update(updates)
    except RequestError as e:
        log.error(f"Prefix update failed: {e.error}")
        raise


def get_prefix_dict(prefix: Union[int, Record]) -> Optional[Dict[str, Any]]:
    """Return a dict representation of a prefix."""
    if isinstance(prefix, Record):
        return dict(prefix)
    record = get_prefix(id=prefix)
    return dict(record) if record else None
