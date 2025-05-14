

import os
import shutil
import tempfile
from typing import Optional, Dict, List, Any
from fastapi import UploadFile
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.files.logic")


def save_temp_file(file: UploadFile) -> str:
    """Save uploaded file to a temp path and return the path."""
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        return tmp.name


def upload_file(
    entity_type: str,
    entity_id: int,
    file: UploadFile,
    field_name: Optional[str] = None,
    display_name: Optional[str] = None,
    tag_list: Optional[str] = None
) -> int:
    sg = get_sg_client()
    tmp_path = save_temp_file(file)
    try:
        result = sg.upload(entity_type, entity_id, tmp_path, field_name, display_name, tag_list)
        return result
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def upload_thumbnail(entity_type: str, entity_id: int, file: UploadFile) -> int:
    sg = get_sg_client()
    tmp_path = save_temp_file(file)
    try:
        result = sg.upload_thumbnail(entity_type, entity_id, tmp_path)
        return result
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def upload_filmstrip_thumbnail(entity_type: str, entity_id: int, file: UploadFile) -> int:
    sg = get_sg_client()
    tmp_path = save_temp_file(file)
    try:
        result = sg.upload_filmstrip_thumbnail(entity_type, entity_id, tmp_path)
        return result
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def get_download_url(attachment_id: int) -> str:
    sg = get_sg_client()
    return sg.get_attachment_download_url({"type": "Attachment", "id": attachment_id})


def share_thumbnail(
    entities: List[Dict[str, Any]],
    file: Optional[UploadFile] = None,
    source_entity: Optional[Dict[str, Any]] = None,
    filmstrip_thumbnail: bool = False
) -> int:
    sg = get_sg_client()

    if file:
        tmp_path = save_temp_file(file)
        try:
            return sg.share_thumbnail(
                entities=entities,
                thumbnail_path=tmp_path,
                filmstrip_thumbnail=filmstrip_thumbnail
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    elif source_entity:
        return sg.share_thumbnail(
            entities=entities,
            source_entity=source_entity,
            filmstrip_thumbnail=filmstrip_thumbnail
        )
    else:
        raise ValueError("Either `file` or `source_entity` must be provided for thumbnail sharing.")
