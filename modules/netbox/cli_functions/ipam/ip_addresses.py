
import json
import click
from typing import Optional

from modules.netbox.cli_functions.ipam import ip_addresses as ip_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.cli.ipam.ip_addresses")


@click.group("ip-addresses")
def cli():
    """Manage IP addresses in NetBox."""
    pass


@cli.command("all")
@click.option("--limit", default=0, help="Max number of IPs to fetch.")
@click.option("--offset", type=int, default=None, help="Offset for pagination.")
def get_all(limit, offset):
    """Fetch all IP addresses."""
    records = ip_logic.get_all_ip_addresses(limit=limit, offset=offset)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("get")
@click.option("--id", type=int, help="IP address ID.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def get_ip(id, filters):
    """Fetch a single IP address by ID or filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    record = ip_logic.get_ip_address(id=id, **kwargs)
    if record:
        click.echo(json.dumps(dict(record), indent=2))
    else:
        click.echo("IP address not found", err=True)


@cli.command("filter")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def filter_ips(filters):
    """Filter IP addresses."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    records = ip_logic.filter_ip_addresses(**kwargs)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("count")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def count_ips(filters):
    """Count IP addresses matching filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    count = ip_logic.count_ip_addresses(**kwargs)
    click.echo(f"{count} IP address(es)")


@cli.command("create")
@click.option("--data", required=True, help="JSON string or @file.json")
def create_ips(data):
    """Create one or more IP addresses."""
    payload = load_json_arg(data)
    created = ip_logic.create_ip_address(payload)
    if isinstance(created, list):
        click.echo(json.dumps([dict(r) for r in created], indent=2))
    else:
        click.echo(json.dumps(dict(created), indent=2))


@cli.command("update")
@click.option("--data", required=True, help="JSON string or @file.json")
def update_ips(data):
    """Update one or more IP addresses (must include ID)."""
    payload = load_json_arg(data)
    updated = ip_logic.update_ip_addresses(payload)
    click.echo(json.dumps([dict(r) for r in updated], indent=2))


@cli.command("delete")
@click.option("--ids", help="Comma-separated list of IP address IDs.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def delete_ips(ids, filters):
    """Delete IP addresses by ID or filters."""
    if ids:
        id_list = [int(i.strip()) for i in ids.split(",")]
        result = ip_logic.delete_ip_addresses(id_list)
    elif filters:
        kwargs = dict(kv.split("=", 1) for kv in filters)
        result = ip_logic.delete_ip_addresses_by_filter(**kwargs)
    else:
        click.echo("Must provide either --ids or --filter", err=True)
        return
    click.echo("IP addresses deleted" if result else "Delete failed")


@cli.command("choices")
def ip_choices():
    """Show available field choices for IPs."""
    choices = ip_logic.get_ip_address_choices()
    click.echo(json.dumps(choices, indent=2))


@cli.command("patch")
@click.argument("address")
@click.option("--data", required=True, help="JSON string or @file.json")
def patch_ip(address, data):
    """Patch a single IP address by address string."""
    payload = load_json_arg(data)
    success = ip_logic.update_ip_address_fields(address, payload)
    if success:
        click.echo(f"IP address '{address}' updated")
    else:
        click.echo(f"Failed to update IP address '{address}'", err=True)


def load_json_arg(arg: str):
    """Load JSON from inline or @filename.json"""
    if arg.startswith("@"):
        with open(arg[1:], "r") as f:
            return json.load(f)
    return json.loads(arg)
