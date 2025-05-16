# cli_functions/actions.py

import click
from homer.utils.logger import get_module_logger
from modules.example.logic import actions as action_logic

log = get_module_logger("example.actions.cli")

@click.group(
    name="actions",
    help="🧠 Example Actions — Run triggerable module actions (e.g., notifyUser)"
)
def actions_cmd():
    pass

@actions_cmd.command("trigger", help="Run an action based on a query string.")
@click.option("--action", required=True, help="The action query string to execute.")
def run_action_trigger(action):
    """CLI handler to parse and execute actions."""
    try:
        result = action_logic.handle_action_trigger(action)
        click.echo("✅ Action executed successfully:")
        click.echo(result)
    except ValueError as ve:
        click.echo(f"⚠️ Invalid request: {ve}")
    except Exception as e:
        log.exception("❌ Failed to handle action from CLI")
        click.echo(f"❌ Internal error: {e}")
