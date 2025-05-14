

from modules.flow.utils.shotgun_action import ShotgunAction
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.actions.logic")


def handle_action_menu(url: str) -> dict:
    """
    Handle AMI-triggered calls using the ShotgunAction parser.
    Supports dispatching actions like 'package4client'.
    """
    action = ShotgunAction(url)
    sg = get_sg_client()
    log.info(f"✅ Received AMI action: {action.action}")

    result = {
        "protocol": action.protocol,
        "action": action.action,
        "entity_type": action.entity_type,
        "project": action.project,
        "user": action.user,
        "selected_ids": action.selected_ids,
        "sort": action.sort,
    }

    # 🚚 Example Action Dispatcher: Package4Client
    if action.action == "package4client":
        if action.entity_type != "Version":
            raise ValueError("package4client only supports Version entities.")
        if not action.selected_ids:
            raise ValueError("No selected_ids provided.")

        fields = ["code", "sg_path_to_frames", "sg_status_list"]
        versions = sg.find("Version", action.selected_ids_filter, fields)

        result["versions"] = versions
        log.info(f"📦 Prepared {len(versions)} version(s) for packaging preview")

    return result
