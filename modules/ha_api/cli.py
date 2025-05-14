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

# ──────────────────────────────────────────────────────────────────────────────
# 🛠️ Helper Commands
# ──────────────────────────────────────────────────────────────────────────────

@cli.command("lights", help="List all light.* entities and their states")
def list_lights():
    try:
        with build_client() as client:
            states = client.get_states()
            lights = [s for s in states if s.entity_id.startswith("light.")]
            if not lights:
                click.echo("ℹ️ No lights found.")
                return
            for light in lights:
                click.echo(f"{light.entity_id} → {light.state} ({light.attributes.get('friendly_name', '-')})")
    except Exception as e:
        click.echo("❌ Failed to fetch lights.")
        log.exception("lights error")


@cli.command("domains", help="List all service domains available in Home Assistant")
def list_domains():
    try:
        with build_client() as client:
            domains = client.get_domains()
            for domain in domains:
                click.echo(f"📂 {domain}")
    except Exception as e:
        click.echo("❌ Failed to fetch domains.")
        log.exception("domains error")


@cli.command("components", help="Show all registered HA components")
def list_components():
    try:
        with build_client() as client:
            components = client.get_components()
            for component in components:
                click.echo(f"🔧 {component}")
    except Exception as e:
        click.echo("❌ Failed to fetch components.")
        log.exception("components error")


@cli.command("config", help="Show HA config info (name, version, timezone, etc)")
def get_config():
    try:
        with build_client() as client:
            config = client.get_config()
            for k, v in config.items():
                click.echo(f"{k}: {v}")
    except Exception as e:
        click.echo("❌ Failed to fetch config.")
        log.exception("config error")


@cli.command("log", help="Get latest Home Assistant error log")
def get_error_log():
    try:
        with build_client() as client:
            error_log = client.get_error_log()
            click.echo(error_log)
    except Exception as e:
        click.echo("❌ Failed to fetch error log.")
        log.exception("log error")


@cli.command("state", help="Get the state of a single entity")
@click.argument("entity_id")
def get_state(entity_id):
    try:
        with build_client() as client:
            state = client.get_state(entity_id=entity_id)
            if not state:
                click.echo(f"⚠️ No state found for: {entity_id}")
            else:
                click.echo(f"{state.entity_id} → {state.state}")
                for k, v in state.attributes.items():
                    click.echo(f"  • {k}: {v}")
    except Exception as e:
        click.echo(f"❌ Failed to get state for {entity_id}")
        log.exception("get_state error")
