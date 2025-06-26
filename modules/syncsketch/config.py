from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

class SyncSketchEnv(BaseModel):
    SYNCSKETCH_API_KEY: str
    SYNCSKETCH_WORKSPACE: str
    SYNCSKETCH_BASE_URL: str = "https://syncsketch.com/api/v1"

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "syncsketch",
    env_path=str(ENV_PATH),
    schema_cls=SyncSketchEnv
)
def _():
    write_env_example(SyncSketchEnv, ENV_PATH.with_name(".env.example"), include_base=True)