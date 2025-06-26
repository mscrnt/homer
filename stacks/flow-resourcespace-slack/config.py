"""
Flow-ResourceSpace-Slack Stack Configuration
"""
from typing import Dict, Any


class FlowResourceSpaceSlackConfig:
    """Configuration for Flow-ResourceSpace-Slack stack."""
    
    def __init__(self):
        self.stack_name = "flow-resourcespace-slack"
        self.default_channel = "#assets"
        self.auto_tag_assets = True
        self.sync_project_updates = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "stack_name": self.stack_name,
            "default_channel": self.default_channel,
            "auto_tag_assets": self.auto_tag_assets,
            "sync_project_updates": self.sync_project_updates
        }


def get_stack_config() -> Dict[str, Any]:
    """Get stack configuration."""
    config = FlowResourceSpaceSlackConfig()
    return config.to_dict()