
import json
import click
from typing import Optional

from modules.netbox.cli_functions.dcim import devices as device_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.cli.dcim.devices")


@click.group("devices")
def cli():
    """Commands for managing NetBox devices."""
    pass


@cli.command("all")
@click.option("--limit", default=0, help="Max number of devices to fetch.")
@click.option("--offset", default=None, type=int, help="Offset for pagination.")
def get_all(limit: int, offset: Optional[int]):
    """Fetch all devices."""
    records = device_logic.get_all_devices(limit=limit, offset=offset)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("get")
@click.option("--id", type=int, help="Device ID to retrieve.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def get_device(id: Optional[int], filters):
    """Fetch a single device by ID or filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    device = device_logic.get_device(id=id, **kwargs)
    if device:
        click.echo(json.dumps(dict(device), indent=2))
    else:
        click.echo("Device not found", err=True)


@cli.command("filter")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def filter_devices(filters):
    """Filter devices using NetBox query parameters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    results = device_logic.filter_devices(**kwargs)
    click.echo(json.dumps([dict(r) for r in results], indent=2))


@cli.command("count")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def count_devices(filters):
    """Count devices matching filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    count = device_logic.count_devices(**kwargs)
    click.echo(f"{count} device(s)")


@cli.command("create")
@click.option("--data", required=True, help="JSON string or @file.json with device(s).")
def create_devices(data):
    """Create one or more devices."""
    payload = load_json_arg(data)
    created = device_logic.create_device(payload)
    if isinstance(created, list):
        click.echo(json.dumps([dict(r) for r in created], indent=2))
    else:
        click.echo(json.dumps(dict(created), indent=2))


@cli.command("update")
@click.option("--data", required=True, help="JSON string or @file.json with updates (must include ID).")
def update_devices(data):
    """Update one or more devices."""
    payload = load_json_arg(data)
    updated = device_logic.update_devices(payload)
    click.echo(json.dumps([dict(r) for r in updated], indent=2))


@cli.command("delete")
@click.option("--ids", help="Comma-separated list of device IDs to delete.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def delete_devices(ids, filters):
    """Delete devices by ID or filter."""
    if ids:
        id_list = [int(i.strip()) for i in ids.split(",")]
        result = device_logic.delete_devices(id_list)
    elif filters:
        kwargs = dict(kv.split("=", 1) for kv in filters)
        result = device_logic.delete_devices_by_filter(**kwargs)
    else:
        click.echo("Must provide either --ids or --filter", err=True)
        return
    click.echo("Devices deleted" if result else "Delete failed")


@cli.command("choices")
def device_choices():
    """Display valid choices for device fields."""
    choices = device_logic.get_device_choices()
    click.echo(json.dumps(choices, indent=2))


@cli.command("patch")
@click.argument("device_name")
@click.option("--data", required=True, help="JSON string or @file.json to patch fields.")
def patch_device(device_name, data):
    """Update fields on a single device by name."""
    payload = load_json_arg(data)
    success = device_logic.update_device_fields(device_name, payload)
    if success:
        click.echo(f"Device '{device_name}' updated")
    else:
        click.echo(f"Failed to update device '{device_name}'", err=True)


def load_json_arg(arg: str):
    """Load JSON from string or @file path."""
    if arg.startswith("@"):
        with open(arg[1:], "r") as f:
            return json.load(f)
    return json.loads(arg)
