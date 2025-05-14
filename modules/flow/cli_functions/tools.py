#!/usr/bin/env python3



import click
import json
from homer.utils.logger import get_module_logger
from modules.flow.logic import tools as tools_logic

log = get_module_logger("flow.tools.cli")

@click.group(name="tools", help="🧰 Flow helper utilities (project lookup, etc.)")
def tools_cmd():
    pass


@tools_cmd.command("list-projects", help="List all ShotGrid projects.")
@click.option("--fields", default='["id", "name"]', help="Fields to return (JSON list).")
def cli_list_projects(fields):
    fields_list = json.loads(fields)
    result = tools_logic.list_projects(fields=fields_list)
    click.echo(json.dumps(result, indent=2))


@tools_cmd.command("get-project-id", help="Get project ID from name.")
@click.option("--name", required=True, help="Project name.")
def cli_get_project_id(name):
    result = tools_logic.find_project_by_name(name)
    if result:
        click.echo(result["id"])
    else:
        click.echo("❌ Project not found.")


@tools_cmd.command("get-project-name", help="Get project name from ID.")
@click.option("--id", "project_id", required=True, type=int, help="Project ID.")
def cli_get_project_name(project_id):
    result = tools_logic.find_project_by_id(project_id)
    if result:
        click.echo(result["name"])
    else:
        click.echo("❌ Project not found.")
