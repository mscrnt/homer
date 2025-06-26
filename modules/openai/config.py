from pydantic import BaseModel
from pathlib import Path
from homer.utils.config import register_module_env, write_env_example

class OpenAIEnv(BaseModel):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.7

ENV_PATH = Path(__file__).parent / ".env"

@register_module_env(
    "openai",
    env_path=str(ENV_PATH),
    schema_cls=OpenAIEnv
)
def _():
    write_env_example(OpenAIEnv, ENV_PATH.with_name(".env.example"), include_base=True)