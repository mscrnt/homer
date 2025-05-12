from ..client import call_api

def get_user_collections() -> dict:
    """Return a list of the current user's collections."""
    return call_api("get_user_collections")


def add_resource_to_collection(resource_id: int, collection_id: int) -> dict:
    """Add a resource to a collection."""
    return call_api("add_resource_to_collection", {
        "param1": str(resource_id),
        "param2": str(collection_id)
    })


def remove_resource_from_collection(resource_id: int, collection_id: int) -> dict:
    """Remove a resource from a collection."""
    return call_api("remove_resource_from_collection", {
        "param1": str(resource_id),
        "param2": str(collection_id)
    })


def create_collection(name: str, forupload: int = 0) -> dict:
    """Create a new collection for the user."""
    return call_api("create_collection", {
        "param1": name,
        "param2": str(forupload)
    })


def delete_collection(collection_id: int) -> dict:
    """Delete a collection."""
    return call_api("delete_collection", {
        "param1": str(collection_id)
    })


def search_public_collections(search: str = "", order_by: str = "name", sort: str = "ASC", exclude_themes: int = 1) -> dict:
    """Search public and featured collections."""
    return call_api("search_public_collections", {
        "param1": search,
        "param2": order_by,
        "param3": sort,
        "param4": str(exclude_themes)
    })

def get_user_collections() -> dict:
    """Return a list of the current user's collections."""
    return call_api("get_user_collections")


def add_resource_to_collection(resource_id: int, collection_id: int) -> dict:
    """Add a resource to a collection."""
    return call_api("add_resource_to_collection", {
        "param1": str(resource_id),
        "param2": str(collection_id)
    })


def remove_resource_from_collection(resource_id: int, collection_id: int) -> dict:
    """Remove a resource from a collection."""
    return call_api("remove_resource_from_collection", {
        "param1": str(resource_id),
        "param2": str(collection_id)
    })


def create_collection(name: str, forupload: int = 0) -> dict:
    """Create a new collection for the user."""
    return call_api("create_collection", {
        "param1": name,
        "param2": str(forupload)
    })


def delete_collection(collection_id: int) -> dict:
    """Delete a collection."""
    return call_api("delete_collection", {
        "param1": str(collection_id)
    })


def search_public_collections(search: str = "", order_by: str = "name", sort: str = "ASC", exclude_themes: int = 1) -> dict:
    """Search public and featured collections."""
    return call_api("search_public_collections", {
        "param1": search,
        "param2": order_by,
        "param3": sort,
        "param4": str(exclude_themes)
    })


def get_collection(ref: int) -> dict:
    """Get details for a specific collection (admin only)."""
    return call_api("get_collection", {
        "param1": str(ref)
    })


def save_collection(ref: int, coldata: dict) -> dict:
    """Save metadata or settings for a collection."""
    from json import dumps
    return call_api("save_collection", {
        "param1": str(ref),
        "param2": dumps(coldata)
    })


def show_hide_collection(collection_id: int, show: int = 1, user_id: int = None) -> dict:
    """Show or hide a collection from the user's dropdown list."""
    if user_id is None:
        raise ValueError("❌ User ID is required to call show_hide_collection.")
    return call_api("show_hide_collection", {
        "param1": str(collection_id),
        "param2": str(show),
        "param3": str(user_id)
    })


def send_collection_to_admin(collection_id: int) -> dict:
    """Send a copy of the collection to an admin for review."""
    return call_api("send_collection_to_admin", {
        "param1": str(collection_id)
    })


def get_featured_collections(parent_id: int = 0) -> dict:
    """Return featured collections under a parent category."""
    return call_api("get_featured_collections", {
        "param1": str(parent_id)
    })


def delete_resources_in_collection(collection_id: int) -> dict:
    """Delete all resources in the collection."""
    return call_api("delete_resources_in_collection", {
        "param1": str(collection_id)
    })
