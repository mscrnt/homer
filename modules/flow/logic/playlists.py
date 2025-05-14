

from typing import Dict, Any
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.playlists.logic")


def get_playlist_versions(playlist_id: int) -> Dict[str, Any]:
    """
    Retrieve all versions linked to a specific playlist via PlaylistVersionConnection.
    """
    sg = get_sg_client()
    filters = [["playlist", "is", {"type": "Playlist", "id": playlist_id}]]
    fields = [
        "playlist.Playlist.code",
        "sg_sort_order",
        "version.Version.code",
        "version.Version.user",
        "version.Version.entity"
    ]
    order = [{"column": "sg_sort_order", "direction": "asc"}]

    log.debug(f"Fetching PlaylistVersionConnections for playlist_id={playlist_id}")
    versions = sg.find("PlaylistVersionConnection", filters, fields, order)

    return {
        "playlist_id": playlist_id,
        "versions": versions
    }
