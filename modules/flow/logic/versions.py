

import os
import tempfile
from typing import Optional, Dict, Any
from fastapi import UploadFile
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.versions.logic")


def create_version(
    project_id: int,
    code: str,
    description: Optional[str] = None,
    sg_path_to_frames: Optional[str] = None,
    sg_status_list: Optional[str] = None,
    shot_id: Optional[int] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a new Version in ShotGrid.
    """
    sg = get_sg_client()
    data = {
        "project": {"type": "Project", "id": project_id},
        "code": code,
    }

    if description:
        data["description"] = description
    if sg_path_to_frames:
        data["sg_path_to_frames"] = sg_path_to_frames
    if sg_status_list:
        data["sg_status_list"] = sg_status_list
    if shot_id:
        data["entity"] = {"type": "Shot", "id": shot_id}
    if task_id:
        data["sg_task"] = {"type": "Task", "id": task_id}
    if user_id:
        data["user"] = {"type": "HumanUser", "id": user_id}

    log.info(f"🎞️ Creating Version: {code} for Project ID {project_id}")
    return sg.create("Version", data)


def upload_version_thumbnail(version_id: int, file: UploadFile) -> Dict[str, Any]:
    """
    Upload a thumbnail to a specific Version.
    """
    sg = get_sg_client()

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        attachment_id = sg.upload_thumbnail("Version", version_id, tmp_path)
        log.info(f"🖼️ Uploaded thumbnail for Version ID {version_id}")
        return {"version_id": version_id, "attachment_id": attachment_id}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
