

import click
from homer.utils.logger import get_module_logger
from modules.flow.logic import actions as action_logic

log = get_module_logger("flow.actions.cli")

@click.group(
    name="actions",
    help="🧠 Flow Actions — Run AMI-style actions like 'package4client'"
)
def actions_cmd():
    pass

@actions_cmd.command("ami", help="Trigger an AMI action using a URL (e.g., package4client).")
@click.option("--url", required=True, help="The full AMI-style URL to parse and execute.")
def run_action_menu(url):
    """CLI handler to dispatch and echo AMI-style actions."""
    try:
        result = action_logic.handle_action_menu(url)
        click.echo("✅ Action executed successfully:")
        click.echo(result)
    except ValueError as ve:
        click.echo(f"⚠️ Invalid request: {ve}")
    except Exception as e:
        log.exception("❌ Failed to handle AMI action from CLI")
        click.echo(f"❌ Internal error: {e}")
