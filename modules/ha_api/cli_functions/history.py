import click
from datetime import datetime
from modules.ha_api.logic import client as client_logic
from modules.ha_api.logic import history as history_logic
from modules.ha_api.logic import entity as entity_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.history.cli")

@click.group(
    name="history",
    help="📚 History — Inspect historical state changes of Home Assistant entities"
)
def history_cmd():
    pass

@history_cmd.command("first", help="Show the first historical state of an entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. light.kitchen)")
def first_state(entity_id):
    try:
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return

        hist = entity_logic.get_history(entity)
        state = history_logic.get_first_state(hist)
        click.echo(f"🕘 First state for {entity_id}: {state.state} @ {state.last_changed}")
    except Exception as e:
        log.exception("Failed to get first state")
        click.echo(f"❌ Error: {e}")

@history_cmd.command("last", help="Show the last historical state of an entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. sensor.cpu_temp)")
def last_state(entity_id):
    try:
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return

        hist = entity_logic.get_history(entity)
        state = history_logic.get_last_state(hist)
        click.echo(f"🕓 Last state for {entity_id}: {state.state} @ {state.last_changed}")
    except Exception as e:
        log.exception("Failed to get last state")
        click.echo(f"❌ Error: {e}")

@history_cmd.command("all", help="Show all historical states of an entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. switch.heater)")
def all_states(entity_id):
    try:
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return

        hist = entity_logic.get_history(entity)
        states = history_logic.get_all_states(hist)
        click.echo(f"📘 Found {len(states)} states for {entity_id}:")
        for state in states:
            click.echo(f"- {state.state} @ {state.last_changed}")
    except Exception as e:
        log.exception("Failed to list all states")
        click.echo(f"❌ Error: {e}")
