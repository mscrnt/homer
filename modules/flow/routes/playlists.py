

from fastapi import APIRouter, HTTPException
from homer.utils.logger import get_module_logger
from modules.flow.logic import playlists as playlists_logic

log = get_module_logger("flow-playlists")
router = APIRouter()

@router.get("/playlists/{playlist_id}/versions")
def get_playlist_versions(playlist_id: int):
    """
    Get versions on a playlist via PlaylistVersionConnection.
    """
    try:
        return playlists_logic.get_playlist_versions(playlist_id)
    except Exception as e:
        log.exception("❌ Failed to fetch playlist versions")
        raise HTTPException(status_code=500, detail=str(e))
