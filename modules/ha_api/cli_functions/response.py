import click
from modules.ha_api.logic import response as response_logic
from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.response.cli")

@click.group(
    name="response",
    help="📡 WebSocket Response Inspector — View details from Home Assistant WS responses"
)
def response_cmd():
    pass


@response_cmd.command("error", help="Describe a WebSocket error response.")
@click.option("--code", required=True, help="Error code (e.g., not_found)")
@click.option("--message", required=True, help="Error message")
@click.option("--id", type=int, default=1, help="Message ID")
def describe_error(code, message, id):
    try:
        fake = response_logic.ErrorResponse(
            type="result",
            success=False,
            id=id,
            error={"code": code, "message": message}
        )
        click.echo(fake.describe())
    except Exception as e:
        log.exception("Failed to describe ErrorResponse")
        click.echo(f"❌ Error: {e}")


@response_cmd.command("ping", help="Display latency from PingResponse.")
@click.option("--start", type=int, required=True, help="Start timestamp (ms)")
@click.option("--end", type=int, help="End timestamp (ms)")
@click.option("--id", type=int, default=1, help="Message ID")
def ping_latency(start, end, id):
    try:
        ping = response_logic.PingResponse(type="pong", id=id, start=start, end=end)
        latency = ping.get_latency_ms()
        if latency is not None:
            click.echo(f"🟡 Latency: {latency} ms")
        else:
            click.echo("⚠️ Latency could not be calculated (missing 'end')")
    except Exception as e:
        log.exception("Failed to process PingResponse")
        click.echo(f"❌ Error: {e}")


@response_cmd.command("result", help="Describe a ResultResponse.")
@click.option("--id", type=int, default=1, help="Message ID")
@click.option("--value", "result", help="Optional result payload")
def describe_result(id, result):
    try:
        res = response_logic.ResultResponse(
            type="result",
            success=True,
            id=id,
            result=result or None
        )
        click.echo(res.describe())
    except Exception as e:
        log.exception("Failed to describe ResultResponse")
        click.echo(f"❌ Error: {e}")
