from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from utils.config import Settings
import cohere


@dataclass
class LLMResponse:
    text: str
    model: str
    used_mock: bool


class LLM:
    """Wrapper around an LLM."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def complete(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.2,
        max_output_tokens: int = 512,
    ) -> LLMResponse:
        if self.settings.mock_mode:
            return self._mock_complete(prompt, system)

        provider = self.settings.llm_provider
        if provider == "cohere":
            return self._cohere_complete(prompt, system, temperature, max_output_tokens)

        raise ValueError(f"Unknown LLM provider: {provider!r}. Use 'cohere'.")

    def _cohere_complete(self, prompt: str, system: str | None, temperature: float, max_output_tokens: int) -> LLMResponse:

        client = cohere.ClientV2(api_key=self.settings.cohere_api_key, timeout=60.0)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        res = client.chat(
            model=self.settings.cohere_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_output_tokens,
        )

        text = res.message.content[0].text
        return LLMResponse(text=text, model=f"cohere:{self.settings.cohere_model}", used_mock=False)
