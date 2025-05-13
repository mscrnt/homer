# modules/flow/config.py


from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Schema for Flow nvironment variables
# ──────────────────────────────────────────────────────────────────────────────

class FlowEnv(BaseModel):
    # Confluence
    CONFLUENCE_API_TOKEN: str | None = None


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
