#!/usr/bin/env python3

import click
import asyncio
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from modules.discord.logic.runner import start_bot, start_client
from modules.discord.config import DiscordEnv
from pathlib import Path
import os

log = get_module_logger("discord")

# 🧠 Register the CLI group for this module
@register_cli("discord")
@click.group(
    help="🎮 Discord CLI — Commands for Discord bot and client",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

# ──────────────────────────────────────────────────────────────────────────────
# 🤖 Run Discord Bot/Client
# ──────────────────────────────────────────────────────────────────────────────
@cli.command("run", help="Start the Discord bot or client")
@click.option("--mode", type=click.Choice(["bot", "client"]), default="bot", help="Run as bot or client")
@click.option("--token", help="Discord bot token (overrides env var)")
def run(mode: str, token: str):
    """Start the Discord bot or client."""
    try:
        # Load environment config
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        # Get token from parameter or environment
        bot_token = token or os.getenv("DISCORD_BOT_TOKEN")
        if not bot_token:
            click.echo("❌ No Discord bot token provided. Set DISCORD_BOT_TOKEN or use --token")
            return
        
        click.echo(f"🚀 Starting Discord {mode}...")
        
        if mode == "bot":
            asyncio.run(start_bot(bot_token))
        else:
            asyncio.run(start_client(bot_token))
            
    except KeyboardInterrupt:
        click.echo("\n👋 Discord bot stopped")
    except Exception as e:
        click.echo(f"❌ Error starting Discord {mode}: {e}")
        log.exception("Discord startup error")

# ──────────────────────────────────────────────────────────────────────────────
# 🩺 Ping (Health Check)
# ──────────────────────────────────────────────────────────────────────────────
@cli.command("ping", help="Check Discord module configuration")
def cli_ping():
    """Ping command to check Discord module status."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            click.echo("✅ Discord module configuration found")
            click.echo(f"📁 Config path: {env_path}")
        else:
            click.echo("⚠️  No .env file found in Discord module")
            click.echo(f"📁 Expected path: {env_path}")
        
        # Check if token is available
        if os.getenv("DISCORD_BOT_TOKEN"):
            click.echo("🔑 Discord token configured")
        else:
            click.echo("❌ No DISCORD_BOT_TOKEN found in environment")
            
    except Exception as e:
        click.echo(f"❌ Ping failed: {e}")
        log.exception("Ping error")
