import os
import discord
from homer.utils.logger import get_module_logger

log = get_module_logger("discord.intents")

# All available Discord intent attributes as of v2.5+
ALL_INTENT_FLAGS = {
    "auto_moderation",
    "auto_moderation_configuration",
    "auto_moderation_execution",
    "bans",
    "dm_messages",
    "dm_polls",
    "dm_reactions",
    "dm_typing",
    "emojis",
    "emojis_and_stickers",
    "expressions",
    "guild_messages",
    "guild_polls",
    "guild_reactions",
    "guild_scheduled_events",
    "guild_typing",
    "guilds",
    "integrations",
    "invites",
    "members",
    "message_content",
    "messages",
    "moderation",
    "polls",
    "presences",
    "reactions",
    "typing",
    "voice_states",
    "webhooks",
}

def build_intents() -> discord.Intents:
    """Parse DISCORD_INTENTS and return a configured discord.Intents instance."""
    raw = os.getenv("DISCORD_INTENTS", "guilds,messages,message_content")

    # Start with all disabled
    intents = discord.Intents.none()

    for name in raw.split(","):
        key = name.strip().lower()
        if key in ALL_INTENT_FLAGS and hasattr(intents, key):
            setattr(intents, key, True)
        else:
            log.warning(f"⚠️ Unknown or unsupported intent: '{key}'")

    enabled = [k for k in ALL_INTENT_FLAGS if getattr(intents, k, False)]
    log.info(f"✅ Discord intents enabled: {', '.join(enabled)}")
    return intents

def build_member_cache_flags(intents: discord.Intents) -> discord.MemberCacheFlags:
    """
    Build a member cache policy based on enabled intents.
    Ensures that the bot can cleanly manage member events.
    """
    flags = discord.MemberCacheFlags.from_intents(intents)
    log.info(f"🔍 Member cache flags: joined={flags.joined}, voice={flags.voice}")
    return flags
