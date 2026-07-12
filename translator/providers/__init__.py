"""
Translation provider registry.
"""

from __future__ import annotations

from translator.providers.base import TranslationProvider

_PROVIDERS: dict[str, type[TranslationProvider]] = {}


def register(provider: type[TranslationProvider]) -> None:
    _PROVIDERS[provider.name] = provider


# Import providerów - powoduje ich rejestrację
import translator.providers.dummy  # noqa: E402,F401


def get(name: str) -> TranslationProvider:
    try:
        return _PROVIDERS[name]()
    except KeyError as exc:
        available = ", ".join(sorted(_PROVIDERS))
        raise ValueError(
            f"Unknown provider '{name}'. Available: {available}"
        ) from exc


def available() -> list[str]:
    return sorted(_PROVIDERS)