import httpx

from saff_project.config import OllamaConfig
from saff_project.providers.base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, config: OllamaConfig):
        self.model = config.model
        self.endpoint = f"{config.base_url.rstrip('/')}/api/chat"

    def chat(self, prompt: str, system_prompt: str | None = None) -> str:
        actual_system_prompt = system_prompt or self.config.system_prompt
        messages = []

        if actual_system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})
            
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = httpx.post(self.endpoint, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]

        except httpx.ConnectError:
            raise ConnectionError(
                f"Can't connect to Ollama at {self.config.base_url} Please check Ollama is running"
            )

        except httpx.TimeoutException:
            raise TimeoutError("Ollama is thinking timeout")
