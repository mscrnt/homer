from typing import Literal
from pydantic import BaseModel, Field

from homeassistant_api import AuthInvalid as HAAuthInvalid
from homeassistant_api import AuthOk as HAAuthOk
from homeassistant_api import AuthRequired as HAAuthRequired

from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.auth")


# ──────────────────────────────────────────────────────────────────────────────
# 🔐 AuthRequired Model Wrapper
# ──────────────────────────────────────────────────────────────────────────────

class AuthRequired(HAAuthRequired):
    """
    Home Assistant WebSocket initial response indicating that authentication is required.
    """
    type: Literal["auth_required"] = Field(..., description="Type of auth message.")
    ha_version: str = Field(..., description="Home Assistant version.")

    def describe(self) -> str:
        return f"🔒 Auth required for Home Assistant {self.ha_version}"


# ──────────────────────────────────────────────────────────────────────────────
# ✅ AuthOk Model Wrapper
# ──────────────────────────────────────────────────────────────────────────────

class AuthOk(HAAuthOk):
    """
    Home Assistant WebSocket response confirming that authentication succeeded.
    """
    type: Literal["auth_ok"] = Field(..., description="Type of auth message.")
    ha_version: str = Field(..., description="Home Assistant version.")

    def describe(self) -> str:
        return f"✅ Auth OK - connected to Home Assistant {self.ha_version}"


# ──────────────────────────────────────────────────────────────────────────────
# ❌ AuthInvalid Model Wrapper
# ──────────────────────────────────────────────────────────────────────────────

class AuthInvalid(HAAuthInvalid):
    """
    Home Assistant WebSocket response indicating authentication failed.
    """
    type: Literal["auth_invalid"] = Field(..., description="Type of auth message.")
    message: str = Field(..., description="Reason for authentication failure.")

    def describe(self) -> str:
        return f"❌ Auth failed: {self.message}"


# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Debug utility (optional)
# ──────────────────────────────────────────────────────────────────────────────

def log_auth_response(response: BaseModel):
    """
    Utility function to log any auth message in a standardized way.
    """
    if isinstance(response, AuthRequired):
        log.info(response.describe())
    elif isinstance(response, AuthOk):
        log.success(response.describe())
    elif isinstance(response, AuthInvalid):
        log.error(response.describe())
    else:
        log.warning(f"🌀 Unknown auth message: {response}")
