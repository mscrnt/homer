

import click
import json
from typing import Optional

from homer.utils.logger import get_module_logger
from modules.flow.logic import crud as crud_logic

log = get_module_logger("flow.crud.cli")

@click.group(
    name="crud",
    help="🛠️ CRUD operations for ShotGrid entities."
)
def crud_cmd():
    pass

@crud_cmd.command("create", help="Create a new entity.")
@click.option("--entity-type", required=True, help="Entity type to create (e.g., Shot, Asset).")
@click.option("--data", required=True, help="JSON string of field data to set.")
def create_entity(entity_type, data):
    data_dict = json.loads(data)
    result = crud_logic.create_entity(entity_type, data_dict)
    click.echo(json.dumps(result, indent=2))


@crud_cmd.command("find", help="Find entities with filters.")
@click.option("--entity-type", required=True, help="Entity type to find.")
@click.option("--filters", required=True, help="JSON list of filters.")
@click.option("--fields", default='["id", "type"]', help="JSON list of fields to return.")
@click.option("--order", default=None, help="Optional JSON list of ordering rules.")
@click.option("--limit", default=0, type=int, help="Limit the number of results.")
def find_entities(entity_type, filters, fields, order, limit):
    filters_list = json.loads(filters)
    fields_list = json.loads(fields)
    order_list = json.loads(order) if order else None
    results = crud_logic.find_entities(entity_type, filters_list, fields_list, order_list, limit)
    click.echo(json.dumps(results, indent=2))


@crud_cmd.command("find-one", help="Find one entity using filters.")
@click.option("--entity-type", required=True, help="Entity type to find.")
@click.option("--filters", required=True, help="JSON list of filters.")
@click.option("--fields", default='["id", "type"]', help="JSON list of fields to return.")
def find_one_entity(entity_type, filters, fields):
    filters_list = json.loads(filters)
    fields_list = json.loads(fields)
    result = crud_logic.find_one_entity(entity_type, filters_list, fields_list)
    click.echo(json.dumps(result, indent=2))


@crud_cmd.command("update", help="Update an entity.")
@click.option("--entity-type", required=True, help="Entity type.")
@click.option("--entity-id", required=True, type=int, help="Entity ID.")
@click.option("--data", required=True, help="JSON dict of data to update.")
@click.option("--modes", default=None, help="Optional multi-entity update modes.")
def update_entity(entity_type, entity_id, data, modes):
    data_dict = json.loads(data)
    modes_dict = json.loads(modes) if modes else None
    result = crud_logic.update_entity(entity_type, entity_id, data_dict, modes_dict)
    click.echo(json.dumps(result, indent=2))


@crud_cmd.command("delete", help="Soft-delete an entity.")
@click.option("--entity-type", required=True, help="Entity type.")
@click.option("--entity-id", required=True, type=int, help="Entity ID.")
def delete_entity(entity_type, entity_id):
    result = crud_logic.delete_entity(entity_type, entity_id)
    click.echo(f"✅ Deleted: {result}")


@crud_cmd.command("revive", help="Revive a deleted entity.")
@click.option("--entity-type", required=True, help="Entity type.")
@click.option("--entity-id", required=True, type=int, help="Entity ID.")
def revive_entity(entity_type, entity_id):
    result = crud_logic.revive_entity(entity_type, entity_id)
    click.echo(f"✅ Revived: {result}")


@crud_cmd.command("batch", help="Run batch operations.")
@click.option("--requests", required=True, help="JSON list of batch request dicts.")
def batch_operations(requests):
    batch_data = json.loads(requests)
    result = crud_logic.batch_operations(batch_data)
    click.echo(json.dumps(result, indent=2))


@crud_cmd.command("summarize", help="Summarize entity data.")
@click.option("--entity-type", required=True, help="Entity type.")
@click.option("--filters", required=True, help="JSON list of filters.")
@click.option("--summary-fields", required=True, help="JSON list of summary field dicts.")
@click.option("--grouping", default=None, help="Optional JSON list of grouping dicts.")
def summarize_entity(entity_type, filters, summary_fields, grouping):
    filters_list = json.loads(filters)
    summary_fields_list = json.loads(summary_fields)
    grouping_list = json.loads(grouping) if grouping else None
    result = crud_logic.summarize_entity(entity_type, filters_list, summary_fields_list, grouping_list)
    click.echo(json.dumps(result, indent=2))
