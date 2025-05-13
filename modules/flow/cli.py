#!/usr/bin/env python3

# flow.cli


import click
from homer.cli_registry import register_cli 
from homer.utils.logger import get_module_logger

log = get_module_logger("flow")

@register_cli("flow")  
@click.group(
    help="Flow integration commands (Confluence, Jira, etc.)",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

