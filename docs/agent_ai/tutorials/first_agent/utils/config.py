from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


def load_env(env_path: str | None = None) -> None:
    if env_path is None:
        env_file = Path.cwd() / ".env"
        if env_file.exists():
            load_dotenv(env_file)
        return

    p = Path(env_path)
    if p.exists():
        load_dotenv(p)


@dataclass(frozen=True)
class Settings:
    # Which LLM provider to use: "cohere"
    llm_provider: str

    cohere_api_key: str | None
    cohere_model: str

    serpapi_api_key: str | None

    @property
    def mock_mode(self) -> bool:
        if self.llm_provider == "cohere":
            return not bool(self.cohere_api_key)
        return True   

    @property
    def active_model(self) -> str:
        return self.cohere_model


def get_settings() -> Settings:
    provider = (os.getenv("LLM_PROVIDER") or "").strip().lower() or None

    # Cohere SDK commonly uses CO_API_KEY, but many setups use COHERE_API_KEY.
    cohere_key = os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY") or None

    if provider is None:
        provider = "cohere" if cohere_key else "missing"

    return Settings(
        llm_provider=provider,
        cohere_api_key=cohere_key,
        cohere_model=os.getenv("COHERE_MODEL", "command-r-plus-08-2024"),
        serpapi_api_key=os.getenv("SERPAPI_API_KEY") or None,
    )
