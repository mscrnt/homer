"""
Slack-SyncSketch Stack Configuration
"""
import os
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SlackSyncSketchConfig:
    """Configuration for Slack-SyncSketch stack"""
    
    # Slack settings
    slack_token: Optional[str] = None
    slack_channel: str = "#general"
    slack_webhook_url: Optional[str] = None
    
    # SyncSketch settings
    syncsketch_api_key: Optional[str] = None
    syncsketch_base_url: str = "https://www.syncsketch.com"
    syncsketch_workspace: Optional[str] = None
    
    # Integration settings
    auto_notify: bool = True
    notification_events: List[str] = None
    
    def __post_init__(self):
        if self.notification_events is None:
            self.notification_events = ["review_created", "review_updated", "comment_added"]
    
    @classmethod
    def from_env(cls) -> "SlackSyncSketchConfig":
        """Load configuration from environment variables"""
        notification_events = os.getenv("NOTIFICATION_EVENTS")
        if notification_events:
            notification_events = notification_events.split(",")
        
        return cls(
            slack_token=os.getenv("SLACK_TOKEN"),
            slack_channel=os.getenv("SLACK_CHANNEL", "#general"),
            slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
            syncsketch_api_key=os.getenv("SYNCSKETCH_API_KEY"),
            syncsketch_base_url=os.getenv("SYNCSKETCH_BASE_URL", "https://www.syncsketch.com"),
            syncsketch_workspace=os.getenv("SYNCSKETCH_WORKSPACE"),
            auto_notify=os.getenv("AUTO_NOTIFY", "true").lower() == "true",
            notification_events=notification_events
        )