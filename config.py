"""
Configuration module for the Telegram Data Breach Search Bot.
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    telegram_bot_token: str
    log_level: str = "INFO"
    website_url: str = "https://scanyour.name"
    initial_credits: int = 51
    credit_cost_per_search: int = 1
    max_multi_query: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
