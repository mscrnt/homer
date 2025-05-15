
import json
import click
from typing import Optional

from modules.netbox.cli_functions.dcim import racks as rack_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.cli.dcim.racks")


@click.group("racks")
def cli():
    """Commands for managing NetBox racks."""
    pass


@cli.command("all")
@click.option("--limit", default=0, help="Max number of racks to fetch.")
@click.option("--offset", type=int, default=None, help="Offset for pagination.")
def get_all(limit, offset):
    """Fetch all racks."""
    records = rack_logic.get_all_racks(limit=limit, offset=offset)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("get")
@click.option("--id", type=int, help="Rack ID.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def get_rack(id, filters):
    """Fetch a single rack by ID or filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    record = rack_logic.get_rack(id=id, **kwargs)
    if record:
        click.echo(json.dumps(dict(record), indent=2))
    else:
        click.echo("Rack not found", err=True)


@cli.command("filter")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def filter_racks(filters):
    """Filter racks using NetBox query parameters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    results = rack_logic.filter_racks(**kwargs)
    click.echo(json.dumps([dict(r) for r in results], indent=2))


@cli.command("count")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def count_racks(filters):
    """Count racks matching filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    count = rack_logic.count_racks(**kwargs)
    click.echo(f"{count} rack(s)")


@cli.command("create")
@click.option("--data", required=True, help="JSON string or @file.json with racks.")
def create_racks(data):
    """Create one or more racks."""
    payload = load_json_arg(data)
    created = rack_logic.create_rack(payload)
    if isinstance(created, list):
        click.echo(json.dumps([dict(r) for r in created], indent=2))
    else:
        click.echo(json.dumps(dict(created), indent=2))


@cli.command("update")
@click.option("--data", required=True, help="JSON string or @file.json with updates (must include ID).")
def update_racks(data):
    """Update one or more racks."""
    payload = load_json_arg(data)
    updated = rack_logic.update_racks(payload)
    click.echo(json.dumps([dict(r) for r in updated], indent=2))


@cli.command("delete")
@click.option("--ids", help="Comma-separated list of rack IDs to delete.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def delete_racks(ids, filters):
    """Delete racks by ID list or filter."""
    if ids:
        id_list = [int(i.strip()) for i in ids.split(",")]
        result = rack_logic.delete_racks(id_list)
    elif filters:
        kwargs = dict(kv.split("=", 1) for kv in filters)
        result = rack_logic.delete_racks_by_filter(**kwargs)
    else:
        click.echo("Must provide either --ids or --filter", err=True)
        return
    click.echo("Racks deleted" if result else "Delete failed")


@cli.command("choices")
def rack_choices():
    """Display valid choices for rack fields."""
    choices = rack_logic.get_rack_choices()
    click.echo(json.dumps(choices, indent=2))


@cli.command("patch")
@click.argument("rack_name")
@click.option("--site", required=True, help="Site name for the rack.")
@click.option("--data", required=True, help="JSON string or @file.json to patch fields.")
def patch_rack(rack_name, site, data):
    """Update fields on a single rack identified by name and site."""
    payload = load_json_arg(data)
    success = rack_logic.update_rack_fields(rack_name, site, payload)
    if success:
        click.echo(f"Rack '{rack_name}' at site '{site}' updated")
    else:
        click.echo(f"Failed to update rack '{rack_name}' at site '{site}'", err=True)


def load_json_arg(arg: str):
    """Load JSON from a string or @file path."""
    if arg.startswith("@"):
        with open(arg[1:], "r") as f:
            return json.load(f)
    return json.loads(arg)
