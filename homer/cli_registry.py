# homer/cli_registry.py

import click
from typing import Dict

# CLI registry: name → click.Group
_HOMER_CLI_REGISTRY: Dict[str, click.Group] = {}

def register_cli(name: str):
    """Decorator to register a Click command group under a specific name."""
    def wrapper(group: click.Group):
        _HOMER_CLI_REGISTRY[name] = group
        return group
    return wrapper

def get_registered_clis():
    return _HOMER_CLI_REGISTRY.items()
