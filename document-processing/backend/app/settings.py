import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ai_service_url: str


def get_settings() -> Settings:
    return Settings(
        ai_service_url=os.getenv("AI_SERVICE_URL", "http://127.0.0.1:8000"),
    )
