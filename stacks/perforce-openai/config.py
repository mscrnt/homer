"""
Perforce-OpenAI Stack Configuration
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class PerforceOpenAIConfig:
    """Configuration for Perforce-OpenAI stack"""
    
    # Perforce settings
    perforce_port: Optional[str] = None
    perforce_user: Optional[str] = None
    perforce_workspace: Optional[str] = None
    
    # OpenAI settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Integration settings
    auto_review: bool = False
    max_file_size: int = 1000000  # 1MB
    
    @classmethod
    def from_env(cls) -> "PerforceOpenAIConfig":
        """Load configuration from environment variables"""
        return cls(
            perforce_port=os.getenv("PERFORCE_PORT"),
            perforce_user=os.getenv("PERFORCE_USER"),
            perforce_workspace=os.getenv("PERFORCE_WORKSPACE"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            auto_review=os.getenv("AUTO_REVIEW", "false").lower() == "true",
            max_file_size=int(os.getenv("MAX_FILE_SIZE", "1000000"))
        )