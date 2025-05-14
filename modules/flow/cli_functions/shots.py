

import click
from typing import Optional
from modules.flow.logic import shots as shots_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.cli.shots")

@click.group(
    name="shots",
    help="🎬 Shot commands — Manage and query Shot entities."
)
def shots_cmd():
    pass


@shots_cmd.command("by-project", help="List all Shots by project name.")
@click.option("--project", required=True, help="The name of the project")
def get_by_project(project: str):
    try:
        result = shots_logic.get_shots_by_project_name(project)
        for shot in result["shots"]:
            click.echo(f"{shot['id']}: {shot['code']}")
    except Exception as e:
        log.exception("Failed to retrieve shots by project")
        click.echo(f"❌ {e}")


@shots_cmd.command("get", help="Get a Shot by its ID.")
@click.option("--shot-id", required=True, type=int, help="Shot ID")
def get_shot(shot_id: int):
    try:
        shot = shots_logic.get_shot_by_id(shot_id)
        click.echo(shot)
    except Exception as e:
        log.exception("Failed to retrieve shot by ID")
        click.echo(f"❌ {e}")


@shots_cmd.command("create", help="Create a new Shot.")
@click.option("--project-id", required=True, type=int, help="Project ID")
@click.option("--code", required=True, help="Shot code")
@click.option("--description", help="Description for the Shot")
@click.option("--status", help="Shot status list value")
@click.option("--task-template-id", type=int, help="Optional TaskTemplate ID")
def create(project_id, code, description, status, task_template_id):
    try:
        result = shots_logic.create_shot(
            project_id=project_id,
            code=code,
            description=description,
            sg_status_list=status,
            task_template_id=task_template_id
        )
        click.echo(f"✅ Created Shot: {result['id']} — {result['code']}")
    except Exception as e:
        log.exception("Failed to create shot")
        click.echo(f"❌ {e}")


@shots_cmd.command("update", help="Update a Shot.")
@click.option("--shot-id", required=True, type=int, help="Shot ID to update")
@click.option("--description", help="New description")
@click.option("--status", help="New status list value")
def update(shot_id, description, status):
    updates = {}
    if description:
        updates["description"] = description
    if status:
        updates["sg_status_list"] = status

    if not updates:
        click.echo("⚠️ No update fields provided.")
        return

    try:
        result = shots_logic.update_shot(shot_id, updates)
        click.echo(f"✅ Updated Shot {shot_id}: {result}")
    except Exception as e:
        log.exception("Failed to update shot")
        click.echo(f"❌ {e}")


@shots_cmd.command("delete", help="Delete a Shot by ID.")
@click.option("--shot-id", required=True, type=int, help="Shot ID to delete")
def delete(shot_id: int):
    try:
        success = shots_logic.delete_shot(shot_id)
        if success:
            click.echo(f"🗑️ Deleted Shot {shot_id}")
        else:
            click.echo(f"⚠️ Shot {shot_id} not deleted.")
    except Exception as e:
        log.exception("Failed to delete shot")
        click.echo(f"❌ {e}")
