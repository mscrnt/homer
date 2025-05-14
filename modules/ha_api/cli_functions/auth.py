import click
from homer.utils.logger import get_module_logger
from homer.modules.ha_api.logic import auth as auth_logic

log = get_module_logger("ha_api.auth.cli")

@click.group(
    name="auth",
    help="🔐 HA Auth — Inspect and log Home Assistant WebSocket auth responses."
)
def auth_cmd():
    pass

@auth_cmd.command("describe", help="Describe a raw auth response message.")
@click.option("--json", "json_data", required=True, help="Raw JSON auth response string.")
def describe_auth(json_data):
    """
    Parse and log a raw Home Assistant auth message.
    """
    import json
    from pydantic import ValidationError

    try:
        data = json.loads(json_data)
        type_ = data.get("type")

        match type_:
            case "auth_required":
                response = auth_logic.AuthRequired(**data)
            case "auth_ok":
                response = auth_logic.AuthOk(**data)
            case "auth_invalid":
                response = auth_logic.AuthInvalid(**data)
            case _:
                raise ValueError(f"Unsupported auth type: {type_}")

        click.echo(response.describe())

    except ValidationError as ve:
        log.error("❌ Validation failed for auth message.")
        click.echo(str(ve))
    except Exception as e:
        log.exception("❌ Failed to parse or describe auth message.")
        click.echo(f"❌ Internal error: {e}")
