import click
from homer.utils.logger import get_module_logger
from modules.ha_api.logic import client as client_logic
from modules.ha_api.logic import group as group_logic

log = get_module_logger("ha_api.group.cli")


@click.group(
    name="group",
    help="📦 Entity Groups — List and inspect grouped Home Assistant entities"
)
def group_cmd():
    pass


@group_cmd.command("list", help="List all groups and their entity counts.")
def list_groups():
    try:
        groups = client_logic.get_entities()
        click.echo(f"✅ Found {len(groups)} groups:")
        for group_id, group in groups.items():
            entity_count = len(group.entities)
            click.echo(f"- {group_id} ({entity_count} entities)")
    except Exception as e:
        log.exception("Failed to list groups")
        click.echo(f"❌ Error: {e}")


@group_cmd.command("entities", help="List all entities in a given group.")
@click.option("--id", "group_id", required=True, help="Group ID (e.g. light, sensor)")
def list_entities(group_id):
    try:
        groups = client_logic.get_entities()
        group = groups.get(group_id)
        if not group:
            click.echo(f"⚠️ Group not found: {group_id}")
            return

        entities = group_logic.list_entities(group)
        click.echo(f"✅ Found {len(entities)} entities in '{group_id}':")
        for entity_id, entity in entities.items():
            click.echo(f"- {entity_id}: {entity.state.state}")
    except Exception as e:
        log.exception("Failed to list entities for group")
        click.echo(f"❌ Error: {e}")


@group_cmd.command("entity", help="Get an entity from a group by slug.")
@click.option("--group", "group_id", required=True, help="Group ID (e.g. light)")
@click.option("--slug", required=True, help="Entity slug (e.g. living_room)")
def get_entity(group_id, slug):
    try:
        groups = client_logic.get_entities()
        group = groups.get(group_id)
        if not group:
            click.echo(f"⚠️ Group not found: {group_id}")
            return

        entity = group_logic.get_entity(group, slug)
        if entity:
            click.echo(f"✅ Entity: {entity.entity_id} → {entity.state.state}")
        else:
            click.echo(f"⚠️ Entity not found in group '{group_id}' with slug '{slug}'")
    except Exception as e:
        log.exception("Failed to get entity from group")
        click.echo(f"❌ Error: {e}")
