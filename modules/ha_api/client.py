from datetime import timedelta
from typing import Optional
import os

from homeassistant_api import Client
from modules.ha_api.config import HomeAssistantEnv

# Optional persistent cache backends
from requests_cache import CachedSession
from aiohttp_client_cache import CachedSession as AioCachedSession
from aiohttp_client_cache.backends.filesystem import FileBackend


def get_env(required: bool = False, safe: bool = False) -> Optional[HomeAssistantEnv]:
    try:
        env = HomeAssistantEnv(**os.environ)
        if required and (not env.HA_API_URL or not env.HA_API_TOKEN):
            raise ValueError("HA_API_URL and HA_API_TOKEN are required but missing.")
        return env
    except Exception:
        if safe:
            return None
        raise

def build_client(use_async: bool = False) -> Client:
    """
    Constructs a Home Assistant Client with optional persistent caching.
    """
    env = get_env()

    token = env.HA_API_TOKEN.get_secret_value()
    url = env.HA_API_URL

    if use_async:
        session = AioCachedSession(
            cache=FileBackend(
                cache_name=".homer_ha_api_cache_async",
                expire_after=timedelta(minutes=5)
            )
        )
        return Client(url, token, use_async=True, cache_session=session)
    else:
        session = CachedSession(
            cache_name=".homer_ha_api_cache",
            backend="filesystem",
            expire_after=timedelta(minutes=5)
        )
        return Client(url, token, cache_session=session)
