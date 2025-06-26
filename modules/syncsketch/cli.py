#!/usr/bin/env python3

import click
import asyncio
import json
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from modules.syncsketch.client import get_syncsketch_client
from pathlib import Path
import os

log = get_module_logger("syncsketch")

@register_cli("syncsketch")
@click.group(
    help="🎨 SyncSketch CLI — Commands for SyncSketch integration",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

@cli.command("upload", help="Upload media to SyncSketch")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--project-id", required=True, help="SyncSketch project ID")
@click.option("--name", help="Name for the uploaded media")
def upload_media(file_path: str, project_id: str, name: str):
    """Upload media file to SyncSketch."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_syncsketch_client()
        result = asyncio.run(client.upload_media(file_path, project_id, name))
        
        click.echo(f"✅ Media uploaded successfully")
        click.echo(f"📁 ID: {result['id']}")
        click.echo(f"🏷️  Name: {result['name']}")
        click.echo(f"🔗 URL: {result['url']}")
        
    except Exception as e:
        click.echo(f"❌ Failed to upload media: {e}")
        log.exception("Upload media error")

@cli.command("projects", help="List SyncSketch projects")
@click.option("--output", "-o", type=click.Path(), help="Output file for projects data (JSON)")
def list_projects(output: str):
    """List available SyncSketch projects."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_syncsketch_client()
        projects = asyncio.run(client.get_projects())
        
        if output:
            with open(output, 'w') as f:
                json.dump(projects, f, indent=2)
            click.echo(f"✅ Projects data saved to {output}")
        else:
            click.echo(f"📋 Available projects ({len(projects)}):")
            for project in projects:
                click.echo(f"  • {project.get('name', 'Unknown')} (ID: {project.get('id', 'N/A')})")
        
    except Exception as e:
        click.echo(f"❌ Failed to list projects: {e}")
        log.exception("List projects error")

@cli.command("reviews", help="List reviews for a project")
@click.option("--project-id", required=True, help="SyncSketch project ID")
@click.option("--output", "-o", type=click.Path(), help="Output file for reviews data (JSON)")
def list_reviews(project_id: str, output: str):
    """List reviews for a SyncSketch project."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_syncsketch_client()
        reviews = asyncio.run(client.get_reviews(project_id))
        
        if output:
            with open(output, 'w') as f:
                json.dump(reviews, f, indent=2)
            click.echo(f"✅ Reviews data saved to {output}")
        else:
            click.echo(f"📋 Reviews for project {project_id} ({len(reviews)}):")
            for review in reviews:
                click.echo(f"  • {review.get('name', 'Unknown')} (Status: {review.get('status', 'N/A')})")
        
    except Exception as e:
        click.echo(f"❌ Failed to list reviews: {e}")
        log.exception("List reviews error")

@cli.command("create-review", help="Create a new review")
@click.option("--project-id", required=True, help="SyncSketch project ID")
@click.option("--name", required=True, help="Review name")
@click.option("--description", help="Review description")
def create_review(project_id: str, name: str, description: str):
    """Create a new review in SyncSketch."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_syncsketch_client()
        result = asyncio.run(client.create_review(project_id, name, description or ""))
        
        click.echo(f"✅ Review created successfully")
        click.echo(f"📁 ID: {result['id']}")
        click.echo(f"🏷️  Name: {result['name']}")
        click.echo(f"🔗 URL: {result['url']}")
        
    except Exception as e:
        click.echo(f"❌ Failed to create review: {e}")
        log.exception("Create review error")

@cli.command("ping", help="Check SyncSketch module configuration")
def cli_ping():
    """Ping command to check SyncSketch module status."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            click.echo("✅ SyncSketch module configuration found")
            click.echo(f"📁 Config path: {env_path}")
        else:
            click.echo("⚠️  No .env file found in SyncSketch module")
            click.echo(f"📁 Expected path: {env_path}")
        
        # Check if required env vars are available
        if os.getenv("SYNCSKETCH_API_KEY"):
            click.echo("🔑 SyncSketch API key configured")
        else:
            click.echo("❌ No SYNCSKETCH_API_KEY found in environment")
            
        if os.getenv("SYNCSKETCH_WORKSPACE"):
            click.echo(f"🏢 Workspace: {os.getenv('SYNCSKETCH_WORKSPACE')}")
        else:
            click.echo("❌ No SYNCSKETCH_WORKSPACE found in environment")
            
    except Exception as e:
        click.echo(f"❌ Ping failed: {e}")
        log.exception("Ping error")