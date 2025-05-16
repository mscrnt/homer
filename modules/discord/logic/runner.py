# modules/discord/logic/runner.py

import os
import asyncio
import discord
from discord.ext import commands
from homer.utils.logger import get_module_logger
from modules.discord.logic.intents import build_intents, build_member_cache_flags
from modules.discord.client import get_discord_bot, get_discord_client

log = get_module_logger("discord.runner")

# Global instance cache
_instance = None


async def run_discord(mode: str = "bot"):
    """
    Launch the Discord bot or client with proper config and cog loading.
    Can be reused from CLI or API context.
    """
    global _instance

    # Check token
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing required environment variable: DISCORD_BOT_TOKEN")

    # Select client mode
    if mode == "bot":
        bot = get_discord_bot()
        await load_all_cogs(bot)
        _instance = bot
        log.info("🤖 Running as commands.Bot...")
        await bot.start(token)

    elif mode == "client":
        client = get_discord_client()
        _instance = client
        log.info("📡 Running as discord.Client...")
        await client.start(token)

    else:
        raise ValueError(f"Unsupported DISCORD_MODE: {mode}")


def get_instance():
    """
    Return the current global Discord client or bot instance.
    This is useful if other modules need access.
    """
    return _instance


async def load_all_cogs(bot: commands.Bot):
    """
    Register all cogs into the bot instance.
    """
    from modules.discord.logic.cogs import commands as command_cog
    from modules.discord.logic.cogs import events as event_cog
    from modules.discord.logic.cogs import periodic as periodic_cog

    try:
        await bot.add_cog(command_cog.CommandCog(bot))
        await bot.add_cog(event_cog.EventHookCog(bot))
        await bot.add_cog(periodic_cog.PeriodicTaskCog(bot))
        log.info("✅ Loaded Discord cogs: commands, events, periodic")
    except Exception as e:
        log.exception("❌ Failed to load cogs")
        raise
