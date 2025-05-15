
from typing import Any, Dict, List, Optional, Union
from pynetbox.core.response import Record, RecordSet
from pynetbox.core.query import RequestError
from pynetbox.core.endpoint import Endpoint
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.utils")


def get_all(endpoint: Endpoint, limit: int = 0, offset: Optional[int] = None) -> List[Record]:
    """Return all objects from a given NetBox endpoint."""
    log.debug(f"Fetching all records from {endpoint.name}")
    return list(endpoint.all(limit=limit, offset=offset))


def get_object(endpoint: Endpoint, id: Optional[int] = None, **kwargs) -> Optional[Record]:
    """Return a single object from the endpoint."""
    if id is not None:
        log.debug(f"Getting object by ID: {id}")
        return endpoint.get(id)
    log.debug(f"Getting object by filter: {kwargs}")
    return endpoint.get(**kwargs)


def filter_objects(endpoint: Endpoint, *args: str, **kwargs: Any) -> List[Record]:
    """Return a filtered list of objects from the endpoint."""
    log.debug(f"Filtering on {endpoint.name} with args={args}, kwargs={kwargs}")
    return list(endpoint.filter(*args, **kwargs))


def count_objects(endpoint: Endpoint, *args: str, **kwargs: Any) -> int:
    """Count the number of objects matching filters."""
    log.debug(f"Counting records on {endpoint.name} with args={args}, kwargs={kwargs}")
    return endpoint.count(*args, **kwargs)


def create_objects(endpoint: Endpoint, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Record, List[Record]]:
    """Create one or more objects on the endpoint."""
    log.info(f"Creating objects on {endpoint.name}")
    try:
        return endpoint.create(data)
    except RequestError as e:
        log.error(f"Create operation failed on {endpoint.name}: {e.error}")
        raise


def update_objects(endpoint: Endpoint, updates: Union[List[Dict[str, Any]], List[Record]]) -> List[Record]:
    """Update multiple objects (must include `id`)."""
    log.info(f"Updating objects on {endpoint.name}")
    try:
        return endpoint.update(updates)
    except RequestError as e:
        log.error(f"Update failed on {endpoint.name}: {e.error}")
        raise


def patch_object(record: Record, changes: Dict[str, Any]) -> bool:
    """Update a single object via .update()."""
    log.info(f"Patching record ID {record.id} with {changes}")
    try:
        return record.update(changes)
    except RequestError as e:
        log.error(f"Patch failed: {e.error}")
        raise


def delete_objects(endpoint: Endpoint, objects: Union[List[Record], List[int], RecordSet]) -> bool:
    """Delete one or more objects."""
    log.warning(f"Deleting {len(objects)} objects from {endpoint.name}")
    try:
        return endpoint.delete(objects)
    except RequestError as e:
        log.error(f"Delete failed on {endpoint.name}: {e.error}")
        raise


def delete_filtered(endpoint: Endpoint, **filters) -> bool:
    """Delete objects based on filters."""
    records = list(endpoint.filter(**filters))
    log.warning(f"Deleting {len(records)} filtered records from {endpoint.name} with {filters}")
    try:
        return endpoint.delete(records)
    except RequestError as e:
        log.error(f"Delete by filter failed on {endpoint.name}: {e.error}")
        raise


def get_choices(endpoint: Endpoint) -> Dict[str, Any]:
    """Return choice values from the endpoint (e.g., status, role)."""
    log.debug(f"Getting choices for {endpoint.name}")
    return endpoint.choices()


def serialize_record(record: Record) -> Dict[str, Any]:
    """Return a dict representation of a Record object."""
    return dict(record)


def safe_full_details(record: Record) -> bool:
    """Call .full_details() on a record safely."""
    log.debug(f"Fetching full details for record ID: {record.id}")
    try:
        return record.full_details()
    except RequestError as e:
        log.warning(f"Failed to fetch full details: {e.error}")
        return False


def summarize_record(record: Record) -> str:
    """Return a quick human-readable summary of a Record."""
    name = getattr(record, "name", None) or getattr(record, "display_name", None) or f"ID {record.id}"
    return f"{record.__class__.__name__}({name})"
