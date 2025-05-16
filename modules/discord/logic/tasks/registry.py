# modules/discord/logic/tasks/registry.py

from modules.discord.logic.tasks import (
    scheduler,
    batcher,
    debug,
)

TASKS = {
    "daily_ping": scheduler.daily_ping_loop,
    "batch_update": batcher.batch_task_loop,
    "print_index": debug.index_loop,
}

def start_all():
    for name, task in TASKS.items():
        if not task.is_running():
            task.start()

def stop_all():
    for task in TASKS.values():
        if task.is_running():
            task.stop()

def get_status():
    return {
        name: {
            "running": task.is_running(),
            "loop": getattr(task, "current_loop", None),
            "next": str(getattr(task, "next_iteration", "unknown")),
        }
        for name, task in TASKS.items()
    }
