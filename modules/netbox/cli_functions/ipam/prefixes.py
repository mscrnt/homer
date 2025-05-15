
import json
import click
from typing import Optional

from modules.netbox.cli_functions.ipam import prefixes as prefix_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.cli.ipam.prefixes")


@click.group("prefixes")
def cli():
    """Manage IP prefixes in NetBox."""
    pass


@cli.command("all")
@click.option("--limit", default=0, help="Limit number of prefixes.")
@click.option("--offset", type=int, default=None, help="Pagination offset.")
def get_all(limit, offset):
    """List all prefixes."""
    records = prefix_logic.get_all_prefixes(limit=limit, offset=offset)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("get")
@click.option("--id", type=int, help="Prefix ID.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def get_prefix(id, filters):
    """Get a prefix by ID or filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    record = prefix_logic.get_prefix(id=id, **kwargs)
    if record:
        click.echo(json.dumps(dict(record), indent=2))
    else:
        click.echo("Prefix not found", err=True)


@cli.command("filter")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def filter_prefixes(filters):
    """Filter prefixes by keyword arguments."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    records = prefix_logic.filter_prefixes(**kwargs)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("count")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def count_prefixes(filters):
    """Count prefixes matching filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    count = prefix_logic.count_prefixes(**kwargs)
    click.echo(f"{count} prefix(es)")


@cli.command("create")
@click.option("--data", required=True, help="JSON string or @file.json")
def create(data):
    """Create new prefix(es)."""
    payload = load_json_arg(data)
    result = prefix_logic.create_prefixes(payload)
    if isinstance(result, list):
        click.echo(json.dumps([dict(r) for r in result], indent=2))
    else:
        click.echo(json.dumps(dict(result), indent=2))


@cli.command("update")
@click.option("--data", required=True, help="JSON string or @file.json")
def update(data):
    """Update prefix records (must include IDs)."""
    payload = load_json_arg(data)
    updated = prefix_logic.update_prefixes(payload)
    click.echo(json.dumps([dict(r) for r in updated], indent=2))


@cli.command("delete")
@click.option("--ids", help="Comma-separated list of prefix IDs.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def delete(ids, filters):
    """Delete prefixes by ID or filters."""
    if ids:
        id_list = [int(i.strip()) for i in ids.split(",")]
        result = prefix_logic.delete_prefixes(id_list)
    elif filters:
        kwargs = dict(kv.split("=", 1) for kv in filters)
        result = prefix_logic.delete_prefixes_by_filter(**kwargs)
    else:
        click.echo("Must provide --ids or --filter", err=True)
        return
    click.echo("Prefixes deleted" if result else "Delete failed")


@cli.command("choices")
def choices():
    """Show available choices for prefix fields."""
    choices = prefix_logic.get_prefix_choices()
    click.echo(json.dumps(choices, indent=2))


@cli.command("available-ips")
@click.argument("prefix_id", type=int)
def list_available_ips(prefix_id):
    """List available IPs in a prefix."""
    ips = prefix_logic.get_available_ips(prefix_id)
    click.echo(json.dumps(ips, indent=2))


@cli.command("create-ips")
@click.argument("prefix_id", type=int)
@click.option("--count", default=1, help="Number of IPs to allocate.")
def create_ips(prefix_id, count):
    """Allocate new IPs from a prefix."""
    records = prefix_logic.create_available_ips(prefix_id, count)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("available-prefixes")
@click.argument("prefix_id", type=int)
def list_available_prefixes(prefix_id):
    """List available sub-prefixes."""
    prefixes = prefix_logic.get_available_child_prefixes(prefix_id)
    click.echo(json.dumps(prefixes, indent=2))


@cli.command("create-child")
@click.argument("prefix_id", type=int)
@click.option("--prefix-length", type=int, required=True, help="Length of new prefix.")
def create_child(prefix_id, prefix_length):
    """Create a child prefix from a parent."""
    new_prefix = prefix_logic.create_child_prefix(prefix_id, prefix_length)
    if new_prefix:
        click.echo(json.dumps(dict(new_prefix), indent=2))
    else:
        click.echo("Failed to create child prefix", err=True)


@cli.command("patch")
@click.argument("prefix_id", type=int)
@click.option("--data", required=True, help="JSON string or @file.json")
def patch(prefix_id, data):
    """Patch a prefix by ID."""
    updates = load_json_arg(data)
    result = prefix_logic.update_prefix_fields(prefix_id, updates)
    click.echo("Update succeeded" if result else "Update failed")


def load_json_arg(arg: str):
    """Load JSON string or file."""
    if arg.startswith("@"):
        with open(arg[1:], "r") as f:
            return json.load(f)
    return json.loads(arg)
