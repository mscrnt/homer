# stacks/example-another/config.py

from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example
from homer.modules.example.config import ExampleEnv
from homer.modules.another_module.config import AnotherModuleEnv

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Optional: Combined env schema for this stack (for .env.example only)
# ──────────────────────────────────────────────────────────────────────────────

class StackExampleAnotherEnv(ExampleEnv, AnotherModuleEnv):
    """Merged env schema for example + another_module stack (no new keys)."""
    pass

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register only to generate a merged .env.example (not for validation)
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    name="example-another",
    env_path=str(ENV_PATH),
    schema_cls=StackExampleAnotherEnv,
)
def _():
    write_env_example(StackExampleAnotherEnv, ENV_PATH.with_name(".env.example"), include_base=True)
