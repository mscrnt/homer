#!/usr/bin/env python3

import click
import asyncio
import json
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from modules.perforce.client import get_perforce_client
from pathlib import Path
import os

log = get_module_logger("perforce")

@register_cli("perforce")
@click.group(
    help="🔧 Perforce CLI — Commands for Perforce integration",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

@cli.command("changelist", help="Get details of a changelist")
@click.argument("changelist_id")
@click.option("--output", "-o", type=click.Path(), help="Output file for changelist data (JSON)")
def get_changelist(changelist_id: str, output: str):
    """Get details of a specific changelist."""
    try:
        # Load environment config
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_perforce_client()
        changelist = asyncio.run(client.get_changelist(changelist_id))
        
        if output:
            with open(output, 'w') as f:
                json.dump(changelist, f, indent=2)
            click.echo(f"✅ Changelist data saved to {output}")
        else:
            click.echo(f"📋 Changelist {changelist['id']}")
            click.echo(f"👤 User: {changelist['user']}")
            click.echo(f"📅 Date: {changelist['date']}")
            click.echo(f"📝 Description: {changelist['description']}")
            click.echo(f"📁 Files ({len(changelist['files'])}):")
            for file_info in changelist['files'][:10]:  # Show first 10 files
                click.echo(f"  • {file_info['action']} {file_info['path']}")
            if len(changelist['files']) > 10:
                click.echo(f"  ... and {len(changelist['files']) - 10} more files")
        
    except Exception as e:
        click.echo(f"❌ Failed to get changelist: {e}")
        log.exception("Get changelist error")

@cli.command("changes", help="List recent changelists")
@click.option("--user", "-u", help="Filter by user")
@click.option("--max", type=int, default=20, help="Maximum number of changelists to show")
@click.option("--output", "-o", type=click.Path(), help="Output file for changelists data (JSON)")
def list_changelists(user: str, max: int, output: str):
    """List recent changelists."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_perforce_client()
        changelists = asyncio.run(client.list_changelists(user, max))
        
        if output:
            with open(output, 'w') as f:
                json.dump(changelists, f, indent=2)
            click.echo(f"✅ Changelists data saved to {output}")
        else:
            click.echo(f"📋 Recent changelists ({len(changelists)}):")
            for cl in changelists:
                click.echo(f"  • {cl['id']} by {cl['user']} on {cl['date']}")
                if cl['description']:
                    click.echo(f"    {cl['description'][:80]}{'...' if len(cl['description']) > 80 else ''}")
        
    except Exception as e:
        click.echo(f"❌ Failed to list changelists: {e}")
        log.exception("List changelists error")

@cli.command("streams", help="List available streams")
@click.option("--output", "-o", type=click.Path(), help="Output file for streams data (JSON)")
def list_streams(output: str):
    """List available streams."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_perforce_client()
        streams = asyncio.run(client.get_streams())
        
        if output:
            with open(output, 'w') as f:
                json.dump(streams, f, indent=2)
            click.echo(f"✅ Streams data saved to {output}")
        else:
            click.echo(f"🌊 Available streams ({len(streams)}):")
            for stream in streams:
                click.echo(f"  • {stream['name']} ({stream['type']})")
                if stream['parent']:
                    click.echo(f"    Parent: {stream['parent']}")
                if stream['description']:
                    click.echo(f"    {stream['description'][:80]}{'...' if len(stream['description']) > 80 else ''}")
        
    except Exception as e:
        click.echo(f"❌ Failed to list streams: {e}")
        log.exception("List streams error")

@cli.command("sync", help="Sync files from depot")
@click.argument("filespec", default="...")
def sync_files(filespec: str):
    """Sync files from the depot."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_perforce_client()
        result = asyncio.run(client.sync_files(filespec))
        
        click.echo(f"🔄 Sync completed for: {filespec}")
        if result:
            lines = result.split('\\n')
            click.echo(f"📁 Synced {len(lines)} items")
            # Show first few lines
            for line in lines[:5]:
                if line.strip():
                    click.echo(f"  • {line}")
            if len(lines) > 5:
                click.echo(f"  ... and {len(lines) - 5} more items")
        
    except Exception as e:
        click.echo(f"❌ Failed to sync files: {e}")
        log.exception("Sync files error")

@cli.command("info", help="Show workspace information")
def workspace_info():
    """Show information about the current workspace."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_perforce_client()
        info = asyncio.run(client.get_workspace_info())
        
        click.echo("🏢 Workspace Information:")
        for key, value in info.items():
            # Format key for display
            display_key = key.replace('_', ' ').title()
            click.echo(f"  {display_key}: {value}")
        
    except Exception as e:
        click.echo(f"❌ Failed to get workspace info: {e}")
        log.exception("Workspace info error")

@cli.command("ping", help="Check Perforce module configuration")
def cli_ping():
    """Ping command to check Perforce module status."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            click.echo("✅ Perforce module configuration found")
            click.echo(f"📁 Config path: {env_path}")
        else:
            click.echo("⚠️  No .env file found in Perforce module")
            click.echo(f"📁 Expected path: {env_path}")
        
        # Check if required env vars are available
        if os.getenv("P4PORT"):
            click.echo(f"🌐 P4PORT: {os.getenv('P4PORT')}")
        else:
            click.echo("❌ No P4PORT found in environment")
            
        if os.getenv("P4USER"):
            click.echo(f"👤 P4USER: {os.getenv('P4USER')}")
        else:
            click.echo("❌ No P4USER found in environment")
            
        if os.getenv("P4CLIENT"):
            click.echo(f"💻 P4CLIENT: {os.getenv('P4CLIENT')}")
        else:
            click.echo("⚠️  P4CLIENT not set (optional)")
            
    except Exception as e:
        click.echo(f"❌ Ping failed: {e}")
        log.exception("Ping error")