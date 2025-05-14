

from typing import Optional, Dict, Any, List
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.shots.logic")


def get_shots_by_project_name(project: str) -> Dict[str, Any]:
    sg = get_sg_client()
    filters = [["project.Project.name", "is", project]]
    fields = ["code", "sg_sequence.Sequence.sg_status_list"]
    log.debug(f"🔍 Looking up shots for project: {project}")
    result = sg.find("Shot", filters, fields)
    return {"project": project, "shots": result}


def get_shot_by_id(shot_id: int) -> Dict[str, Any]:
    sg = get_sg_client()
    log.debug(f"🔍 Retrieving Shot by ID: {shot_id}")
    result = sg.find_one("Shot", [["id", "is", shot_id]])
    if not result:
        raise ValueError("Shot not found")
    return result


def create_shot(
    project_id: int,
    code: str,
    description: Optional[str] = None,
    sg_status_list: Optional[str] = None,
    task_template_id: Optional[int] = None
) -> Dict[str, Any]:
    sg = get_sg_client()
    data = {
        "project": {"type": "Project", "id": project_id},
        "code": code,
    }
    if description:
        data["description"] = description
    if sg_status_list:
        data["sg_status_list"] = sg_status_list
    if task_template_id:
        data["task_template"] = {"type": "TaskTemplate", "id": task_template_id}

    log.info(f"🛠️ Creating Shot: {code} for Project ID {project_id}")
    return sg.create("Shot", data)


def update_shot(shot_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
    sg = get_sg_client()
    log.info(f"✏️ Updating Shot {shot_id} with: {updates}")
    return sg.update("Shot", shot_id, updates)


def delete_shot(shot_id: int) -> bool:
    sg = get_sg_client()
    log.warning(f"🗑️ Deleting Shot {shot_id}")
    return sg.delete("Shot", shot_id)
