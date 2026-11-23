"""Runtime settings for the SprutMonitor MCP server.

Defaults intentionally point at the public demo tenant so `pip install` + run
works out of the box. Production credentials must come from env / .env and
must never be committed.
"""

from __future__ import annotations

import warnings
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEMO_EMAIL = "demo@sprutmonitor.ru"
DEMO_PASSWORD = "demo"
DEFAULT_API_BASE = "https://cloud.sprutmonitor.ru/v3"

# TreeviewUsers root = all users (NodeType RemoteComputer = -666666).
# Group filter uses NodeType=14; user filter uses NodeType=1 (see filters.py).
ROOT_FILTER = [{"NodeType": -666666, "UserID": -666666}]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SPRUT_",
        extra="ignore",
    )

    api_base: str = Field(
        default=DEFAULT_API_BASE,
        description="SprutMonitor web API address, including the cloud.",
    )
    email: str = Field(default=DEMO_EMAIL)
    password: str = Field(default=DEMO_PASSWORD)
    default_days: int = Field(default=1, ge=1, le=90)

    @field_validator("api_base")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")

    @property
    def is_demo(self) -> bool:
        return self.email.lower() == DEMO_EMAIL.lower() and self.password == DEMO_PASSWORD

    def warn_if_demo(self) -> None:
        if self.is_demo:
            warnings.warn(
                "Using SprutMonitor DEMO credentials "
                f"({DEMO_EMAIL}). Do not put production passwords in config "
                "or MCP JSON; use SPRUT_EMAIL / SPRUT_PASSWORD env vars.",
                UserWarning,
                stacklevel=2,
            )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.warn_if_demo()
    return settings
