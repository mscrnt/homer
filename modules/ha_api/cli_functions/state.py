import click
from homer.utils.logger import get_module_logger
from modules.ha_api.logic import client as client_logic
from modules.ha_api.logic import state as state_logic

log = get_module_logger("ha_api.state.cli")


@click.group(
    name="state",
    help="📦 State Utilities — Inspect and query Home Assistant state objects"
)
def state_cmd():
    pass


@state_cmd.command("describe", help="Describe a given entity state.")
@click.option("--id", "entity_id", required=True, help="Entity ID to inspect (e.g. light.kitchen)")
def describe_state(entity_id):
    try:
        state = client_logic.get_state(entity_id)
        if not state:
            click.echo(f"⚠️ No state found for entity '{entity_id}'")
            return

        details = state_logic.to_dict(state)
        click.echo("✅ State Details:")
        for key, value in details.items():
            click.echo(f"{key}: {value}")

    except Exception as e:
        log.exception("Failed to describe entity state")
        click.echo(f"❌ Error: {e}")


@state_cmd.command("onoff", help="Check if state is on or off.")
@click.option("--id", "entity_id", required=True, help="Entity ID to check (e.g. switch.garage_door)")
def check_state_onoff(entity_id):
    try:
        state = client_logic.get_state(entity_id)
        if not state:
            click.echo(f"⚠️ No state found for entity '{entity_id}'")
            return

        if state_logic.is_state_on(state):
            click.echo(f"✅ {entity_id} is ON (state: {state.state})")
        elif state_logic.is_state_off(state):
            click.echo(f"🛑 {entity_id} is OFF (state: {state.state})")
        else:
            click.echo(f"ℹ️ {entity_id} is in unknown state: {state.state}")

    except Exception as e:
        log.exception("Failed to check on/off state")
        click.echo(f"❌ Error: {e}")


@state_cmd.command("attribute", help="Get a specific attribute from an entity state.")
@click.option("--id", "entity_id", required=True, help="Entity ID to inspect")
@click.option("--key", required=True, help="Attribute key to fetch")
@click.option("--default", default=None, help="Default value if key is missing")
def get_state_attribute(entity_id, key, default):
    try:
        state = client_logic.get_state(entity_id)
        if not state:
            click.echo(f"⚠️ No state found for entity '{entity_id}'")
            return

        value = state_logic.get_attribute(state, key, default)
        click.echo(f"🔑 Attribute '{key}': {value}")

    except Exception as e:
        log.exception("Failed to fetch attribute")
        click.echo(f"❌ Error: {e}")
