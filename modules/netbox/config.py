
from pydantic import BaseModel, HttpUrl, SecretStr
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 🌐 Schema for NetBox environment variables
# ──────────────────────────────────────────────────────────────────────────────

class NetboxEnv(BaseModel):
    NETBOX_URL: HttpUrl               # e.g. http://localhost:8000
    NETBOX_TOKEN: SecretStr           # API token with access rights to NetBox

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register this module's .env file and validation schema
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "netbox",
    env_path=str(ENV_PATH),
    schema_cls=NetboxEnv
)
def _():
    """This noop function triggers registration at import time."""
    write_env_example(NetboxEnv, ENV_PATH.with_name(".env.example"), include_base=True)
