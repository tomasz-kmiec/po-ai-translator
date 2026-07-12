"""
Dummy translation provider.
"""

from __future__ import annotations

from translator.providers import register
from translator.providers.base import (
    BatchRequest,
    TranslationProvider,
    TranslationResult,
)


class DummyProvider(TranslationProvider):
    """
    Dummy provider used for testing.
    """

    name = "dummy"
    requires_rate_limit = False

    def translate_batch(
        self,
        request: BatchRequest,
    ) -> list[TranslationResult]:

        return [
            TranslationResult(
                id=item.id,
                original=item.text,
                translated=f"[PL] {item.text}",
                success=True,
            )
            for item in request.items
        ]


register(DummyProvider)