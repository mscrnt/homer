# logic/actions.py

from modules.example.utils.action_parser import ExampleAction
from modules.example.client import get_example_client
from homer.utils.logger import get_module_logger

log = get_module_logger("example.actions.logic")


def handle_action_trigger(action_query: str) -> dict:
    """
    Handle incoming action trigger requests using ExampleAction parser.
    Supports dispatching custom actions (e.g., 'notifyUser', 'generateReport').
    """
    action = ExampleAction(action_query)
    client = get_example_client()

    log.info(f"✅ Received action: {action.action}")

    result = {
        "protocol": action.protocol,
        "action": action.action,
        "resource_type": action.resource_type,
        "project": action.project,
        "user": action.user,
        "selected_ids": action.selected_ids,
        "sort": action.sort,
    }

    # 🚀 Example Action Dispatcher: notifyUser
    if action.action == "notifyUser":
        if action.resource_type != "User":
            raise ValueError("notifyUser only supports User resources.")
        if not action.selected_ids:
            raise ValueError("No selected_ids provided.")

        notifications = client.send_notifications(action.selected_ids)
        result["notifications_sent"] = len(notifications)
        log.info(f"📬 Sent {len(notifications)} notifications.")

    return result
