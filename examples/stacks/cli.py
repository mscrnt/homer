# stacks/example-another/cli.py

import click
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from homer.modules.example.client import fetch_records_from_example
from homer.modules.another_module.logic import push_data_to_another

log = get_module_logger("example-another")

@register_cli("example-sync")
@click.group(
    invoke_without_command=True,
    help="📦 Combined automation: Example → AnotherModule sync commands.",
    context_settings=dict(help_option_names=["-h", "--help"])
)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("🧩 HOMER Example + AnotherModule Stack CLI")
        click.echo("Use `--help` to view available commands.")
        ctx.exit(0)

@cli.command("sync-data", help="Sync data from Example to AnotherModule.")
@click.option("--project", required=True, help="Project ID or name to sync from Example.")
@click.option("--filter", default=None, help="Optional filter expression.")
def sync_data(project, filter):
    log.info(f"🔄 Fetching records from Example project: {project}")
    records = fetch_records_from_example(project, filter=filter)
    if not records:
        log.warning("⚠️ No records found.")
        return
    log.info(f"📤 Syncing {len(records)} record(s) to AnotherModule...")
    push_data_to_another(records)
    log.info("✅ Data sync complete.")
