
import json
import click
from typing import Optional
from homer.modules.netbox.logic import utils as nb_utils
from modules.netbox.cli_context import pass_netbox_context
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox.cli.utils")


@click.group("utils")
def cli():
    """Generic NetBox utility commands."""
    pass


@cli.command("all")
@click.argument("endpoint_path")
@click.option("--limit", default=0, help="Limit the number of results.")
@click.option("--offset", default=None, type=int, help="Offset for paginated results.")
@pass_netbox_context
def get_all(ctx, endpoint_path: str, limit: int, offset: Optional[int]):
    """Fetch all records from the specified NetBox endpoint."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    records = nb_utils.get_all(endpoint, limit=limit, offset=offset)
    click.echo(json.dumps([nb_utils.serialize_record(r) for r in records], indent=2))


@cli.command("get")
@click.argument("endpoint_path")
@click.option("--id", type=int, help="Object ID to retrieve.")
@click.option("--filter", "filters", multiple=True, help="Filter parameters in key=value format.")
@pass_netbox_context
def get_single(ctx, endpoint_path: str, id: Optional[int], filters):
    """Fetch a single object by ID or filters."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    kwargs = dict(kv.split("=", 1) for kv in filters)
    record = nb_utils.get_object(endpoint, id=id, **kwargs)
    if record:
        click.echo(json.dumps(nb_utils.serialize_record(record), indent=2))
    else:
        click.echo("No matching object found.", err=True)


@cli.command("filter")
@click.argument("endpoint_path")
@click.option("--filter", "filters", multiple=True, help="Filter parameters in key=value format.")
@pass_netbox_context
def filter_objects(ctx, endpoint_path: str, filters):
    """Filter records from an endpoint."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    kwargs = dict(kv.split("=", 1) for kv in filters)
    results = nb_utils.filter_objects(endpoint, **kwargs)
    click.echo(json.dumps([nb_utils.serialize_record(r) for r in results], indent=2))


@cli.command("count")
@click.argument("endpoint_path")
@click.option("--filter", "filters", multiple=True, help="Filter parameters in key=value format.")
@pass_netbox_context
def count(ctx, endpoint_path: str, filters):
    """Count records on an endpoint, optionally filtered."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    kwargs = dict(kv.split("=", 1) for kv in filters)
    count = nb_utils.count_objects(endpoint, **kwargs)
    click.echo(f"{count} record(s)")


@cli.command("create")
@click.argument("endpoint_path")
@click.option("--data", required=True, help="JSON string or @file.json with record(s) to create.")
@pass_netbox_context
def create(ctx, endpoint_path: str, data: str):
    """Create records on the specified endpoint."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    payload = load_json_arg(data)
    created = nb_utils.create_objects(endpoint, payload)
    if isinstance(created, list):
        click.echo(json.dumps([nb_utils.serialize_record(r) for r in created], indent=2))
    else:
        click.echo(json.dumps(nb_utils.serialize_record(created), indent=2))


@cli.command("update")
@click.argument("endpoint_path")
@click.option("--data", required=True, help="JSON string or @file.json with updates (must include id).")
@pass_netbox_context
def update(ctx, endpoint_path: str, data: str):
    """Update one or more records on an endpoint."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    payload = load_json_arg(data)
    updated = nb_utils.update_objects(endpoint, payload)
    click.echo(json.dumps([nb_utils.serialize_record(r) for r in updated], indent=2))


@cli.command("delete")
@click.argument("endpoint_path")
@click.option("--ids", help="Comma-separated list of IDs to delete.")
@click.option("--filter", "filters", multiple=True, help="Filter parameters in key=value format.")
@pass_netbox_context
def delete(ctx, endpoint_path: str, ids: Optional[str], filters):
    """Delete objects by ID or filter."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    if ids:
        id_list = [int(i.strip()) for i in ids.split(",")]
        result = nb_utils.delete_objects(endpoint, id_list)
    elif filters:
        kwargs = dict(kv.split("=", 1) for kv in filters)
        result = nb_utils.delete_filtered(endpoint, **kwargs)
    else:
        click.echo("Must provide either --ids or --filter", err=True)
        return
    click.echo("Delete successful" if result else "Delete failed")


@cli.command("choices")
@click.argument("endpoint_path")
@pass_netbox_context
def choices(ctx, endpoint_path: str):
    """Return available choices from an endpoint."""
    endpoint = ctx.resolve_endpoint(endpoint_path)
    result = nb_utils.get_choices(endpoint)
    click.echo(json.dumps(result, indent=2))


def load_json_arg(arg: str):
    """Load JSON from a string or file reference."""
    if arg.startswith("@"):
        with open(arg[1:], "r") as f:
            return json.load(f)
    return json.loads(arg)
