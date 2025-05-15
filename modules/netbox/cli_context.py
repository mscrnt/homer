
import click
import functools
from modules.netbox.client import get_netbox_client


class NetboxContext:
    """Encapsulates pynetbox client and dynamic endpoint resolution."""
    def __init__(self):
        self.client = get_netbox_client()

    def resolve_endpoint(self, path: str):
        """
        Resolve a dotted endpoint path (e.g., 'ipam.prefixes') to pynetbox endpoint.
        """
        obj = self.client
        for part in path.strip().split("."):
            obj = getattr(obj, part)
        return obj


def pass_netbox_context(func):
    """Injects a NetboxContext instance into the CLI function."""
    @click.pass_context
    @functools.wraps(func)
    def wrapper(click_ctx, *args, **kwargs):
        ctx = NetboxContext()
        return func(ctx, *args, **kwargs)
    return wrapper
