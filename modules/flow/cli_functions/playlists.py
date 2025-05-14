

import click
from homer.utils.logger import get_module_logger
from modules.flow.logic import playlists as playlists_logic

log = get_module_logger("flow.cli.playlists")

@click.group(
    name="playlists",
    help="🎞️ Playlist commands — Manage and inspect playlist version connections."
)
def playlists_cmd():
    pass

@playlists_cmd.command("get-versions", help="List all Versions linked to a Playlist.")
@click.option("--playlist-id", required=True, type=int, help="Playlist ID to fetch versions for")
def get_versions(playlist_id):
    try:
        result = playlists_logic.get_playlist_versions(playlist_id)
        versions = result.get("versions", [])
        click.echo(f"📋 Playlist ID {playlist_id} contains {len(versions)} version(s):")
        for v in versions:
            code = v.get("version.Version.code", "N/A")
            user = v.get("version.Version.user", {}).get("name", "Unknown")
            entity = v.get("version.Version.entity", {}).get("name", "Unknown")
            click.echo(f"  • {code} (User: {user}, Entity: {entity})")
    except Exception as e:
        log.exception("❌ Failed to fetch playlist versions")
        click.echo(f"❌ Error: {e}")
