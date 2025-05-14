#!/usr/bin/env python3

import click
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
import modules.ha_api.config 

# Subcommand groups
from modules.ha_api.cli_functions.auth import auth_cmd
from modules.ha_api.cli_functions.client import client_cmd
from modules.ha_api.cli_functions.context import context_cmd
from modules.ha_api.cli_functions.domain import domain_cmd
from modules.ha_api.cli_functions.entity import entity_cmd
from modules.ha_api.cli_functions.event import event_cmd
from modules.ha_api.cli_functions.group import group_cmd
from modules.ha_api.cli_functions.history import history_cmd
from modules.ha_api.cli_functions.logbook import logbook_cmd
from modules.ha_api.cli_functions.response import response_cmd
from modules.ha_api.cli_functions.service import service_cmd
from modules.ha_api.cli_functions.state import state_cmd
from modules.ha_api.cli_functions.ws_client import ws_cmd

from modules.ha_api.client import build_client  

log = get_module_logger("ha_api")

@register_cli("ha_api")
@click.group(
    help="🏠 Home Assistant CLI — control and query your Home Assistant instance",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

# 🔌 Register CLI subcommands
cli.add_command(auth_cmd)
cli.add_command(client_cmd)
cli.add_command(context_cmd)
cli.add_command(domain_cmd)
cli.add_command(entity_cmd)
cli.add_command(event_cmd)
cli.add_command(group_cmd)
cli.add_command(history_cmd)
cli.add_command(logbook_cmd)
cli.add_command(response_cmd)
cli.add_command(service_cmd)
cli.add_command(state_cmd)
cli.add_command(ws_cmd)

# ──────────────────────────────────────────────────────────────────────────────
# 🩺 Ping
# ──────────────────────────────────────────────────────────────────────────────
@cli.command("ping", help="Ping the Home Assistant REST API.")
def cli_ping():
    try:
        with build_client() as client:
            if client.check_api_running():
                click.echo("✅ Home Assistant REST API is up.")
            else:
                click.echo("⚠️ API responded but may not be healthy.")
    except Exception as e:
        click.echo("❌ Ping failed.")
        log.exception("Ping error")
