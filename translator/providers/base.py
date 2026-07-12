"""
Base classes for translation providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(slots=True)
class TranslationItem:
    id: int
    text: str


@dataclass(slots=True)
class BatchRequest:
    items: list[TranslationItem] = field(default_factory=list)


@dataclass(slots=True)
class TranslationResult:
    id: int
    original: str
    translated: str
    success: bool = True
    error: str = ""


class TranslationProvider(ABC):

    name = "base"

    # Czy provider korzysta z zewnętrznego API?
    requires_rate_limit = False

    @abstractmethod
    def translate_batch(
        self,
        request: BatchRequest,
    ) -> list[TranslationResult]:
        raise NotImplementedError