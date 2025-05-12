from ..client import call_api
from typing import List
from json import dumps

def get_users(find: str = "", exact_username_match: bool = False) -> dict:
    """Retrieve users matching a string (partial or exact match)."""
    return call_api("get_users", {
        "param1": find,
        "param2": str(int(exact_username_match))
    })


def get_users_by_permission(permissions: List[str]) -> dict:
    """Get users that belong to a group with the specified permissions (must have all)."""
    return call_api("get_users_by_permission", {
        "param1": dumps(permissions)
    })


def mark_email_as_invalid(email: str) -> dict:
    """Mark an email address as invalid across all user accounts."""
    return call_api("mark_email_as_invalid", {
        "param1": email
    })


def login(username: str, password: str) -> dict:
    """Attempt to log in and retrieve a session API key."""
    return call_api("login", {
        "param1": username,
        "param2": password
    })


def checkperm(perm: str) -> dict:
    """Check whether the current user has the given permission string."""
    return call_api("checkperm", {
        "param1": perm
    })
