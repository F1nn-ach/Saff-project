from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def chat(self, prompt: str, system_prompt: str | None = None) -> str:
        pass
