import click
from modules.ha_api.logic import client as client_logic
from modules.ha_api.logic import logbook as logbook_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.logbook.cli")

@click.group(
    name="logbook",
    help="📓 Logbook — View Home Assistant log entries"
)
def logbook_cmd():
    pass

@logbook_cmd.command("list", help="List recent logbook entries.")
@click.option("--limit", default=10, help="Number of log entries to display.")
def list_entries(limit):
    try:
        entries = list(client_logic.get_logbook_entries())
        click.echo(f"🗒️ Showing {min(len(entries), limit)} of {len(entries)} log entries:")
        for entry in entries[:limit]:
            info = logbook_logic.describe_entry(entry)
            click.echo(f"- [{info['timestamp']}] {info['name']}: {info['message'] or '[no message]'}")
    except Exception as e:
        log.exception("Failed to list logbook entries")
        click.echo(f"❌ Error: {e}")

@logbook_cmd.command("filter", help="List logbook entries for a specific entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. light.kitchen)")
@click.option("--limit", default=10, help="Maximum number of entries to display.")
def filter_by_entity(entity_id, limit):
    try:
        entries = [
            entry for entry in client_logic.get_logbook_entries()
            if logbook_logic.is_entity_entry(entry, entity_id)
        ]
        click.echo(f"📘 Showing {min(len(entries), limit)} entries for {entity_id}:")
        for entry in entries[:limit]:
            info = logbook_logic.describe_entry(entry)
            click.echo(f"- [{info['timestamp']}] {info['name']}: {info['message'] or '[no message]'}")
    except Exception as e:
        log.exception("Failed to filter logbook entries")
        click.echo(f"❌ Error: {e}")

@logbook_cmd.command("messages", help="Show only log entries that include messages.")
@click.option("--limit", default=10, help="Max entries to display.")
def only_messages(limit):
    try:
        entries = [
            entry for entry in client_logic.get_logbook_entries()
            if logbook_logic.has_message(entry)
        ]
        click.echo(f"💬 Showing {min(len(entries), limit)} log entries with messages:")
        for entry in entries[:limit]:
            info = logbook_logic.describe_entry(entry)
            click.echo(f"- [{info['timestamp']}] {info['name']}: {info['message']}")
    except Exception as e:
        log.exception("Failed to fetch message-only log entries")
        click.echo(f"❌ Error: {e}")
