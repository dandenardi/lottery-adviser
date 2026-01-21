"""
Configuration module for the Lottery Adviser API.

This module handles all application settings using Pydantic Settings.
"""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="Lottery Adviser API", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    environment: str = Field(default="production", alias="ENVIRONMENT")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Database
    database_url: str = Field(..., alias="DATABASE_URL")
    
    # Redis (optional)
    redis_url: str | None = Field(default=None, alias="REDIS_URL")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:19006"],
        alias="CORS_ORIGINS"
    )
    
    # Rate Limiting
    rate_limit_suggestions_per_day: int = Field(default=3, alias="RATE_LIMIT_SUGGESTIONS_PER_DAY")
    rate_limit_premium_unlimited: bool = Field(default=True, alias="RATE_LIMIT_PREMIUM_UNLIMITED")
    
    # Lottery Configuration
    lottery_min_number: int = Field(default=1, alias="LOTTERY_MIN_NUMBER")
    lottery_max_number: int = Field(default=25, alias="LOTTERY_MAX_NUMBER")
    numbers_per_game: int = Field(default=15, alias="NUMBERS_PER_GAME")
    
    # Scraper
    scraper_enabled: bool = Field(default=True, alias="SCRAPER_ENABLED")
    scraper_schedule_hour: int = Field(default=22, alias="SCRAPER_SCHEDULE_HOUR")
    scraper_url: str = Field(
        default="https://asloterias.com.br/download-todos-resultados-lotofacil",
        alias="SCRAPER_URL"
    )
    
    # RevenueCat
    revenuecat_api_key: str | None = Field(default=None, alias="REVENUECAT_API_KEY")
    revenuecat_webhook_secret: str | None = Field(default=None, alias="REVENUECAT_WEBHOOK_SECRET")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance loaded from environment variables
    """
    return Settings()


# Convenience exports
settings = get_settings()
