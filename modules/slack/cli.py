#!/usr/bin/env python3

import click
import asyncio
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from modules.slack.client import get_slack_client
from pathlib import Path
import os

log = get_module_logger("slack")

@register_cli("slack")
@click.group(
    help="💬 Slack CLI — Commands for Slack integration",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

@cli.command("send", help="Send a message to a Slack channel")
@click.option("--channel", "-c", required=True, help="Slack channel ID or name")
@click.option("--message", "-m", required=True, help="Message to send")
@click.option("--token", help="Slack bot token (overrides env var)")
def send_message(channel: str, message: str, token: str):
    """Send a message to a Slack channel."""
    try:
        # Load environment config
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_slack_client(token)
        response = asyncio.run(client.send_message(channel, message))
        
        click.echo(f"✅ Message sent to {channel}")
        click.echo(f"📅 Timestamp: {response['ts']}")
        
    except Exception as e:
        click.echo(f"❌ Failed to send message: {e}")
        log.exception("Send message error")

@cli.command("channels", help="List available Slack channels")
@click.option("--token", help="Slack bot token (overrides env var)")
def list_channels(token: str):
    """List all available Slack channels."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_slack_client(token)
        channels = asyncio.run(client.list_channels())
        
        click.echo("📋 Available channels:")
        for channel in channels:
            click.echo(f"  • #{channel['name']} ({channel['id']})")
            
    except Exception as e:
        click.echo(f"❌ Failed to list channels: {e}")
        log.exception("List channels error")

@cli.command("ping", help="Check Slack module configuration")
def cli_ping():
    """Ping command to check Slack module status."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            click.echo("✅ Slack module configuration found")
            click.echo(f"📁 Config path: {env_path}")
        else:
            click.echo("⚠️  No .env file found in Slack module")
            click.echo(f"📁 Expected path: {env_path}")
        
        # Check if token is available
        if os.getenv("SLACK_BOT_TOKEN"):
            click.echo("🔑 Slack token configured")
        else:
            click.echo("❌ No SLACK_BOT_TOKEN found in environment")
            
    except Exception as e:
        click.echo(f"❌ Ping failed: {e}")
        log.exception("Ping error")