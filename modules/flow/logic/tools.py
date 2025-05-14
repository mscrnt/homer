

from typing import List, Dict, Any, Optional
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.tools.logic")


def list_projects(fields: List[str] = ["id", "name"]) -> List[Dict[str, Any]]:
    """
    Retrieve all accessible ShotGrid projects with specified fields.
    """
    sg = get_sg_client()
    log.debug("📁 Fetching all accessible ShotGrid projects")
    return sg.find("Project", [], fields)


def find_project_by_name(name: str, fields: List[str] = ["id", "name"]) -> Optional[Dict[str, Any]]:
    """
    Find a single project by its name.
    """
    sg = get_sg_client()
    log.debug(f"🔍 Finding ShotGrid project with name: {name}")
    return sg.find_one("Project", [["name", "is", name]], fields)


def find_project_by_id(project_id: int, fields: List[str] = ["id", "name"]) -> Optional[Dict[str, Any]]:
    """
    Find a single project by its ID.
    """
    sg = get_sg_client()
    log.debug(f"🔍 Finding ShotGrid project with ID: {project_id}")
    return sg.find_one("Project", [["id", "is", project_id]], fields)
