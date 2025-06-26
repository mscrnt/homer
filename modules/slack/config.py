from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

class SlackEnv(BaseModel):
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str | None = None
    SLACK_SIGNING_SECRET: str | None = None
    SLACK_DEFAULT_CHANNEL: str | None = None

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "slack",
    env_path=str(ENV_PATH),
    schema_cls=SlackEnv
)
def _():
    write_env_example(SlackEnv, ENV_PATH.with_name(".env.example"), include_base=True)