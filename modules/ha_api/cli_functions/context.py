import click
from homer.utils.logger import get_module_logger
from homeassistant_api import Context
from modules.ha_api.logic import context as context_logic

log = get_module_logger("ha_api.context.cli")

@click.group(
    name="context",
    help="🧠 Context Utilities — Inspect Home Assistant context objects"
)
def context_cmd():
    pass

@context_cmd.command("show", help="Print all details for a context object.")
@click.option("--id", "context_id", required=True, help="Context ID")
@click.option("--user-id", default=None, help="User ID")
@click.option("--parent-id", default=None, help="Parent Context ID")
def show_context(context_id, user_id, parent_id):
    try:
        ctx = Context(id=context_id, user_id=user_id, parent_id=parent_id)
        info = context_logic.to_dict(ctx)
        click.echo("🧠 Context Info:")
        for key, value in info.items():
            click.echo(f"  {key}: {value}")
    except Exception as e:
        log.exception("Failed to show context info")
        click.echo(f"❌ Error: {e}")

@context_cmd.command("is-user", help="Check if context is user-triggered.")
@click.option("--id", "context_id", required=True, help="Context ID")
@click.option("--user-id", default=None, help="User ID")
@click.option("--parent-id", default=None, help="Parent Context ID")
def is_user_context(context_id, user_id, parent_id):
    try:
        ctx = Context(id=context_id, user_id=user_id, parent_id=parent_id)
        result = context_logic.is_user_context(ctx)
        click.echo("✅ Is user-triggered." if result else "⚠️ Not a user-triggered context.")
    except Exception as e:
        log.exception("Failed to evaluate user context")
        click.echo(f"❌ Error: {e}")

@context_cmd.command("get", help="Get a specific field from context.")
@click.option("--field", required=True, type=click.Choice(["id", "user_id", "parent_id"]), help="Field to retrieve.")
@click.option("--id", "context_id", required=True, help="Context ID")
@click.option("--user-id", default=None, help="User ID")
@click.option("--parent-id", default=None, help="Parent Context ID")
def get_field(field, context_id, user_id, parent_id):
    try:
        ctx = Context(id=context_id, user_id=user_id, parent_id=parent_id)
        value = {
            "id": context_logic.get_context_id,
            "user_id": context_logic.get_user_id,
            "parent_id": context_logic.get_parent_id
        }[field](ctx)
        click.echo(f"{field}: {value}")
    except Exception as e:
        log.exception("Failed to get field from context")
        click.echo(f"❌ Error: {e}")
