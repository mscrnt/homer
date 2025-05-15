# config.py

from pydantic import BaseModel, HttpUrl
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Environment Variable Schema (Example Module)
# ──────────────────────────────────────────────────────────────────────────────

class ExampleEnv(BaseModel):
    EXAMPLE_API_URL: HttpUrl          # e.g. https://api.example.com
    EXAMPLE_API_KEY: str              # Your API key for the Example service
    EXAMPLE_MODE: str = "demo"        # Optional mode: demo, production, etc.

# ──────────────────────────────────────────────────────────────────────────────
# 🧩 Register this module's .env file and validation schema
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "example",                         # Module name (used in logs + CLI)
    env_path=str(ENV_PATH),           # Path to the .env file
    schema_cls=ExampleEnv             # Pydantic schema for validation
)
def _():
    """Register and optionally write .env.example for the example module."""
    write_env_example(ExampleEnv, ENV_PATH.with_name(".env.example"), include_base=True)
