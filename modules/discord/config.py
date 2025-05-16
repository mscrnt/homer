from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

class DiscordEnv(BaseModel):
    DISCORD_BOT_TOKEN: str
    DISCORD_GUILD_ID: str | None = None

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "discord",
    env_path=str(ENV_PATH),
    schema_cls=DiscordEnv
)
def _():
    write_env_example(DiscordEnv, ENV_PATH.with_name(".env.example"), include_base=True)
