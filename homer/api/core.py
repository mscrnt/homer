# homer/api/core.py

from fastapi import APIRouter
from typing import List, Type

class HomerAPI:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.router = APIRouter(prefix=prefix)
        self.register_routes()

    def register_routes(self):
        raise NotImplementedError("Modules must implement register_routes()")

# Global registry
_HOMER_API_REGISTRY: List[HomerAPI] = []

def register_api(cls: Type[HomerAPI]):
    """Decorator to auto-register API classes."""
    instance = cls()
    _HOMER_API_REGISTRY.append(instance)
    return cls

def get_registered_apis() -> List[HomerAPI]:
    return _HOMER_API_REGISTRY
