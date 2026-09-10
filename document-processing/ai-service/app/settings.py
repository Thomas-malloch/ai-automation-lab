import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str
    use_mock_extractor: bool


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        use_mock_extractor=os.getenv("USE_MOCK_EXTRACTOR", "true").lower()
        in {"1", "true", "yes", "on"},
    )

