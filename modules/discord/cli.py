#!/usr/bin/env python3

import click
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from modules.example.logic import connection as conn_logic  # 🔗 Example logic

# 🧩 Optional: Import subcommand groups
# These should be defined in `cli_functions/<feature>.py`
from modules.example.cli_functions.connection import connection_cmd
from modules.example.cli_functions.actions import actions_cmd

log = get_module_logger("example")

# 🧠 Register the CLI group for this module
@register_cli("example")
@click.group(
    help="🧪 Example CLI — Commands for the example module",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

# 🔌 Register CLI subcommands or groups
cli.add_command(connection_cmd)
cli.add_command(actions_cmd)

# ──────────────────────────────────────────────────────────────────────────────
# 🩺 Ping (Health Check)
# ──────────────────────────────────────────────────────────────────────────────
@cli.command("ping", help="Ping the Example server and return version info.")
def cli_ping():
    try:
        info = conn_logic.get_server_info()
        version = info.get("version", "unknown")
        click.echo(f"✅ Example service is responsive. Version: {version}")
    except Exception:
        click.echo("❌ Ping failed.")
        log.exception("Ping error")
