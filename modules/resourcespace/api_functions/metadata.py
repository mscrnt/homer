from ..client import call_api
from typing import Union

def get_field_options(field_ref: Union[int, str], nodeinfo: bool = False) -> dict:
    """Get available options for a fixed-list metadata field."""
    return call_api("get_field_options", {
        "param1": str(field_ref),
        "param2": str(int(nodeinfo))
    })

def get_node_id(value: str, field_ref: int) -> dict:
    """Find the node ID by label/value and metadata field ref."""
    return call_api("get_node_id", {
        "param1": value,
        "param2": str(field_ref)
    })

def get_nodes(field_ref: int, parent: int = None, recursive: bool = False,
              offset: int = None, rows: int = None, name: str = "",
              use_count: bool = False, order_by_translated_name: bool = False) -> dict:
    """Get all nodes for a field, optionally filtered or paginated."""
    return call_api("get_nodes", {
        "param1": str(field_ref),
        "param2": "" if parent is None else str(parent),
        "param3": str(int(recursive)),
        "param4": "" if offset is None else str(offset),
        "param5": "" if rows is None else str(rows),
        "param6": name,
        "param7": str(int(use_count)),
        "param8": str(int(order_by_translated_name))
    })

def add_resource_nodes(resource_id: int, node_ids: list[int]) -> dict:
    """Add nodes (by ID) to a single resource."""
    return call_api("add_resource_nodes", {
        "param1": str(resource_id),
        "param2": ",".join(map(str, node_ids))
    })

def add_resource_nodes_multi(resource_ids: list[int], node_ids: list[int]) -> dict:
    """Add node IDs to multiple resource IDs."""
    return call_api("add_resource_nodes_multi", {
        "param1": ",".join(map(str, resource_ids)),
        "param2": ",".join(map(str, node_ids))
    })

def update_field(resource_id: int, field: Union[int, str], value: str, nodevalues: bool = False) -> dict:
    """Update a metadata field value for a resource."""
    return call_api("update_field", {
        "param1": str(resource_id),
        "param2": str(field),
        "param3": value,
        "param4": str(int(nodevalues))
    })

def set_node(ref: Union[int, str], field_ref: int, name: str, parent: Union[int, None] = None,
             order_by: int = 0, returnexisting: bool = False) -> dict:
    """Create or update a node."""
    return call_api("set_node", {
        "param1": str(ref),
        "param2": str(field_ref),
        "param3": name,
        "param4": "" if parent is None else str(parent),
        "param5": str(order_by),
        "param6": str(int(returnexisting))
    })

def get_resource_type_fields(by_resource_types: str = "", find: str = "", by_types: str = "") -> dict:
    """Return metadata fields (requires admin 'a' permission)."""
    return call_api("get_resource_type_fields", {
        "param1": by_resource_types,
        "param2": find,
        "param3": by_types
    })

def create_resource_type_field(name: str, resource_types: str, field_type: int) -> dict:
    """Create a new metadata field (admin only)."""
    return call_api("create_resource_type_field", {
        "param1": name,
        "param2": resource_types,
        "param3": str(field_type)
    })

def toggle_active_state_for_nodes(node_refs: list[int]) -> dict:
    """Toggle active state of metadata nodes (e.g. enable/disable dropdown entries)."""
    from json import dumps
    return call_api("toggle_active_state_for_nodes", {
        "param1": dumps(node_refs)
    })
