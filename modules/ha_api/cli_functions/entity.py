import click
import asyncio
from datetime import datetime

from homer.utils.logger import get_module_logger
from modules.ha_api.logic import entity as entity_logic
from modules.ha_api.logic import client as client_logic

log = get_module_logger("ha_api.entity.cli")


@click.group(
    name="entity",
    help="🧩 Entity Tools — Inspect, update, and retrieve entity data"
)
def entity_cmd():
    pass


@entity_cmd.command("id", help="Get the full entity_id from group and slug.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. light.kitchen)")
def show_entity_id(entity_id):
    try:
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return
        eid = entity_logic.get_entity_id(entity)
        click.echo(f"✅ Full Entity ID: {eid}")
    except Exception as e:
        log.exception("Failed to get entity ID")
        click.echo(f"❌ Error: {e}")


@entity_cmd.command("state", help="Get current state of an entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. light.kitchen)")
def current_state(entity_id):
    try:
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return
        state = entity_logic.get_current_state(entity)
        click.echo(f"✅ {state.entity_id} = {state.state}")
    except Exception as e:
        log.exception("Failed to fetch entity state")
        click.echo(f"❌ Error: {e}")


@entity_cmd.command("update", help="Push local state to Home Assistant.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. light.kitchen)")
def update_state(entity_id):
    try:
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return
        state = entity_logic.update_state(entity)
        click.echo(f"📤 State updated for {state.entity_id}: {state.state}")
    except Exception as e:
        log.exception("Failed to update state")
        click.echo(f"❌ Error: {e}")


@entity_cmd.command("history", help="Get state history for an entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. light.kitchen)")
@click.option("--start", help="Start timestamp (ISO format)")
@click.option("--end", help="End timestamp (ISO format)")
@click.option("--significant", is_flag=True, help="Only include significant changes")
def get_history(entity_id, start, end, significant):
    try:
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return

        start_ts = datetime.fromisoformat(start) if start else None
        end_ts = datetime.fromisoformat(end) if end else None

        history = entity_logic.get_history(entity, start_ts, end_ts, significant)
        if not history or not history.states:
            click.echo(f"ℹ️ No history found for {entity_id}")
            return

        click.echo(f"📚 History for {entity_id}:")
        for s in history.states:
            click.echo(f"{s.last_changed.isoformat()} — {s.state}")
    except Exception as e:
        log.exception("Failed to get entity history")
        click.echo(f"❌ Error: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# ⚡ Async Variants via asyncio.run
# ──────────────────────────────────────────────────────────────────────────────

@entity_cmd.command("astate", help="[Async] Get current state of an entity.")
@click.option("--id", "entity_id", required=True)
def async_state(entity_id):
    async def run():
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return
        state = await entity_logic.async_get_current_state(entity)
        click.echo(f"✅ {state.entity_id} = {state.state}")

    asyncio.run(run())


@entity_cmd.command("aupdate", help="[Async] Push local state to Home Assistant.")
@click.option("--id", "entity_id", required=True)
def async_update(entity_id):
    async def run():
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return
        state = await entity_logic.async_update_state(entity)
        click.echo(f"📤 State updated: {state.entity_id} = {state.state}")

    asyncio.run(run())


@entity_cmd.command("ahistory", help="[Async] Get state history for an entity.")
@click.option("--id", "entity_id", required=True)
@click.option("--start", help="Start timestamp (ISO format)")
@click.option("--end", help="End timestamp (ISO format)")
@click.option("--significant", is_flag=True)
def async_history(entity_id, start, end, significant):
    async def run():
        entity = client_logic.get_entity(entity_id)
        if not entity:
            click.echo(f"⚠️ Entity not found: {entity_id}")
            return

        start_ts = datetime.fromisoformat(start) if start else None
        end_ts = datetime.fromisoformat(end) if end else None

        history = await entity_logic.async_get_history(entity, start_ts, end_ts, significant)
        if not history or not history.states:
            click.echo(f"ℹ️ No history found for {entity_id}")
            return

        click.echo(f"📚 [Async] History for {entity_id}:")
        for s in history.states:
            click.echo(f"{s.last_changed.isoformat()} — {s.state}")

    asyncio.run(run())
