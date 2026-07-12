"""
Translation engine.
"""

from __future__ import annotations

from typing import Iterable

from translator.limiter import RateLimiter
from translator.providers.base import (
    BatchRequest,
    TranslationItem,
    TranslationProvider,
)


class TranslatorEngine:

    def __init__(
        self,
        provider: TranslationProvider,
        requests_per_minute: int,
    ) -> None:

        self.provider = provider
        self.limiter = RateLimiter(requests_per_minute)

    def translate_batch(
        self,
        texts: Iterable[str],
    ) -> list[str]:

        request = BatchRequest()

        for idx, text in enumerate(texts, start=1):
            request.items.append(
                TranslationItem(
                    id=idx,
                    text=text,
                )
            )

        if self.provider.requires_rate_limit:
            self.limiter.wait()

        results = self.provider.translate_batch(request)

        return [r.translated for r in results]