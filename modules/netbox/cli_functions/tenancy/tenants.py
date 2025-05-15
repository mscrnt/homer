
import json
import click
from typing import Optional

from modules.netbox.cli_functions.tenancy import tenants as tenant_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.cli.tenancy.tenants")


@click.group("tenants")
def cli():
    """Manage NetBox tenants."""
    pass


@cli.command("all")
@click.option("--limit", default=0, help="Limit number of tenants.")
@click.option("--offset", type=int, default=None, help="Pagination offset.")
def get_all(limit, offset):
    """Retrieve all tenants."""
    tenants = tenant_logic.get_all_tenants(limit=limit, offset=offset)
    click.echo(json.dumps([dict(t) for t in tenants], indent=2))


@cli.command("get")
@click.option("--id", type=int, help="Tenant ID.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def get_tenant(id, filters):
    """Get a tenant by ID or filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    record = tenant_logic.get_tenant(id=id, **kwargs)
    if record:
        click.echo(json.dumps(dict(record), indent=2))
    else:
        click.echo("Tenant not found", err=True)


@cli.command("filter")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def filter_tenants(filters):
    """Filter tenants by field values."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    tenants = tenant_logic.filter_tenants(**kwargs)
    click.echo(json.dumps([dict(t) for t in tenants], indent=2))


@cli.command("count")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def count_tenants(filters):
    """Count tenants matching filters."""
    kwargs = dict(kv.split("=", 1) for kv in filters)
    count = tenant_logic.count_tenants(**kwargs)
    click.echo(f"{count} tenant(s)")


@cli.command("create")
@click.option("--data", required=True, help="JSON string or @file.json")
def create(data):
    """Create one or more tenants."""
    payload = load_json_arg(data)
    result = tenant_logic.create_tenants(payload)
    if isinstance(result, list):
        click.echo(json.dumps([dict(r) for r in result], indent=2))
    else:
        click.echo(json.dumps(dict(result), indent=2))


@cli.command("update")
@click.option("--data", required=True, help="JSON string or @file.json")
def update(data):
    """Bulk update tenants."""
    updates = load_json_arg(data)
    result = tenant_logic.update_tenants(updates)
    click.echo(json.dumps([dict(r) for r in result], indent=2))


@cli.command("patch")
@click.argument("tenant_id", type=int)
@click.option("--data", required=True, help="JSON string or @file.json")
def patch(tenant_id, data):
    """Patch a single tenant by ID."""
    updates = load_json_arg(data)
    result = tenant_logic.update_tenant_fields(tenant_id, updates)
    click.echo("Tenant updated" if result else "Update failed")


@cli.command("delete")
@click.option("--ids", help="Comma-separated list of tenant IDs.")
@click.option("--filter", "filters", multiple=True, help="Filter as key=value.")
def delete(ids, filters):
    """Delete tenants by ID or filter."""
    if ids:
        id_list = [int(i.strip()) for i in ids.split(",")]
        result = tenant_logic.delete_tenants(id_list)
    elif filters:
        kwargs = dict(kv.split("=", 1) for kv in filters)
        result = tenant_logic.delete_tenants_by_filter(**kwargs)
    else:
        click.echo("Must provide --ids or --filter", err=True)
        return
    click.echo("Tenants deleted" if result else "Delete failed")


@cli.command("choices")
def choices():
    """Show available tenant choices."""
    choices = tenant_logic.get_tenant_choices()
    click.echo(json.dumps(choices, indent=2))


@cli.command("dict")
@click.argument("tenant", required=True)
def get_dict(tenant):
    """Return tenant as dict by ID or object."""
    try:
        tenant_id = int(tenant)
        record = tenant_logic.get_tenant_dict(tenant_id)
    except ValueError:
        click.echo("Provide tenant ID as integer", err=True)
        return

    if record:
        click.echo(json.dumps(record, indent=2))
    else:
        click.echo("Tenant not found", err=True)


def load_json_arg(arg: str):
    """Load JSON string or file."""
    if arg.startswith("@"):
        with open(arg[1:], "r") as f:
            return json.load(f)
    return json.loads(arg)
