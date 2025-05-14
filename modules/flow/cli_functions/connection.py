

import click
from homer.utils.logger import get_module_logger
from modules.flow.logic import connection as conn_logic

log = get_module_logger("flow.cli.connection")

@click.group(
    name="connection",
    help="🌐 Connection commands — API session, server info, and user authentication."
)
def connection_cmd():
    pass

@connection_cmd.command("info", help="Get ShotGrid server metadata.")
def cli_get_server_info():
    try:
        info = conn_logic.get_server_info()
        click.echo("✅ Server Info:")
        for k, v in info.items():
            click.echo(f"{k}: {v}")
    except Exception as e:
        click.echo("❌ Failed to get server info")
        log.exception("Server info error")

@connection_cmd.command("session", help="Get current ShotGrid session token.")
def cli_get_session_token():
    try:
        token = conn_logic.get_session_token()
        click.echo(f"🔐 Session Token: {token}")
    except Exception as e:
        click.echo("❌ Failed to get session token")
        log.exception("Session token error")

@connection_cmd.command("auth", help="Authenticate a human user manually.")
@click.option("--login", required=True, help="ShotGrid username")
@click.option("--password", required=True, help="ShotGrid password")
@click.option("--token", required=False, help="2FA one-time token (if required)")
def cli_authenticate_user(login, password, token):
    try:
        user = conn_logic.authenticate_user(login, password, token)
        click.echo(f"✅ Authenticated: {user['name']} (id={user['id']})")
    except Exception as e:
        click.echo("❌ Authentication failed")
        log.exception("Authentication error")
