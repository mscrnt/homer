

from typing import Dict, Any
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.tasks.logic")


def get_tasks_for_shot(shot_id: int) -> Dict[str, Any]:
    """
    Retrieve all Tasks linked to a specific Shot.
    """
    sg = get_sg_client()
    filters = [["entity", "is", {"type": "Shot", "id": shot_id}]]
    fields = ["content", "step.Step.short_name", "sg_status_list", "task_assignees"]

    log.debug(f"🔍 Fetching tasks for Shot ID: {shot_id}")
    tasks = sg.find("Task", filters, fields)

    return {
        "shot_id": shot_id,
        "tasks": tasks
    }
