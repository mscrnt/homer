
from typing import Any, Optional, Union, List, Dict
from pynetbox.core.response import Record
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.dcim.interfaces")


def get_all_interfaces(limit: int = 0, offset: Optional[int] = None) -> List[Record]:
    """Retrieve all interfaces from NetBox."""
    nb = get_netbox_client()
    log.debug("Fetching all interfaces")
    return list(nb.dcim.interfaces.all(limit=limit, offset=offset))


def filter_interfaces(*args: str, **kwargs: Any) -> List[Record]:
    """Filter interfaces using full-text or keyword filters."""
    nb = get_netbox_client()
    log.debug(f"Filtering interfaces with args={args}, kwargs={kwargs}")
    return list(nb.dcim.interfaces.filter(*args, **kwargs))


def get_interface(id: Optional[int] = None, **kwargs) -> Optional[Record]:
    """Get a single interface by ID or filters like name/device."""
    nb = get_netbox_client()
    if id:
        log.debug(f"Fetching interface by ID: {id}")
        return nb.dcim.interfaces.get(id)
    log.debug(f"Fetching interface by filters: {kwargs}")
    return nb.dcim.interfaces.get(**kwargs)


def count_interfaces(*args: str, **kwargs: Any) -> int:
    """Return count of interfaces."""
    nb = get_netbox_client()
    log.debug(f"Counting interfaces with args={args}, kwargs={kwargs}")
    return nb.dcim.interfaces.count(*args, **kwargs)


def create_interface(
    interface_data: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> Union[Record, List[Record], None]:
    """Create one or more interfaces."""
    nb = get_netbox_client()
    log.info("Creating interface(s)")
    try:
        return nb.dcim.interfaces.create(interface_data)
    except RequestError as e:
        log.error(f"Interface creation failed: {e.error}")
        raise


def update_interfaces(
    updates: Union[List[Record], List[Dict[str, Any]]]
) -> Optional[List[Record]]:
    """Bulk update existing interfaces."""
    nb = get_netbox_client()
    log.info("Updating interface(s)")
    try:
        return nb.dcim.interfaces.update(updates)
    except RequestError as e:
        log.error(f"Interface update failed: {e.error}")
        raise


def delete_interfaces(
    interfaces: Union[List[Record], List[int]]
) -> bool:
    """Delete one or more interfaces by record or ID."""
    nb = get_netbox_client()
    log.warning(f"Deleting {len(interfaces)} interface(s)")
    try:
        return nb.dcim.interfaces.delete(interfaces)
    except RequestError as e:
        log.error(f"Interface deletion failed: {e.error}")
        raise


def delete_interfaces_by_filter(**kwargs) -> bool:
    """Delete all interfaces matching a filter query."""
    nb = get_netbox_client()
    records = list(nb.dcim.interfaces.filter(**kwargs))
    log.warning(f"Deleting {len(records)} interfaces by filter: {kwargs}")
    try:
        return nb.dcim.interfaces.delete(records)
    except RequestError as e:
        log.error(f"Filtered interface deletion failed: {e.error}")
        raise


def get_interface_choices() -> Dict[str, Any]:
    """Return valid choices for interface fields (type, mode, etc.)."""
    nb = get_netbox_client()
    log.debug("Fetching interface choices")
    return nb.dcim.interfaces.choices()


def get_interface_dict(interface: Union[int, str, Record], device: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Return a dictionary representation of an interface."""
    record = None
    if isinstance(interface, Record):
        return dict(interface)
    elif isinstance(interface, int):
        record = get_interface(id=interface)
    elif isinstance(interface, str) and device:
        record = get_interface(name=interface, device=device)
    if record:
        return dict(record)
    return None


def update_interface_fields(interface_name: str, device_name: str, data: Dict[str, Any]) -> bool:
    """Update a single interface on a specific device."""
    interface = get_interface(name=interface_name, device=device_name)
    if not interface:
        log.error(f"Interface '{interface_name}' on device '{device_name}' not found.")
        return False
    log.info(f"Updating fields for interface '{interface_name}' on device '{device_name}'")
    try:
        return interface.update(data)
    except RequestError as e:
        log.error(f"Update failed: {e.error}")
        raise


def assign_ip_to_interface(ip_record: Record, interface: Record) -> bool:
    """Assign an IP address record to a network interface."""
    log.info(f"Assigning IP {ip_record.address} to interface {interface.name}")
    try:
        ip_record.assigned_object = interface
        ip_record.assigned_object_id = interface.id
        ip_record.assigned_object_type = 'dcim.interface'
        return ip_record.save()
    except RequestError as e:
        log.error(f"IP assignment failed: {e.error}")
        raise
