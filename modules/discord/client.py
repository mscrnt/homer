# modules/discord/client.py

import os
import discord
from discord.ext import commands
from homer.utils.logger import get_module_logger

log = get_module_logger("discord-client")

_bot = None
_client = None

def get_discord_client():
    global _client
    if _client is None:
        intents = discord.Intents.default()
        intents.message_content = True

        class MyClient(discord.Client):
            async def on_ready(self):
                log.info(f"🤖 Logged on as {self.user}")

            async def on_message(self, message):
                if message.author == self.user:
                    return
                if message.content.lower() == "ping":
                    await message.channel.send("pong")

        _client = MyClient(intents=intents)
    return _client


def get_discord_bot():
    global _bot
    if _bot is None:
        intents = discord.Intents.default()
        intents.message_content = True
        _bot = commands.Bot(command_prefix=">", intents=intents)

        @_bot.event
        async def on_ready():
            log.info(f"🤖 Logged in as {_bot.user}")

        @_bot.command()
        async def ping(ctx):
            await ctx.send("pong")

    return _bot
