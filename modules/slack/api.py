from fastapi import HTTPException
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from modules.slack.client import get_slack_client
import os

log = get_module_logger("slack-api")

class SendMessageRequest(BaseModel):
    channel: str
    text: str
    blocks: list = None

class ChannelInfo(BaseModel):
    id: str
    name: str
    is_channel: bool
    is_private: bool

@register_api
class SlackAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/slack")

    def register_routes(self):
        # 🩺 Health check route
        @self.router.get("/ping")
        async def ping():
            """Simple health check for Slack service."""
            try:
                has_token = bool(os.getenv("SLACK_BOT_TOKEN"))
                return {
                    "status": "ok", 
                    "module": "slack",
                    "token_configured": has_token
                }
            except Exception as e:
                log.exception("❌ Slack ping failed")
                return {"status": "error", "message": str(e)}

        # 💬 Send message route
        @self.router.post("/send")
        async def send_message(request: SendMessageRequest):
            """Send a message to a Slack channel."""
            try:
                client = get_slack_client()
                response = await client.send_message(
                    channel=request.channel,
                    text=request.text,
                    blocks=request.blocks
                )
                return {
                    "status": "success",
                    "message": "Message sent successfully",
                    "timestamp": response['ts'],
                    "channel": request.channel
                }
            except Exception as e:
                log.exception("❌ Failed to send Slack message")
                raise HTTPException(status_code=500, detail=str(e))

        # 📋 List channels route
        @self.router.get("/channels")
        async def list_channels():
            """List all available Slack channels."""
            try:
                client = get_slack_client()
                channels = await client.list_channels()
                return {
                    "status": "success",
                    "channels": [
                        {
                            "id": ch["id"],
                            "name": ch["name"],
                            "is_channel": ch.get("is_channel", False),
                            "is_private": ch.get("is_private", False)
                        }
                        for ch in channels
                    ]
                }
            except Exception as e:
                log.exception("❌ Failed to list Slack channels")
                raise HTTPException(status_code=500, detail=str(e))

        # 📝 Channel info route
        @self.router.get("/channels/{channel_id}")
        async def get_channel_info(channel_id: str):
            """Get information about a specific Slack channel."""
            try:
                client = get_slack_client()
                channel = await client.get_channel_info(channel_id)
                return {
                    "status": "success",
                    "channel": {
                        "id": channel["id"],
                        "name": channel["name"],
                        "is_channel": channel.get("is_channel", False),
                        "is_private": channel.get("is_private", False),
                        "topic": channel.get("topic", {}).get("value", ""),
                        "purpose": channel.get("purpose", {}).get("value", "")
                    }
                }
            except Exception as e:
                log.exception(f"❌ Failed to get channel info for {channel_id}")
                raise HTTPException(status_code=500, detail=str(e))