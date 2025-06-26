# api.py

from fastapi import HTTPException
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from modules.discord.routes import bot, message
import os

log = get_module_logger("discord-api")

class SendMessageRequest(BaseModel):
    channel_id: int
    content: str
    embed: dict = None

class BotStatusResponse(BaseModel):
    status: str
    guilds: int = 0
    latency: float = 0.0

@register_api
class DiscordAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/discord")

    def register_routes(self):
        # 🩺 Health check route
        @self.router.get("/ping")
        async def ping():
            """Simple health check for Discord service."""
            try:
                has_token = bool(os.getenv("DISCORD_BOT_TOKEN"))
                return {
                    "status": "ok", 
                    "module": "discord",
                    "token_configured": has_token
                }
            except Exception as e:
                log.exception("❌ Discord ping failed")
                return {"status": "error", "message": str(e)}

        # 🤖 Bot status route
        @self.router.get("/status", response_model=BotStatusResponse)
        async def get_bot_status():
            """Get Discord bot status."""
            # This would connect to a running bot instance
            return BotStatusResponse(
                status="offline",
                guilds=0,
                latency=0.0
            )

        # 💬 Send message route
        @self.router.post("/send")
        async def send_message(request: SendMessageRequest):
            """Send a message to a Discord channel."""
            try:
                # This would integrate with the bot client
                return {
                    "status": "success",
                    "message": "Message sending not implemented yet",
                    "channel_id": request.channel_id
                }
            except Exception as e:
                log.exception("❌ Failed to send Discord message")
                raise HTTPException(status_code=500, detail=str(e))

        # 📦 Register all modular routers
        self.router.include_router(bot.router, prefix="/bot")
        self.router.include_router(message.router, prefix="/message")
