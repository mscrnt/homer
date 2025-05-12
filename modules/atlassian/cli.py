#!/usr/bin/env python3

# atlassian.cli


import click
from homer.cli_registry import register_cli 
from homer.utils.logger import get_module_logger
from .confluence import push_to_confluence

log = get_module_logger("atlassian")

@register_cli("atlassian")  
@click.group(
    help="Atlassian integration commands (Confluence, Jira, etc.)",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

@cli.command("push-page", help="Push raw HTML content to Confluence.")
@click.option("--title", required=True, help="Title of the Confluence page.")
@click.option("--space", required=True, help="Confluence space key.")
@click.option("--parent", default=None, help="Optional parent page ID.")
@click.option("--content", required=True, help="HTML content to publish.")
def push_page(title, space, parent, content):
    result = push_to_confluence(title, space, content, parent_page_id=parent)
    log.info(f"📤 Confluence push result: {result}")
