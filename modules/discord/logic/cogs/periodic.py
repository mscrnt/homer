from discord.ext import commands
from modules.discord.logic.tasks.registry import start_all, stop_all

class PeriodicTaskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        start_all()

    def cog_unload(self):
        stop_all()
