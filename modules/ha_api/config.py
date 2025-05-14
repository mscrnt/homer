from pathlib import Path
from typing import Optional
from pydantic import BaseModel, HttpUrl, SecretStr

from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 🔌 Schema for Home Assistant environment variables
# ──────────────────────────────────────────────────────────────────────────────

class HomeAssistantEnv(BaseModel):
    """Environment schema for Home Assistant CLI integration."""

    HA_API_URL: Optional[HttpUrl] = None
    HA_API_TOKEN: Optional[SecretStr] = None
    HA_WS_URL: Optional[HttpUrl] = None
    HA_ENABLE_CACHE: bool = False

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register this module's .env file and validation schema
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "ha_api",
    env_path=str(ENV_PATH),
    schema_cls=HomeAssistantEnv
)
def _():
    """Triggers registration of the HA module config at import time."""
    write_env_example(HomeAssistantEnv, ENV_PATH.with_name(".env.example"), include_base=True)
