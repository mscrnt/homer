

from pydantic import BaseModel, HttpUrl
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Schema for Flow (ShotGrid) environment variables
# ──────────────────────────────────────────────────────────────────────────────

class FlowEnv(BaseModel):
    SG_SITE: HttpUrl                   # e.g. https://yourstudio.shotgrid.autodesk.com
    SG_SCRIPT_NAME: str               # Your script name registered in ShotGrid
    SG_API_KEY: str                   # Your ShotGrid script API key

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register this module's .env file and validation schema
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "flow",
    env_path=str(ENV_PATH),
    schema_cls=FlowEnv
)
def _():
    """This noop function triggers registration at import time."""
    write_env_example(FlowEnv, ENV_PATH.with_name(".env.example"), include_base=True)
