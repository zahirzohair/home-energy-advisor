from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List, Optional

from app.models.home import Home


class LLMProvider(ABC):
    @abstractmethod
    def generate_advice(self, home: Home) -> List[str]:
        """Return a prioritized list of actionable recommendations."""
        pass


def _build_prompt(home: Home) -> str:
    parts = [
        "You are an energy efficiency advisor. Based on the following home profile, provide actionable, prioritized energy-saving recommendations.",
        "Respond with a numbered list of recommendations only, one per line. No preamble or conclusion.",
        "",
        "Home profile:",
        f"- Size: {home.size_sqm} m²",
        f"- Year built: {home.year_built or 'Unknown'}",
        f"- Heating: {home.heating_type.value}",
        f"- Insulation: {home.insulation.value if home.insulation else 'Unknown'}",
    ]
    if home.notes:
        parts.append(f"- Notes: {home.notes}")
    return "\n".join(parts)


def _parse_recommendations(text: str) -> List[str]:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    result = []
    for line in lines:
        stripped = line.lstrip("0123456789.)-•* ")
        if stripped:
            result.append(stripped)
    return result if result else [text.strip()]


class MockLLMProvider(LLMProvider):
    """Returns fixed recommendations when no API key is configured."""

    def generate_advice(self, home: Home) -> List[str]:
        return [
            "Consider upgrading to a heat pump if your heating system is old.",
            "Improve insulation in the attic and walls where possible.",
            "Install programmable thermostats to reduce heating when away.",
            "Seal drafts around windows and doors.",
            "Switch to LED lighting and energy-efficient appliances.",
        ]


class OpenAILLMProvider(LLMProvider):
    """Uses OpenAI API to generate advice. Requires OPENAI_API_KEY."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini", client: Optional["OpenAI"] = None):
        self._api_key = api_key
        self._model = model
        self._client = client

    def generate_advice(self, home: Home) -> List[str]:
        from openai import OpenAI
        client = self._client or OpenAI(api_key=self._api_key)
        prompt = _build_prompt(home)
        response = client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content or ""
        return _parse_recommendations(content)


@lru_cache(maxsize=1)
def _cached_openai_client(api_key: str):
    from openai import OpenAI
    return OpenAI(api_key=api_key)


def get_llm_provider() -> LLMProvider:
    from app.core.config import settings
    if settings.OPENAI_API_KEY:
        client = _cached_openai_client(settings.OPENAI_API_KEY)
        return OpenAILLMProvider(settings.OPENAI_API_KEY, settings.OPENAI_MODEL, client=client)
    return MockLLMProvider()
