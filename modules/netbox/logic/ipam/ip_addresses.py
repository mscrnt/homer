
from typing import Any, Dict, List, Optional, Union
from pynetbox.core.response import Record
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.ipam.ip_addresses")


def get_all_ip_addresses(limit: int = 0, offset: Optional[int] = None) -> List[Record]:
    """Retrieve all IP addresses from NetBox."""
    nb = get_netbox_client()
    log.debug("Fetching all IP addresses")
    return list(nb.ipam.ip_addresses.all(limit=limit, offset=offset))


def filter_ip_addresses(*args: str, **kwargs: Any) -> List[Record]:
    """Filter IP addresses using full-text or keyword filters."""
    nb = get_netbox_client()
    log.debug(f"Filtering IP addresses with args={args}, kwargs={kwargs}")
    return list(nb.ipam.ip_addresses.filter(*args, **kwargs))


def get_ip_address(id: Optional[int] = None, **kwargs) -> Optional[Record]:
    """Get a single IP address by ID or keyword filters (e.g. address)."""
    nb = get_netbox_client()
    if id:
        log.debug(f"Fetching IP address by ID: {id}")
        return nb.ipam.ip_addresses.get(id)
    log.debug(f"Fetching IP address with filters: {kwargs}")
    return nb.ipam.ip_addresses.get(**kwargs)


def count_ip_addresses(*args: str, **kwargs: Any) -> int:
    """Return count of IP addresses matching query."""
    nb = get_netbox_client()
    log.debug(f"Counting IP addresses with args={args}, kwargs={kwargs}")
    return nb.ipam.ip_addresses.count(*args, **kwargs)


def create_ip_address(
    ip_data: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> Union[Record, List[Record], None]:
    """Create one or more IP addresses."""
    nb = get_netbox_client()
    log.info("Creating IP address(es)")
    try:
        return nb.ipam.ip_addresses.create(ip_data)
    except RequestError as e:
        log.error(f"IP address creation failed: {e.error}")
        raise


def update_ip_addresses(
    updates: Union[List[Record], List[Dict[str, Any]]]
) -> Optional[List[Record]]:
    """Bulk update existing IP addresses."""
    nb = get_netbox_client()
    log.info("Updating IP address(es)")
    try:
        return nb.ipam.ip_addresses.update(updates)
    except RequestError as e:
        log.error(f"IP address update failed: {e.error}")
        raise


def delete_ip_addresses(
    ip_records: Union[List[Record], List[int]]
) -> bool:
    """Delete one or more IP addresses by record or ID."""
    nb = get_netbox_client()
    log.warning(f"Deleting {len(ip_records)} IP address(es)")
    try:
        return nb.ipam.ip_addresses.delete(ip_records)
    except RequestError as e:
        log.error(f"IP address deletion failed: {e.error}")
        raise


def delete_ip_addresses_by_filter(**kwargs) -> bool:
    """Delete all IP addresses matching a filter query."""
    nb = get_netbox_client()
    records = list(nb.ipam.ip_addresses.filter(**kwargs))
    log.warning(f"Deleting {len(records)} IP address(es) by filter: {kwargs}")
    try:
        return nb.ipam.ip_addresses.delete(records)
    except RequestError as e:
        log.error(f"Filtered IP address deletion failed: {e.error}")
        raise


def get_ip_address_choices() -> Dict[str, Any]:
    """Return valid choices for IP address fields (status, role, etc.)."""
    nb = get_netbox_client()
    log.debug("Fetching IP address choices")
    return nb.ipam.ip_addresses.choices()


def assign_ip_to_interface(
    address: str,
    interface: Record,
    tenant: Optional[Record] = None,
    dns_name: Optional[str] = None,
    tags: Optional[List[Dict[str, str]]] = None
) -> Record:
    """Create and assign an IP address to a device interface."""
    nb = get_netbox_client()
    payload = {
        "address": address,
        "assigned_object_type": "dcim.interface",
        "assigned_object_id": interface.id,
    }

    if tenant:
        payload["tenant"] = tenant.id
    if dns_name:
        payload["dns_name"] = dns_name
    if tags:
        payload["tags"] = tags

    log.info(f"Assigning IP {address} to interface ID={interface.id}")
    try:
        return nb.ipam.ip_addresses.create(payload)
    except RequestError as e:
        log.error(f"IP assignment failed: {e.error}")
        raise


def update_ip_address_fields(address: str, data: Dict[str, Any]) -> bool:
    """Update a single IP address by address string."""
    ip = get_ip_address(address=address)
    if not ip:
        log.error(f"IP address '{address}' not found.")
        return False
    log.info(f"Updating fields for IP address '{address}'")
    try:
        return ip.update(data)
    except RequestError as e:
        log.error(f"Update failed: {e.error}")
        raise


def get_ip_dict(ip: Union[int, str, Record]) -> Optional[Dict[str, Any]]:
    """Return a dictionary representation of an IP address."""
    record = None
    if isinstance(ip, Record):
        return dict(ip)
    elif isinstance(ip, int):
        record = get_ip_address(id=ip)
    elif isinstance(ip, str):
        record = get_ip_address(address=ip)
    if record:
        return dict(record)
    return None
