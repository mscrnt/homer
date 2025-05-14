import click
from homer.utils.logger import get_module_logger
from modules.ha_api.logic import client as client_logic
import asyncio

log = get_module_logger("ha_api.client.cli")

@click.group(
    name="client",
    help="🔌 Home Assistant Client — Access states, config, events and more."
)
def client_cmd():
    pass

@client_cmd.command("states", help="List all entity states.")
def list_states():
    try:
        states = client_logic.get_states()
        click.echo(f"✅ Found {len(states)} states:")
        for state in states:
            click.echo(f"{state.entity_id}: {state.state}")
    except Exception as e:
        log.exception("Failed to list states")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("state", help="Get a specific entity state.")
@click.option("--id", "entity_id", required=True, help="Entity ID (e.g. light.living_room)")
def get_state(entity_id):
    try:
        state = client_logic.get_state(entity_id)
        if state:
            click.echo(f"✅ {state.entity_id}: {state.state}")
        else:
            click.echo(f"⚠️ No state found for {entity_id}")
    except Exception as e:
        log.exception("Failed to get entity state")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("entities", help="List entity groups.")
def list_entities():
    try:
        entities = client_logic.get_entities()
        click.echo(f"✅ Found {len(entities)} entity groups:")
        for group_id, group in entities.items():
            click.echo(f"- {group_id}: {len(group.entities)} entities")
    except Exception as e:
        log.exception("Failed to fetch entities")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("entity", help="Get a specific entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID to look up.")
def get_entity(entity_id):
    try:
        entity = client_logic.get_entity(entity_id)
        if entity:
            click.echo(f"✅ Entity: {entity.entity_id} - {entity.state}")
        else:
            click.echo(f"⚠️ Entity not found: {entity_id}")
    except Exception as e:
        log.exception("Failed to fetch entity")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("domain", help="Get details of a specific domain.")
@click.option("--id", "domain_id", required=True, help="Domain ID (e.g. light)")
def get_domain(domain_id):
    try:
        domain = client_logic.get_domain(domain_id)
        if domain:
            click.echo(f"✅ Domain: {domain.domain_id} with {len(domain.services)} services")
        else:
            click.echo(f"⚠️ Domain not found: {domain_id}")
    except Exception as e:
        log.exception("Failed to get domain")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("domains", help="List all service domains.")
def list_domains():
    try:
        domains = client_logic.get_domains()
        click.echo(f"✅ Found {len(domains)} domains:")
        for d in domains:
            click.echo(f"- {d}")
    except Exception as e:
        log.exception("Failed to fetch domains")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("components", help="List all HA components.")
def list_components():
    try:
        components = client_logic.get_components()
        click.echo(f"✅ Found {len(components)} components:")
        for c in components:
            click.echo(f"- {c}")
    except Exception as e:
        log.exception("Failed to list components")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("config", help="Get Home Assistant configuration.")
def show_config():
    try:
        config = client_logic.get_config()
        click.echo("✅ Home Assistant Configuration:")
        click.echo(config)
    except Exception as e:
        log.exception("Failed to get config")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("error-log", help="Get Home Assistant error log.")
def show_error_log():
    try:
        logtext = client_logic.get_error_log()
        click.echo("🪵 Error Log:")
        click.echo(logtext)
    except Exception as e:
        log.exception("Failed to retrieve error log")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("event", help="Get a specific event.")
@click.option("--name", required=True, help="Event name")
def get_event(name):
    try:
        event = client_logic.get_event(name)
        if event:
            click.echo(f"✅ Event: {event.event} (listeners: {event.listener_count})")
        else:
            click.echo(f"⚠️ Event not found: {name}")
    except Exception as e:
        log.exception("Failed to get event")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("events", help="List all events.")
def list_events():
    try:
        events = client_logic.get_events()
        click.echo(f"✅ Found {len(events)} events:")
        for event in events:
            click.echo(f"- {event.event} (listeners: {event.listener_count})")
    except Exception as e:
        log.exception("Failed to list events")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("logbook", help="Fetch logbook entries.")
def show_logbook():
    try:
        entries = client_logic.get_logbook_entries()
        for entry in entries:
            click.echo(f"{entry.when} - {entry.name} [{entry.entity_id or entry.context_id}]")
    except Exception as e:
        log.exception("Failed to fetch logbook")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("history", help="Fetch state history.")
@click.option("--entity", "entities", multiple=True, help="Entities to fetch history for.")
@click.option("--start", "start", required=False, help="Start timestamp")
@click.option("--end", "end", required=False, help="End timestamp")
@click.option("--significant", is_flag=True, help="Only fetch significant changes")
def show_history(entities, start, end, significant):
    try:
        histories = client_logic.get_entity_histories(
            entities=list(entities) or None,
            start_timestamp=start,
            end_timestamp=end,
            significant_changes_only=significant
        )
        for history in histories:
            click.echo(f"📜 {history.entity_id}")
            for state in history.states:
                click.echo(f"  - {state.last_changed}: {state.state}")
    except Exception as e:
        log.exception("Failed to get history")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("template", help="Render a Jinja2 template.")
@click.option("--template", required=True, help="Template string to render")
def render_template(template):
    try:
        result = client_logic.get_rendered_template(template)
        click.echo(f"🧠 Rendered Template:\n{result}")
    except Exception as e:
        log.exception("Failed to render template")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("trigger", help="Trigger a Home Assistant service.")
@click.option("--domain", required=True, help="Domain (e.g. light)")
@click.option("--service", required=True, help="Service name (e.g. turn_on)")
@click.option("--data", multiple=True, help="Key=value pairs to send to the service")
def trigger_service(domain, service, data):
    try:
        payload = dict(kv.split("=", 1) for kv in data)
        result = client_logic.trigger_service(domain, service, **payload)
        click.echo(f"✅ Triggered service. States changed: {len(result)}")
    except Exception as e:
        log.exception("Failed to trigger service")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("trigger-with-response", help="Trigger a service and show full response.")
@click.option("--domain", required=True, help="Domain (e.g. light)")
@click.option("--service", required=True, help="Service name (e.g. turn_on)")
@click.option("--data", multiple=True, help="Key=value pairs to send")
def trigger_service_resp(domain, service, data):
    try:
        payload = dict(kv.split("=", 1) for kv in data)
        result, response = client_logic.trigger_service_with_response(domain, service, **payload)
        click.echo(f"✅ Triggered service. States changed: {len(result)}")
        click.echo(f"📦 Service response: {response}")
    except Exception as e:
        log.exception("Failed to trigger service with response")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("set-state", help="Set a fake state on an entity.")
@click.option("--id", "entity_id", required=True, help="Entity ID")
@click.option("--value", required=True, help="New state value")
def set_fake_state(entity_id, value):
    try:
        from homeassistant_api import State
        state = State(entity_id=entity_id, state=value)
        result = client_logic.set_state(state)
        click.echo(f"✅ State set for {result.entity_id}: {result.state}")
    except Exception as e:
        log.exception("Failed to set state")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("check", help="Check HA API is running.")
def check_running():
    try:
        if client_logic.check_api_running():
            click.echo("✅ Home Assistant API is up and running!")
        else:
            click.echo("⚠️ Home Assistant API did not respond as expected.")
    except Exception as e:
        log.exception("Failed to check API status")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("check-config", help="Check HA config is valid.")
def check_config():
    try:
        if client_logic.check_api_config():
            click.echo("✅ Configuration is valid.")
        else:
            click.echo("⚠️ Configuration appears to have issues.")
    except Exception as e:
        log.exception("Failed to validate configuration")
        click.echo(f"❌ Error: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# ⚡ Async CLI commands
# ──────────────────────────────────────────────────────────────────────────────

@client_cmd.command("async-states", help="List all states (async).")
def async_list_states():
    try:
        states = asyncio.run(client_logic.async_get_states())
        click.echo(f"⚡ Found {len(states)} states (via async):")
        for state in states:
            click.echo(f"{state.entity_id}: {state.state}")
    except Exception as e:
        log.exception("Failed to fetch states asynchronously")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("async-state", help="Get a specific state (async).")
@click.option("--id", "entity_id", required=True, help="Entity ID")
def async_get_state(entity_id):
    try:
        state = asyncio.run(client_logic.async_get_state(entity_id))
        if state:
            click.echo(f"⚡ {state.entity_id}: {state.state}")
        else:
            click.echo(f"⚠️ No state found for {entity_id}")
    except Exception as e:
        log.exception("Failed to fetch state asynchronously")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("async-trigger", help="Trigger a service (async).")
@click.option("--domain", required=True, help="Domain (e.g. light)")
@click.option("--service", required=True, help="Service name (e.g. turn_on)")
@click.option("--data", multiple=True, help="Key=value pairs for service data")
def async_trigger(domain, service, data):
    try:
        payload = dict(kv.split("=", 1) for kv in data)
        states = asyncio.run(client_logic.async_trigger_service(domain, service, **payload))
        click.echo(f"⚡ Service triggered: {domain}.{service}")
        click.echo(f"🔄 States changed: {len(states)}")
    except Exception as e:
        log.exception("Failed to trigger service asynchronously")
        click.echo(f"❌ Error: {e}")

@client_cmd.command("async-config", help="Get HA config (async).")
def async_config():
    try:
        config = asyncio.run(client_logic.async_get_config())
        click.echo("⚡ Async Config Result:")
        click.echo(config)
    except Exception as e:
        log.exception("Failed to fetch config asynchronously")
        click.echo(f"❌ Error: {e}")