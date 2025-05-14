# modules/github/config.py


from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Schema for Github environment variables
# ──────────────────────────────────────────────────────────────────────────────

class GithubEnv(BaseModel):
    GH_TOKEN: str | None = None
    REPO_URL: str | None = None
    GITHUB_API_URL: str | None = None

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register this module's .env file and validation schema
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "github",
    env_path=str(ENV_PATH),
    schema_cls=GithubEnv
)
def _():
    """This noop function triggers registration at import time."""
    write_env_example(GithubEnv, ENV_PATH.with_name(".env.example"), include_base=True)
