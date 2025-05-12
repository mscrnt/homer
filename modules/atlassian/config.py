# modules/atlassian/config.py


from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Schema for Atlassian (Confluence + Jira) environment variables
# ──────────────────────────────────────────────────────────────────────────────

class AtlassianEnv(BaseModel):
    # Confluence
    CONFLUENCE_API_TOKEN: str | None = None
    CONFLUENCE_SPACE_KEY: str | None = None
    CONFLUENCE_API_URL: str | None = None

    # Jira
    JIRA_API_TOKEN: str | None = None
    JIRA_PROJECT_KEY: str | None = None
    JIRA_API_URL: str | None = None

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register this module's .env file and validation schema
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "atlassian",
    env_path=str(ENV_PATH),
    schema_cls=AtlassianEnv
)
def _():
    """This noop function triggers registration at import time."""
    write_env_example(AtlassianEnv, ENV_PATH.with_name(".env.example"), include_base=True)
