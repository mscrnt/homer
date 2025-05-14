

import click
from homer.utils.logger import get_module_logger
from modules.flow.logic import activity as activity_logic

log = get_module_logger("flow.activity.cli")

@click.group(
    name="activity",
    help="📊 Activity stream and following management"
)
def activity_cmd():
    pass

# ─────────────────────────────────────────────────────────────────────────────
# 📊 Activity Stream
# ─────────────────────────────────────────────────────────────────────────────

@activity_cmd.command("stream", help="Get activity stream for a given entity.")
@click.option("--entity-type", required=True, help="Entity type (e.g. Shot, Version)")
@click.option("--entity-id", required=True, type=int, help="Entity ID")
@click.option("--min-id", type=int, default=None, help="Only return updates with IDs >= min_id")
@click.option("--max-id", type=int, default=None, help="Only return updates with IDs <= max_id")
@click.option("--limit", type=int, default=50, help="Maximum number of updates to return")
def cli_get_activity_stream(entity_type, entity_id, min_id, max_id, limit):
    try:
        result = activity_logic.get_activity_stream(entity_type, entity_id, min_id, max_id, limit)
        click.echo(result)
    except Exception as e:
        click.echo(f"❌ Failed to get activity stream: {e}")
        log.exception("Activity stream fetch failed")

# ─────────────────────────────────────────────────────────────────────────────
# 👤 Follow / Unfollow
# ─────────────────────────────────────────────────────────────────────────────

@activity_cmd.command("follow", help="Follow an entity as a specific user.")
@click.option("--user-id", required=True, type=int, help="User ID (HumanUser)")
@click.option("--entity-type", required=True, help="Entity type to follow")
@click.option("--entity-id", required=True, type=int, help="Entity ID to follow")
def cli_follow_entity(user_id, entity_type, entity_id):
    try:
        result = activity_logic.follow_entity(user_id, entity_type, entity_id)
        click.echo(result)
    except Exception as e:
        click.echo(f"❌ Failed to follow entity: {e}")
        log.exception("Follow failed")

@activity_cmd.command("unfollow", help="Unfollow an entity as a specific user.")
@click.option("--user-id", required=True, type=int, help="User ID (HumanUser)")
@click.option("--entity-type", required=True, help="Entity type to unfollow")
@click.option("--entity-id", required=True, type=int, help="Entity ID to unfollow")
def cli_unfollow_entity(user_id, entity_type, entity_id):
    try:
        result = activity_logic.unfollow_entity(user_id, entity_type, entity_id)
        click.echo(result)
    except Exception as e:
        click.echo(f"❌ Failed to unfollow entity: {e}")
        log.exception("Unfollow failed")

# ─────────────────────────────────────────────────────────────────────────────
# 📋 Follower Queries
# ─────────────────────────────────────────────────────────────────────────────

@activity_cmd.command("followers", help="List followers of an entity.")
@click.option("--entity-type", required=True, help="Entity type")
@click.option("--entity-id", required=True, type=int, help="Entity ID")
def cli_get_followers(entity_type, entity_id):
    try:
        result = activity_logic.get_followers(entity_type, entity_id)
        for user in result:
            click.echo(f"{user['id']}: {user['name']}")
    except Exception as e:
        click.echo(f"❌ Failed to get followers: {e}")
        log.exception("Followers fetch failed")

@activity_cmd.command("following", help="List entities followed by a user.")
@click.option("--user-id", required=True, type=int, help="User ID")
@click.option("--project-id", type=int, default=None, help="Optional Project ID filter")
@click.option("--entity-type", default=None, help="Optional entity type filter")
def cli_get_following(user_id, project_id, entity_type):
    try:
        result = activity_logic.get_following(user_id, project_id, entity_type)
        for entity in result:
            click.echo(f"{entity['type']} {entity['id']}")
    except Exception as e:
        click.echo(f"❌ Failed to get followed entities: {e}")
        log.exception("Following fetch failed")
