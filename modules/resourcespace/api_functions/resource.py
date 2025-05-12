# modules/resourcespace/api_functions/resource.py

from ..client import call_api, call_api_multipart

def get_resource_data(resource_id: int) -> dict:
    """Get top-level property data for a resource."""
    return call_api("get_resource_data", {"param1": str(resource_id)})


def get_resource_field_data(resource_id: int) -> dict:
    """Return all field data (full metadata) for a resource."""
    return call_api("get_resource_field_data", {"param1": str(resource_id)})


def create_resource(resource_type: int, archive: int = 999, url: str = "", no_exif: int = 0,
                    revert: int = 0, autorotate: int = 0, metadata: str = "") -> dict:
    """Create a new resource, optionally with metadata."""
    return call_api("create_resource", {
        "param1": str(resource_type),
        "param2": str(archive),
        "param3": url,
        "param4": str(no_exif),
        "param5": str(revert),
        "param6": str(autorotate),
        "param7": metadata,
    })


def delete_resource(resource_id: int) -> dict:
    """Delete a resource."""
    return call_api("delete_resource", {"param1": str(resource_id)})


def copy_resource(from_resource: int, resource_type: int = -1) -> dict:
    """Copy a resource (metadata only, not files)."""
    return call_api("copy_resource", {
        "param1": str(from_resource),
        "param2": str(resource_type)
    })


def get_resource_log(resource_id: int, fetchrows: int = -1) -> dict:
    """Fetch log entries for a resource."""
    return call_api("get_resource_log", {
        "param1": str(resource_id),
        "param2": str(fetchrows)
    })


def update_resource_type(resource_id: int, resource_type: int) -> dict:
    """Change the resource type of a resource."""
    return call_api("update_resource_type", {
        "param1": str(resource_id),
        "param2": str(resource_type)
    })


def get_resource_path(ref: int, size: str = "", generate: int = 1, extension: str = "jpg",
                      page: int = 1, watermarked: int = 0, alternative: int = -1) -> dict:
    """Get a temporary download path for a resource file."""
    return call_api("get_resource_path", {
        "param1": str(ref),
        "param2": "",
        "param3": size,
        "param4": str(generate),
        "param5": extension,
        "param6": str(page),
        "param7": str(watermarked),
        "param8": str(alternative),
    })


def get_alternative_files(resource_id: int, orderby: str = "", sort: str = "", file_type: str = "") -> dict:
    """Get a list of alternative files for a resource."""
    return call_api("get_alternative_files", {
        "param1": str(resource_id),
        "param2": orderby,
        "param3": sort,
        "param4": file_type
    })


def get_resource_types() -> dict:
    """Get a list of available resource types for this user."""
    return call_api("get_resource_types")





def add_alternative_file(resource_id: int, name: str, description: str = "", file_name: str = "",
                         file_extension: str = "", file_size: int = 0, alt_type: str = "", file_url: str = "") -> dict:
    """Adds a new alternative file to a resource."""
    return call_api("add_alternative_file", {
        "param1": str(resource_id),
        "param2": name,
        "param3": description,
        "param4": file_name,
        "param5": file_extension,
        "param6": str(file_size),
        "param7": alt_type,
        "param8": file_url
    })


def delete_alternative_file(resource_id: int, alt_id: int) -> dict:
    """Deletes an alternative file."""
    return call_api("delete_alternative_file", {
        "param1": str(resource_id),
        "param2": str(alt_id)
    })


def upload_file(resource_id: int, file_path: str, no_exif: int = 0, revert: int = 0, autorotate: int = 0) -> dict:
    """Uploads a local file to an existing resource."""
    return call_api("upload_file", {
        "param1": str(resource_id),
        "param2": str(no_exif),
        "param3": str(revert),
        "param4": str(autorotate),
        "param5": file_path
    })


def upload_file_by_url(resource_id: int, url: str, no_exif: int = 0, revert: int = 0, autorotate: int = 0) -> dict:
    """Uploads a file from a remote URL to a resource."""
    return call_api("upload_file_by_url", {
        "param1": str(resource_id),
        "param2": str(no_exif),
        "param3": str(revert),
        "param4": str(autorotate),
        "param5": url
    })


def upload_multipart(resource_id: int, file_path: str, no_exif: bool = True, revert: bool = False,
                     previewonly: bool = False, alternative: int = 0) -> dict:
    """
    Upload file using multipart POST (used for large files or replacing alternative).
    Note: `file` is NOT signed.
    """
    params = {
        "ref": str(resource_id),
        "no_exif": str(int(no_exif)),
        "revert": str(int(revert)),
        "previewonly": str(int(previewonly)),
        "alternative": str(alternative)
    }

    return call_api_multipart("upload_multipart", params=params, file_path=file_path)


def get_related_resources(resource_id: int) -> dict:
    """Returns a list of resources related to the given resource."""
    return call_api("get_related_resources", {
        "param1": str(resource_id)
    })


def resource_log_last_rows(minref: int = 0, days: int = 7, maxrecords: int = 0,
                            field: str = "", log_code: str = "") -> dict:
    """Fetch recent entries from the resource log."""
    return call_api("resource_log_last_rows", {
        "param1": str(minref),
        "param2": str(days),
        "param3": str(maxrecords),
        "param4": field,
        "param5": log_code
    })


def replace_resource_file(resource_id: int, file_location: str,
                          no_exif: int = 0, autorotate: int = 0, keep_original: int = 1) -> dict:
    """Replace the main file of a resource."""
    return call_api("replace_resource_file", {
        "param1": str(resource_id),
        "param2": file_location,
        "param3": str(no_exif),
        "param4": str(autorotate),
        "param5": str(keep_original)
    })


def get_resource_all_image_sizes(resource_id: int) -> dict:
    """Get all image sizes available for a resource."""
    return call_api("get_resource_all_image_sizes", {
        "param1": str(resource_id)
    })


def put_resource_data(resource_id: int, data: dict) -> dict:
    """Update top-level resource property data (not metadata fields)."""
    from json import dumps
    return call_api("put_resource_data", {
        "param1": str(resource_id),
        "param2": dumps(data)
    })


def update_related_resource(ref: int, related: str, add: int = 1) -> dict:
    """Add or remove related resources."""
    return call_api("update_related_resource", {
        "param1": str(ref),
        "param2": related,
        "param3": str(add)
    })


def relate_all_resources(related_csv: str) -> dict:
    """Relate a group of resources together."""
    return call_api("relate_all_resources", {
        "param1": related_csv
    })


def get_edit_access(resource_id: int) -> dict:
    """Check if the current user has edit access to a resource."""
    return call_api("get_edit_access", {
        "param1": str(resource_id)
    })


def get_resource_access(resource_id: int) -> dict:
    """Get the access level of the current user for a resource."""
    return call_api("get_resource_access", {
        "param1": str(resource_id)
    })


def resource_file_readonly(resource_id: int) -> dict:
    """Check if the file is read-only (e.g. due to filestore template restrictions)."""
    return call_api("resource_file_readonly", {
        "param1": str(resource_id)
    })
