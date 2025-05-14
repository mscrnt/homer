

from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.connection.logic")


def get_server_info():
    """Return server metadata from ShotGrid."""
    sg = get_sg_client()
    return sg.info()


def get_session_token():
    """Return current API session token."""
    sg = get_sg_client()
    return sg.get_session_token()


def authenticate_user(user_login: str, user_password: str, auth_token: str = None):
    """
    Authenticate a ShotGrid HumanUser.

    Returns the user entity dict if successful.
    Raises Exception if authentication fails.
    """
    sg = get_sg_client()
    result = sg.authenticate_human_user(user_login, user_password, auth_token)
    if result is None:
        raise Exception("Authentication failed")
    return result
