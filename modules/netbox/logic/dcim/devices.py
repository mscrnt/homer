
from typing import Any, Optional, Union, List, Dict
from pynetbox.core.response import Record
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.dcim.devices")


def get_all_devices(limit: int = 0, offset: Optional[int] = None) -> List[Record]:
    """Retrieve all devices from NetBox."""
    nb = get_netbox_client()
    log.debug("Fetching all devices")
    return list(nb.dcim.devices.all(limit=limit, offset=offset))


def filter_devices(*args: str, **kwargs: Any) -> List[Record]:
    """Filter devices using full-text or keyword filters."""
    nb = get_netbox_client()
    log.debug(f"Filtering devices with args={args}, kwargs={kwargs}")
    return list(nb.dcim.devices.filter(*args, **kwargs))


def get_device(id: Optional[int] = None, **kwargs) -> Optional[Record]:
    """Get a single device by ID or keyword filters."""
    nb = get_netbox_client()
    if id:
        log.debug(f"Fetching device by ID: {id}")
        return nb.dcim.devices.get(id)
    log.debug(f"Fetching device by filters: {kwargs}")
    return nb.dcim.devices.get(**kwargs)


def count_devices(*args: str, **kwargs: Any) -> int:
    """Return the count of devices matching filters."""
    nb = get_netbox_client()
    log.debug(f"Counting devices with args={args}, kwargs={kwargs}")
    return nb.dcim.devices.count(*args, **kwargs)


def create_device(
    device_data: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> Union[Record, List[Record], None]:
    """Create a new device or list of devices."""
    nb = get_netbox_client()
    log.info("Creating device(s)")
    try:
        return nb.dcim.devices.create(device_data)
    except RequestError as e:
        log.error(f"Device creation failed: {e.error}")
        raise


def update_devices(
    updates: Union[List[Record], List[Dict[str, Any]]]
) -> Optional[List[Record]]:
    """Bulk update existing devices."""
    nb = get_netbox_client()
    log.info("Updating device(s)")
    try:
        return nb.dcim.devices.update(updates)
    except RequestError as e:
        log.error(f"Device update failed: {e.error}")
        raise


def delete_devices(
    devices: Union[List[Record], List[int]]
) -> bool:
    """Delete one or more devices by record or ID."""
    nb = get_netbox_client()
    log.warning(f"Deleting {len(devices)} device(s)")
    try:
        return nb.dcim.devices.delete(devices)
    except RequestError as e:
        log.error(f"Device deletion failed: {e.error}")
        raise


def delete_devices_by_filter(**kwargs) -> bool:
    """Delete all devices matching a filter query."""
    nb = get_netbox_client()
    records = list(nb.dcim.devices.filter(**kwargs))
    log.warning(f"Deleting {len(records)} devices by filter: {kwargs}")
    try:
        return nb.dcim.devices.delete(records)
    except RequestError as e:
        log.error(f"Filtered device deletion failed: {e.error}")
        raise


def get_device_choices() -> Dict[str, Any]:
    """Return valid choices for device fields (role, status, etc.)."""
    nb = get_netbox_client()
    log.debug("Fetching device choices")
    return nb.dcim.devices.choices()


def get_device_dict(device: Union[int, str, Record]) -> Optional[Dict[str, Any]]:
    """Return a dictionary representation of a device."""
    record = None
    if isinstance(device, Record):
        return dict(device)
    elif isinstance(device, int):
        record = get_device(id=device)
    elif isinstance(device, str):
        record = get_device(name=device)
    if record:
        return dict(record)
    return None


def update_device_fields(device_name: str, data: Dict[str, Any]) -> bool:
    """Update a single device identified by name."""
    device = get_device(name=device_name)
    if not device:
        log.error(f"Device '{device_name}' not found.")
        return False
    log.info(f"Updating fields for device '{device_name}'")
    try:
        return device.update(data)
    except RequestError as e:
        log.error(f"Update failed: {e.error}")
        raise
