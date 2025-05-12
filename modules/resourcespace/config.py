# modules/resourcespace/config.py


from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 📦 Schema for ResourceSpace environment variables
# ──────────────────────────────────────────────────────────────────────────────

class ResourceSpaceEnv(BaseModel):
    RS_API_URL: str | None = None       # e.g. https://rs.example.com/api
    RS_API_USER: str | None = None      # e.g. admin
    RS_API_KEY: str | None = None       # e.g. user's private API key

# ──────────────────────────────────────────────────────────────────────────────
# 🔧 Register this module's .env file and validation schema
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "resourcespace",
    env_path=str(ENV_PATH),
    schema_cls=ResourceSpaceEnv
)
def _():
    """This noop function triggers registration at import time."""
    write_env_example(ResourceSpaceEnv, ENV_PATH.with_name(".env.example"), include_base=True)
