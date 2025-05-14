

import click
from homer.utils.logger import get_module_logger
from modules.flow.logic import versions as version_logic

log = get_module_logger("flow.versions.cli")

@click.group(
    name="versions",
    help="🎞️ Version commands — Create and manage versions."
)
def versions_cmd():
    pass

@versions_cmd.command("create", help="Create a new version.")
@click.option("--project-id", required=True, type=int, help="Project ID")
@click.option("--code", required=True, help="Version code")
@click.option("--description", help="Description for the version")
@click.option("--path-to-frames", help="Path to image or movie sequence")
@click.option("--status", help="ShotGrid status list value")
@click.option("--shot-id", type=int, help="Shot ID")
@click.option("--task-id", type=int, help="Task ID")
@click.option("--user-id", type=int, help="User ID")
def create_version_cli(project_id, code, description, path_to_frames, status, shot_id, task_id, user_id):
    try:
        result = version_logic.create_version(
            project_id=project_id,
            code=code,
            description=description,
            sg_path_to_frames=path_to_frames,
            sg_status_list=status,
            shot_id=shot_id,
            task_id=task_id,
            user_id=user_id
        )
        click.echo(f"✅ Created version: {result['code']} (ID: {result['id']})")
    except Exception as e:
        log.exception("❌ Failed to create version")
        click.echo(f"❌ Error: {e}")
