
from typing import Any, Optional, Union, List, Dict
from pynetbox.core.response import Record
from pynetbox.core.query import RequestError
from modules.netbox.client import get_netbox_client
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.dcim.racks")


def get_all_racks(limit: int = 0, offset: Optional[int] = None) -> List[Record]:
    """Retrieve all racks from NetBox."""
    nb = get_netbox_client()
    log.debug("Fetching all racks")
    return list(nb.dcim.racks.all(limit=limit, offset=offset))


def filter_racks(*args: str, **kwargs: Any) -> List[Record]:
    """Filter racks using full-text or keyword filters."""
    nb = get_netbox_client()
    log.debug(f"Filtering racks with args={args}, kwargs={kwargs}")
    return list(nb.dcim.racks.filter(*args, **kwargs))


def get_rack(id: Optional[int] = None, **kwargs) -> Optional[Record]:
    """Get a single rack by ID or keyword filters (e.g., name, site)."""
    nb = get_netbox_client()
    if id:
        log.debug(f"Fetching rack by ID: {id}")
        return nb.dcim.racks.get(id)
    log.debug(f"Fetching rack by filters: {kwargs}")
    return nb.dcim.racks.get(**kwargs)


def count_racks(*args: str, **kwargs: Any) -> int:
    """Return count of racks matching query."""
    nb = get_netbox_client()
    log.debug(f"Counting racks with args={args}, kwargs={kwargs}")
    return nb.dcim.racks.count(*args, **kwargs)


def create_rack(
    rack_data: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> Union[Record, List[Record], None]:
    """Create one or more racks."""
    nb = get_netbox_client()
    log.info("Creating rack(s)")
    try:
        return nb.dcim.racks.create(rack_data)
    except RequestError as e:
        log.error(f"Rack creation failed: {e.error}")
        raise


def update_racks(
    updates: Union[List[Record], List[Dict[str, Any]]]
) -> Optional[List[Record]]:
    """Bulk update existing racks."""
    nb = get_netbox_client()
    log.info("Updating rack(s)")
    try:
        return nb.dcim.racks.update(updates)
    except RequestError as e:
        log.error(f"Rack update failed: {e.error}")
        raise


def delete_racks(
    racks: Union[List[Record], List[int]]
) -> bool:
    """Delete one or more racks by record or ID."""
    nb = get_netbox_client()
    log.warning(f"Deleting {len(racks)} rack(s)")
    try:
        return nb.dcim.racks.delete(racks)
    except RequestError as e:
        log.error(f"Rack deletion failed: {e.error}")
        raise


def delete_racks_by_filter(**kwargs) -> bool:
    """Delete all racks matching a filter query."""
    nb = get_netbox_client()
    records = list(nb.dcim.racks.filter(**kwargs))
    log.warning(f"Deleting {len(records)} racks by filter: {kwargs}")
    try:
        return nb.dcim.racks.delete(records)
    except RequestError as e:
        log.error(f"Filtered rack deletion failed: {e.error}")
        raise


def get_rack_choices() -> Dict[str, Any]:
    """Return valid choices for rack fields (status, role, etc.)."""
    nb = get_netbox_client()
    log.debug("Fetching rack choices")
    return nb.dcim.racks.choices()


def get_rack_dict(rack: Union[int, str, Record], site: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Return a dictionary representation of a rack."""
    record = None
    if isinstance(rack, Record):
        return dict(rack)
    elif isinstance(rack, int):
        record = get_rack(id=rack)
    elif isinstance(rack, str) and site:
        record = get_rack(name=rack, site=site)
    if record:
        return dict(record)
    return None


def update_rack_fields(rack_name: str, site_name: str, data: Dict[str, Any]) -> bool:
    """Update a single rack by name and site."""
    rack = get_rack(name=rack_name, site=site_name)
    if not rack:
        log.error(f"Rack '{rack_name}' in site '{site_name}' not found.")
        return False
    log.info(f"Updating fields for rack '{rack_name}' at site '{site_name}'")
    try:
        return rack.update(data)
    except RequestError as e:
        log.error(f"Update failed: {e.error}")
        raise
