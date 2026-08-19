"""Centralized test settings loaded from environment / .env file."""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# CI runners are slower than a local machine; TIMEOUT in .env still wins if set
DEFAULT_TIMEOUT = 30.0 if os.getenv("CI") else 15.0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    base_url: str = "https://www.saucedemo.com"
    standard_user: str = "standard_user"
    locked_user: str = "locked_out_user"
    performance_glitch_user: str = "performance_glitch_user"
    password: str = "secret_sauce"
    headless: bool = True
    slow_mo: int = 0
    timeout: float = DEFAULT_TIMEOUT
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
