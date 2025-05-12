# stacks/homer-github-atlassian/config.py


from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example
from homer.modules.github.config import GithubEnv
from homer.modules.atlassian.config import AtlassianEnv

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Optional schema used only to document all env keys for this stack
# ──────────────────────────────────────────────────────────────────────────────

class StackGithubAtlassianEnv(GithubEnv, AtlassianEnv):
    """Merged env schema for github + atlassian stack (no new keys)."""
    pass

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register only to generate a merged .env.example (not for validation)
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    name="github-atlassian",
    env_path=str(ENV_PATH),
    schema_cls=StackGithubAtlassianEnv,
)
def _():
    write_env_example(StackGithubAtlassianEnv, ENV_PATH.with_name(".env.example"), include_base=True)
