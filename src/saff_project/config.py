from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "saff.toml"

@dataclass
class ActiveLLMConfig:
    provider: str 

@dataclass
class BaseProviderConfig:
    model: str

@dataclass
class OllamaConfig(BaseProviderConfig):
    base_url: str | None = None
    system_prompt: str | None = None

@dataclass
class Config:
    active_llm: ActiveLLMConfig | None = None
    ollama: OllamaConfig | None = None

    @classmethod
    def load(cls, path: str | Path = _DEFAULT_CONFIG_PATH) -> Config:
        config_path = Path(path)

        if not config_path.exists():
            raise FileNotFoundError(f"Not found config file in: {config_path}")

        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        active_data = data.get("active_llm", {})
        providers = data.get("provider", {})

        return cls(
            active_llm=ActiveLLMConfig(
                provider=active_data.get("provider", {})
            ),
            ollama=OllamaConfig(**providers["ollama"])
            if "ollama" in providers
            else None
        )
