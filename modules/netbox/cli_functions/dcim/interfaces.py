
import json
import click
from typing import Optional

from modules.netbox.cli_functions.dcim import interfaces as interface_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.cli.dcim.interfaces")


@click.group("interfaces")
def cli():
    """Commands for managing NetBox interfaces."""
    pass


@cli.command("all")
@click.option("--limit", default=0, help="Max number of interfaces to fetch.")
@click.option("--offset", type=int, default=None, help="Offset for pagination.")
def get_all(limit, offset):
    """Fetch all interfaces."""
    records = interface_logic.get_all_interfaces(limit=limit, offset=offset)
    click.echo(json.dumps([dict(r) for r in records], indent=2))


@cli.command("get")
@click.option("--id", type=int, help="Interface ID.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def get_interface(id, filters):
    """Fetch a single interface by ID or filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    record = interface_logic.get_interface(id=id, **kwargs)
    if record:
        click.echo(json.dumps(dict(record), indent=2))
    else:
        click.echo("Interface not found", err=True)


@cli.command("filter")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def filter_interfaces(filters):
    """Filter interfaces using NetBox query parameters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    results = interface_logic.filter_interfaces(**kwargs)
    click.echo(json.dumps([dict(r) for r in results], indent=2))


@cli.command("count")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def count_interfaces(filters):
    """Count interfaces matching filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    count = interface_logic.count_interfaces(**kwargs)
    click.echo(f"{count} interface(s)")


@cli.command("create")
@click.option("--data", required=True, help="JSON string or @file.json with interfaces.")
def create_interfaces(data):
    """Create one or more interfaces."""
    payload = load_json_arg(data)
    created = interface_logic.create_interface(payload)
    if isinstance(created, list):
        click.echo(json.dumps([dict(r) for r in created], indent=2))
    else:
        click.echo(json.dumps(dict(created), indent=2))


@cli.command("update")
@click.option("--data", required=True, help="JSON string or @file.json with updates (must include ID).")
def update_interfaces(data):
    """Update one or more interfaces."""
    payload = load_json_arg(data)
    updated = interface_logic.update_interfaces(payload)
    click.echo(json.dumps([dict(r) for r in updated], indent=2))


@cli.command("delete")
@click.option("--ids", help="Comma-separated list of interface IDs to delete.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def delete_interfaces(ids, filters):
    """Delete interfaces by ID list or filter."""
    if ids:
        id_list = [int(i.strip()) for i in ids.split(",")]
        result = interface_logic.delete_interfaces(id_list)
    elif filters:
        kwargs = dict(kv.split("=", 1) for kv in filters)
        result = interface_logic.delete_interfaces_by_filter(**kwargs)
    else:
        click.echo("Must provide either --ids or --filter", err=True)
        return
    click.echo("Interfaces deleted" if result else "Delete failed")


@cli.command("choices")
def interface_choices():
    """Display valid choices for interface fields."""
    choices = interface_logic.get_interface_choices()
    click.echo(json.dumps(choices, indent=2))


@cli.command("patch")
@click.argument("interface_name")
@click.option("--device", required=True, help="Device name for the interface.")
@click.option("--data", required=True, help="JSON string or @file.json to patch fields.")
def patch_interface(interface_name, device, data):
    """Update fields on a single interface of a specific device."""
    payload = load_json_arg(data)
    success = interface_logic.update_interface_fields(interface_name, device, payload)
    if success:
        click.echo(f"Interface '{interface_name}' on device '{device}' updated")
    else:
        click.echo(f"Failed to update interface '{interface_name}' on '{device}'", err=True)


@cli.command("assign-ip")
@click.argument("ip_id", type=int)
@click.argument("interface_name")
@click.option("--device", required=True, help="Device name to locate the interface.")
def assign_ip(ip_id, interface_name, device):
    """Assign IP (by ID) to interface on given device."""
    from modules.netbox.cli_functions.ipam import ip_addresses

    ip = ip_addresses.get_ip(id=ip_id)
    iface = interface_logic.get_interface(name=interface_name, device=device)

    if not ip or not iface:
        click.echo("Failed to resolve IP or Interface", err=True)
        return

    result = interface_logic.assign_ip_to_interface(ip_record=ip, interface=iface)
    click.echo("IP assigned" if result else "Failed to assign IP")


def load_json_arg(arg: str):
    """Load JSON from a string or @file path."""
    if arg.startswith("@"):
        with open(arg[1:], "r") as f:
            return json.load(f)
    return json.loads(arg)
