from ..client import call_api

def get_user_message(message_id: int) -> dict:
    """Retrieve a message by ID (if user has access)."""
    return call_api("get_user_message", {
        "param1": str(message_id)
    })
