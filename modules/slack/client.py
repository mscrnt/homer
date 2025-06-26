import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from homer.utils.logger import get_module_logger

log = get_module_logger("slack.client")

class SlackClient:
    def __init__(self, token: str = None):
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        if not self.token:
            raise ValueError("SLACK_BOT_TOKEN is required")
        
        self.client = WebClient(token=self.token)
    
    async def send_message(self, channel: str, text: str, blocks: list = None):
        """Send a message to a Slack channel."""
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text,
                blocks=blocks
            )
            log.info(f"Message sent to {channel}: {response['ts']}")
            return response
        except SlackApiError as e:
            log.error(f"Failed to send message: {e.response['error']}")
            raise
    
    async def get_channel_info(self, channel: str):
        """Get information about a Slack channel."""
        try:
            response = self.client.conversations_info(channel=channel)
            return response['channel']
        except SlackApiError as e:
            log.error(f"Failed to get channel info: {e.response['error']}")
            raise
    
    async def list_channels(self):
        """List all channels the bot has access to."""
        try:
            response = self.client.conversations_list()
            return response['channels']
        except SlackApiError as e:
            log.error(f"Failed to list channels: {e.response['error']}")
            raise

def get_slack_client(token: str = None) -> SlackClient:
    """Get a configured Slack client instance."""
    return SlackClient(token)