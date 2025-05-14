

import click
from homer.utils.logger import get_module_logger
from modules.flow.logic import tasks as task_logic

log = get_module_logger("flow.tasks.cli")

@click.group(
    name="tasks",
    help="✅ Task commands — Manage and query tasks linked to shots."
)
def tasks_cmd():
    pass

@tasks_cmd.command("by-shot", help="List all tasks linked to a specific Shot ID.")
@click.option("--shot-id", required=True, type=int, help="The Shot ID to look up tasks for.")
def cli_get_tasks_by_shot(shot_id):
    try:
        result = task_logic.get_tasks_for_shot(shot_id)
        click.echo(f"📝 Tasks for Shot {shot_id}:")
        for task in result["tasks"]:
            step = task.get("step.Step.short_name", "N/A")
            status = task.get("sg_status_list", "N/A")
            assignees = ", ".join([a["name"] for a in task.get("task_assignees", [])])
            click.echo(f" • {task['content']} | Step: {step} | Status: {status} | Assignees: {assignees}")
    except Exception as e:
        click.echo("❌ Failed to retrieve tasks")
        log.exception("CLI error: get_tasks_for_shot")
