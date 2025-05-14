import click
from homer.utils.logger import get_module_logger
from modules.ha_api.logic import domain as domain_logic
from modules.ha_api.logic import client as client_logic

log = get_module_logger("ha_api.domain.cli")


@click.group(
    name="domain",
    help="🧰 Domain Utilities — Inspect services inside Home Assistant domains"
)
def domain_cmd():
    pass


@domain_cmd.command("list", help="List all available domains.")
def list_domains():
    try:
        domains = client_logic.get_domains()
        click.echo(f"✅ Found {len(domains)} domains:")
        for dom in domains.values():
            click.echo(f"- {dom.domain_id}")
    except Exception as e:
        log.exception("Failed to list domains")
        click.echo(f"❌ Error: {e}")


@domain_cmd.command("services", help="List all services in a domain.")
@click.option("--domain-id", required=True, help="Domain ID (e.g. light, climate)")
def list_services(domain_id):
    try:
        domain = client_logic.get_domain(domain_id)
        if not domain:
            click.echo(f"⚠️ Domain not found: {domain_id}")
            return
        services = domain_logic.list_services(domain)
        click.echo(f"✅ Services in '{domain_id}':")
        for service in services:
            click.echo(f"- {service}")
    except Exception as e:
        log.exception("Failed to list services in domain")
        click.echo(f"❌ Error: {e}")


@domain_cmd.command("describe", help="Describe a service in a domain.")
@click.option("--domain-id", required=True, help="Domain ID (e.g. light)")
@click.option("--service-id", required=True, help="Service ID (e.g. turn_on)")
def describe_service(domain_id, service_id):
    try:
        domain = client_logic.get_domain(domain_id)
        if not domain:
            click.echo(f"⚠️ Domain not found: {domain_id}")
            return

        service = domain_logic.get_service(domain, service_id)
        if not service:
            click.echo(f"⚠️ Service '{service_id}' not found in domain '{domain_id}'")
            return

        details = domain_logic.describe_service(service)
        click.echo("✅ Service Details:")
        for key, value in details.items():
            if isinstance(value, dict):
                click.echo(f"{key}:")
                for subk, subv in value.items():
                    click.echo(f"  {subk}: {subv}")
            else:
                click.echo(f"{key}: {value}")

    except Exception as e:
        log.exception("Failed to describe service")
        click.echo(f"❌ Error: {e}")
