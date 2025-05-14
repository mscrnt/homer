from typing import Optional, Dict, Any
from homeassistant_api import Context


# ──────────────────────────────────────────────────────────────────────────────
# 🧠 Context Utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_context_id(ctx: Context) -> str:
    """
    Returns the unique ID of the context.
    """
    return ctx.id


def get_user_id(ctx: Context) -> Optional[str]:
    """
    Returns the user ID tied to the context, if any.
    """
    return ctx.user_id


def get_parent_id(ctx: Context) -> Optional[str]:
    """
    Returns the parent context ID, if any.
    """
    return ctx.parent_id


def is_user_context(ctx: Context) -> bool:
    """
    Returns True if the context was initiated by a known user.
    """
    return bool(ctx.user_id)


def to_dict(ctx: Context) -> Dict[str, Any]:
    """
    Serializes a Context object into a dictionary.
    """
    return {
        "id": ctx.id,
        "parent_id": ctx.parent_id,
        "user_id": ctx.user_id,
    }
