#!/usr/bin/env python3


import click
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger

log = get_module_logger("netbox")

# ──────────────────────────────────────────────────────────────────────────────
# 📡 CLI Group Registration
# ──────────────────────────────────────────────────────────────────────────────

@register_cli("netbox")
@click.group(
    help="📡 netbox CLI — NetBox integration commands",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    """NetBox CLI entrypoint."""
    pass

# ──────────────────────────────────────────────────────────────────────────────
# 🩺 Ping (Server Health Check)
# ──────────────────────────────────────────────────────────────────────────────

@cli.command("ping", help="Ping the NetBox server and return version info.")
def cli_ping():
    try:
        from modules.netbox.client import get_netbox_client
        nb = get_netbox_client()
        version = nb.version
        click.echo(f"✅ NetBox is responsive. Server version: {version}")
    except Exception:
        click.echo("❌ Ping failed.")
        log.exception("Ping error")

# ──────────────────────────────────────────────────────────────────────────────
# 📦 CLI Subcommand Registration
# ──────────────────────────────────────────────────────────────────────────────

# DCIM
from modules.netbox.cli_functions.dcim.devices import cli as devices_cli
from modules.netbox.cli_functions.dcim.interfaces import cli as interfaces_cli
from modules.netbox.cli_functions.dcim.racks import cli as racks_cli

cli.add_command(devices_cli)
cli.add_command(interfaces_cli)
cli.add_command(racks_cli)

# IPAM
from modules.netbox.cli_functions.ipam.ip_addresses import cli as ip_addresses_cli
from modules.netbox.cli_functions.ipam.prefixes import cli as prefixes_cli

cli.add_command(ip_addresses_cli)
cli.add_command(prefixes_cli)

# Tenancy
from modules.netbox.cli_functions.tenancy.tenants import cli as tenants_cli

cli.add_command(tenants_cli)

# Utilities
from modules.netbox.cli_functions import utils as utils_cli

cli.add_command(utils_cli.cli)