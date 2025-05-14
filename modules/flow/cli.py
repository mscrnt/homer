#!/usr/bin/env python3



import click
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from modules.flow.logic import connection as conn_logic  # 🔗 Used for ping

# 🌐 CLI groups
from modules.flow.cli_functions.actions import actions_cmd
from modules.flow.cli_functions.activity import activity_cmd
from modules.flow.cli_functions.connection import connection_cmd
from modules.flow.cli_functions.crud import crud_cmd
from modules.flow.cli_functions.files import files_cmd
from modules.flow.cli_functions.playlists import playlists_cmd
from modules.flow.cli_functions.schema import schema_cmd
from modules.flow.cli_functions.shots import shots_cmd
from modules.flow.cli_functions.tasks import tasks_cmd
from modules.flow.cli_functions.versions import versions_cmd
from modules.flow.cli_functions.tools import tools_cmd

log = get_module_logger("flow")

@register_cli("flow")
@click.group(
    help="📡 Flow CLI — ShotGrid/Flow integration commands",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

# 🔌 Register all subcommands
cli.add_command(actions_cmd)
cli.add_command(activity_cmd)
cli.add_command(connection_cmd)
cli.add_command(crud_cmd)
cli.add_command(files_cmd)
cli.add_command(playlists_cmd)
cli.add_command(schema_cmd)
cli.add_command(shots_cmd)
cli.add_command(tasks_cmd)
cli.add_command(versions_cmd)
cli.add_command(tools_cmd)

# ──────────────────────────────────────────────────────────────────────────────
# 🩺 Ping (Server Health Check)
# ──────────────────────────────────────────────────────────────────────────────
@cli.command("ping", help="Ping the Flow server and return version info.")
def cli_ping():
    try:
        info = conn_logic.get_server_info()
        version = info.get("version", "unknown")
        click.echo(f"✅ Flow is responsive. Server version: {version}")
    except Exception as e:
        click.echo("❌ Ping failed.")
        log.exception("Ping error")
