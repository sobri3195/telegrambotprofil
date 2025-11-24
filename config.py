"""
Configuration module for the Telegram Data Breach Analyzer Bot.
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    telegram_bot_token: str
    log_level: str = "INFO"
    max_file_size: int = 20971520  # 20MB
    allowed_extensions: str = "pdf,txt"
    high_risk_threshold: int = 7
    medium_risk_threshold: int = 4
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get allowed extensions as a list."""
        return [ext.strip() for ext in self.allowed_extensions.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
