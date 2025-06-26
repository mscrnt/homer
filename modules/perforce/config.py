from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

class PerforceEnv(BaseModel):
    P4PORT: str
    P4USER: str
    P4CLIENT: str | None = None
    P4PASSWD: str | None = None
    P4TRUST: str | None = None

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "perforce",
    env_path=str(ENV_PATH),
    schema_cls=PerforceEnv
)
def _():
    write_env_example(PerforceEnv, ENV_PATH.with_name(".env.example"), include_base=True)