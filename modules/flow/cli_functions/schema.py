#!/usr/bin/env python3



import click
from homer.utils.logger import get_module_logger
from modules.flow.logic import schema as schema_logic

log = get_module_logger("flow.schema.cli")

@click.group(help="🔍 ShotGrid schema inspection commands")
def schema_cmd():
    pass

@schema_cmd.command("entities", help="List all ShotGrid entity types and display names.")
def list_entity_types():
    try:
        data = schema_logic.get_entity_types()
        click.echo("📘 Entity Types:")
        for entity, meta in data.items():
            click.echo(f"  {entity}: {meta.get('name')}")
    except Exception as e:
        log.exception("❌ Failed to list entity types")
        click.echo(f"❌ Error: {e}")

@schema_cmd.command("fields", help="List all fields for a given ShotGrid entity.")
@click.argument("entity")
def list_entity_fields(entity):
    try:
        fields = schema_logic.get_entity_fields(entity)
        click.echo(f"📘 Fields for {entity}:")
        for name, meta in fields.items():
            label = meta.get("name", "(no label)")
            data_type = meta.get("data_type", "unknown")
            click.echo(f"  {name} ({data_type}): {label}")
    except Exception as e:
        log.exception(f"❌ Failed to list fields for {entity}")
        click.echo(f"❌ Error: {e}")
