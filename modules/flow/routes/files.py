

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List, Optional, Dict, Any
from homer.utils.logger import get_module_logger
import modules.flow.logic.files as files_logic

log = get_module_logger("flow-files")
router = APIRouter()

@router.post("/upload")
def upload_file(
    entity_type: str = Query(...),
    entity_id: int = Query(...),
    field_name: Optional[str] = Query(None),
    display_name: Optional[str] = Query(None),
    tag_list: Optional[str] = Query(None),
    file: UploadFile = File(...)
):
    """Upload a file to an entity (creates Attachment, optionally sets File field)."""
    try:
        result = files_logic.upload_file(entity_type, entity_id, file, field_name, display_name, tag_list)
        return {"attachment_id": result}
    except Exception as e:
        log.exception("❌ File upload failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/thumbnail")
def upload_thumbnail(
    entity_type: str = Query(...),
    entity_id: int = Query(...),
    file: UploadFile = File(...)
):
    """Upload a thumbnail image to the entity."""
    try:
        result = files_logic.upload_thumbnail(entity_type, entity_id, file)
        return {"attachment_id": result}
    except Exception as e:
        log.exception("❌ Thumbnail upload failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/filmstrip")
def upload_filmstrip_thumbnail(
    entity_type: str = Query(...),
    entity_id: int = Query(...),
    file: UploadFile = File(...)
):
    """Upload a filmstrip thumbnail to the entity."""
    try:
        result = files_logic.upload_filmstrip_thumbnail(entity_type, entity_id, file)
        return {"attachment_id": result}
    except Exception as e:
        log.exception("❌ Filmstrip upload failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download")
def download_attachment_url(
    attachment_id: int = Query(...)
):
    """Get direct download URL for an attachment."""
    try:
        return files_logic.get_download_url(attachment_id)
    except Exception as e:
        log.exception("❌ Failed to get download URL")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/share-thumbnail")
def share_thumbnail(
    entities: List[Dict[str, Any]],
    source_entity: Optional[Dict[str, Any]] = None,
    filmstrip_thumbnail: bool = False,
    file: Optional[UploadFile] = File(None)
):
    """
    Share an uploaded or existing thumbnail with multiple entities.
    Either `file` or `source_entity` is required.
    """
    try:
        result = files_logic.share_thumbnail(
            entities=entities,
            file=file,
            source_entity=source_entity,
            filmstrip_thumbnail=filmstrip_thumbnail
        )
        return {"attachment_id": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        log.exception("❌ Failed to share thumbnail")
        raise HTTPException(status_code=500, detail=str(e))
