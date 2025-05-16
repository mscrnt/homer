# modules/discord/logic/tasks/debug.py

from discord.ext import tasks
import logging

log = logging.getLogger("discord.tasks.debug")

@tasks.loop(seconds=10)
async def index_loop():
    log.info(f"[index_loop] Current iteration: {index_loop.current_loop}")

@index_loop.before_loop
async def before_index():
    from modules.discord.client import get_discord_bot
    await get_discord_bot().wait_until_ready()
    log.info("📡 Starting index loop...")
