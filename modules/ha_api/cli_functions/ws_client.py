import click
import json
import asyncio

from homer.utils.logger import get_module_logger
from modules.ha_api.cli_functions import ws_client as ws_logic

log = get_module_logger("ha_api.ws_client.cli")

@click.group(
    name="ws",
    help="🌐 WebSocket Client — Real-time data from Home Assistant WebSocket API"
)
def ws_cmd():
    pass


@ws_cmd.command("states", help="List all entity states via WebSocket.")
def ws_states():
    try:
        states = ws_logic.get_states()
        click.echo(f"✅ Found {len(states)} states:")
        for state in states:
            click.echo(f"{state.entity_id}: {state.state}")
    except Exception as e:
        log.exception("Failed to list WS states")
        click.echo(f"❌ Error: {e}")


@ws_cmd.command("state", help="Get a specific entity state via WebSocket.")
@click.option("--id", "entity_id", required=True, help="Entity ID to fetch")
def ws_state(entity_id):
    try:
        state = ws_logic.get_state(entity_id)
        if state:
            click.echo(f"✅ {state.entity_id}: {state.state}")
        else:
            click.echo(f"⚠️ No state found for {entity_id}")
    except Exception as e:
        log.exception("Failed to fetch WS state")
        click.echo(f"❌ Error: {e}")


@ws_cmd.command("config", help="Get Home Assistant config via WebSocket.")
def ws_config():
    try:
        config = ws_logic.get_config()
        click.echo("✅ Config:")
        click.echo(json.dumps(config, indent=2))
    except Exception as e:
        log.exception("Failed to fetch WS config")
        click.echo(f"❌ Error: {e}")


@ws_cmd.command("domains", help="List all service domains via WebSocket.")
def ws_domains():
    try:
        domains = ws_logic.get_domains()
        click.echo(f"✅ Found {len(domains)} domains:")
        for domain in domains.values():
            click.echo(f"- {domain.domain_id}")
    except Exception as e:
        log.exception("Failed to fetch WS domains")
        click.echo(f"❌ Error: {e}")


@ws_cmd.command("template", help="Render a Jinja2 template via WebSocket.")
@click.option("--text", required=True, help="Template string to render")
def ws_template(text):
    try:
        result = ws_logic.get_rendered_template(text)
        click.echo(f"✅ Rendered Template:\n{result}")
    except Exception as e:
        log.exception("Failed to render WS template")
        click.echo(f"❌ Error: {e}")


@ws_cmd.command("fire", help="Fire an event via WebSocket.")
@click.option("--type", "event_type", required=True, help="Event type (e.g. test_event)")
@click.option("--data", multiple=True, help="Event payload as key=value")
def ws_fire_event(event_type, data):
    try:
        payload = dict(kv.split("=", 1) for kv in data)
        ctx = ws_logic.fire_event(event_type, **payload)
        click.echo(f"✅ Event fired: {event_type} (context ID: {ctx.id})")
    except Exception as e:
        log.exception("Failed to fire WS event")
        click.echo(f"❌ Error: {e}")


@ws_cmd.command("service", help="Trigger a service via WebSocket.")
@click.option("--domain", required=True, help="Domain (e.g. light)")
@click.option("--service", required=True, help="Service name (e.g. turn_on)")
@click.option("--data", multiple=True, help="Service payload as key=value")
def ws_trigger_service(domain, service, data):
    try:
        payload = dict(kv.split("=", 1) for kv in data)
        ws_logic.trigger_service(domain, service, **payload)
        click.echo(f"✅ Triggered service: {domain}.{service}")
    except Exception as e:
        log.exception("Failed to trigger WS service")
        click.echo(f"❌ Error: {e}")


@ws_cmd.command("service-response", help="Trigger a service and show response.")
@click.option("--domain", required=True, help="Domain (e.g. switch)")
@click.option("--service", required=True, help="Service name (e.g. toggle)")
@click.option("--data", multiple=True, help="Payload as key=value")
def ws_trigger_service_response(domain, service, data):
    try:
        payload = dict(kv.split("=", 1) for kv in data)
        result = ws_logic.trigger_service_with_response(domain, service, **payload)
        click.echo(f"✅ Service triggered. Response:")
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        log.exception("Failed to trigger WS service with response")
        click.echo(f"❌ Error: {e}")
