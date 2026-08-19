"""Centralized test settings loaded from environment / .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    base_url: str = "https://www.saucedemo.com"
    standard_user: str = "standard_user"
    locked_user: str = "locked_out_user"
    performance_glitch_user: str = "performance_glitch_user"
    password: str = "secret_sauce"
    headless: bool = True
    slow_mo: int = 0
    timeout: float = 15.0
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
