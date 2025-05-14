import click
import asyncio

from homer.utils.logger import get_module_logger
from modules.ha_api.logic import client as client_logic
from modules.ha_api.logic import event as event_logic

log = get_module_logger("ha_api.event.cli")


@click.group(
    name="event",
    help="📣 Event Tools — Inspect and fire Home Assistant events"
)
def event_cmd():
    pass


@event_cmd.command("describe", help="Describe an event's metadata.")
@click.option("--type", "event_type", required=True, help="Event type to describe (e.g. test_event)")
def describe_event(event_type):
    try:
        event = client_logic.get_event(event_type)
        if not event:
            click.echo(f"⚠️ Event not found: {event_type}")
            return
        info = event_logic.describe_event(event)
        for k, v in info.items():
            click.echo(f"{k}: {v}")
    except Exception as e:
        log.exception("Failed to describe event")
        click.echo(f"❌ Error: {e}")


@event_cmd.command("fire", help="Fire an event synchronously.")
@click.option("--type", "event_type", required=True, help="Event type to fire (e.g. test_event)")
@click.option("--data", multiple=True, help="Key=value pairs to send with the event.")
def fire_event(event_type, data):
    try:
        event = client_logic.get_event(event_type)
        if not event:
            click.echo(f"⚠️ Event not found: {event_type}")
            return
        payload = dict(kv.split("=", 1) for kv in data)
        response = event_logic.fire_event(event, **payload)
        click.echo(f"✅ Event fired. Context ID: {response}")
    except Exception as e:
        log.exception("Failed to fire event")
        click.echo(f"❌ Error: {e}")


@event_cmd.command("afire", help="Fire an event asynchronously.")
@click.option("--type", "event_type", required=True, help="Event type to fire (e.g. test_event)")
@click.option("--data", multiple=True, help="Key=value pairs to send with the event.")
def async_fire_event(event_type, data):
    async def run():
        try:
            event = client_logic.get_event(event_type)
            if not event:
                click.echo(f"⚠️ Event not found: {event_type}")
                return
            payload = dict(kv.split("=", 1) for kv in data)
            response = await event_logic.async_fire_event(event, **payload)
            click.echo(f"✅ Async event fired. Context ID: {response}")
        except Exception as e:
            log.exception("Failed to async fire event")
            click.echo(f"❌ Error: {e}")

    asyncio.run(run())
