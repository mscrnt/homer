import click
from homer.utils.logger import get_module_logger
from modules.ha_api.logic import service as service_logic

log = get_module_logger("ha_api.service.cli")

@click.group(
    name="service",
    help="🧩 Service Inspector — Interact with Home Assistant services."
)
def service_cmd():
    pass


@service_cmd.command("describe", help="Describe a given service.")
@click.option("--service-id", required=True, help="Service ID (e.g. turn_on)")
@click.option("--domain", required=True, help="Domain name (e.g. light)")
def describe_service(service_id, domain):
    try:
        # You'd typically fetch this service from a domain instance, but here's a mock:
        from homeassistant_api import Domain
        mock_domain = Domain(domain_id=domain, services={})
        mock_service = service_logic.Service(
            service_id=service_id,
            domain=mock_domain,
            name=None,
            description="(No description - simulated)",
            fields={}
        )
        description = service_logic.describe_service(mock_service)
        click.echo("🧩 Service Info:")
        for k, v in description.items():
            click.echo(f"{k}: {v}")
    except Exception as e:
        log.exception("Failed to describe service")
        click.echo(f"❌ Error: {e}")


@service_cmd.command("trigger", help="Trigger a service (sync).")
@click.option("--service-id", required=True, help="Service ID (e.g. turn_on)")
@click.option("--domain", required=True, help="Domain name (e.g. light)")
@click.option("--entity-id", help="Target entity ID")
@click.option("--data", multiple=True, help="Key=value pairs for service data.")
def trigger_service(service_id, domain, entity_id, data):
    try:
        from homeassistant_api import Domain
        mock_domain = Domain(domain_id=domain, services={})
        mock_service = service_logic.Service(
            service_id=service_id,
            domain=mock_domain,
            name=None,
            description="(No description - simulated)",
            fields={}
        )
        payload = dict(kv.split("=", 1) for kv in data)
        result = service_logic.trigger(mock_service, entity_id=entity_id, **payload)
        click.echo(f"✅ Triggered service: {service_id} on {entity_id or 'N/A'}")
        click.echo(result)
    except Exception as e:
        log.exception("Failed to trigger service")
        click.echo(f"❌ Error: {e}")


@service_cmd.command("async-trigger", help="Trigger a service (async).")
@click.option("--service-id", required=True, help="Service ID (e.g. turn_on)")
@click.option("--domain", required=True, help="Domain name (e.g. light)")
@click.option("--entity-id", help="Target entity ID")
@click.option("--data", multiple=True, help="Key=value pairs for service data.")
def async_trigger_service(service_id, domain, entity_id, data):
    import asyncio
    async def run_async():
        try:
            from homeassistant_api import Domain
            mock_domain = Domain(domain_id=domain, services={})
            mock_service = service_logic.Service(
                service_id=service_id,
                domain=mock_domain,
                name=None,
                description="(No description - simulated)",
                fields={}
            )
            payload = dict(kv.split("=", 1) for kv in data)
            result = await service_logic.async_trigger(mock_service, entity_id=entity_id, **payload)
            click.echo(f"✅ Async triggered service: {service_id} on {entity_id or 'N/A'}")
            click.echo(result)
        except Exception as e:
            log.exception("Failed to async trigger service")
            click.echo(f"❌ Error: {e}")

    asyncio.run(run_async())
