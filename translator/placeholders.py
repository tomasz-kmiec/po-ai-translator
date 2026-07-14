"""
Placeholder protection utilities.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class PlaceholderMapping:
    token: str
    value: str


class PlaceholderProtector:
    """
    Protects placeholders from being modified by AI models.
    """

    PATTERNS = (
        r"\{[^\{\}]+\}",              # {0} {name} {price:.2f}
        r"%\([^)]+\)[a-zA-Z]",        # %(name)s
        r"%[sdfoxeg]",                # %s %d %f ...
        r"<[^>]+>",                   # HTML/XML tags
        r"\\n",
        r"\\t",
        r"\\r",
    )

    def __init__(self) -> None:

        self._regex = re.compile(
            "|".join(self.PATTERNS)
        )

    def protect(
        self,
        text: str,
    ) -> tuple[str, list[PlaceholderMapping]]:

        mappings: list[PlaceholderMapping] = []

        def replace(match: re.Match[str]) -> str:

            token = f"__PH_{len(mappings):04d}__"

            mappings.append(
                PlaceholderMapping(
                    token=token,
                    value=match.group(0),
                )
            )

            return token

        protected = self._regex.sub(
            replace,
            text,
        )

        return protected, mappings

    def restore(
        self,
        text: str,
        mappings: list[PlaceholderMapping],
    ) -> str:

        restored = text

        for mapping in mappings:
            restored = restored.replace(
                mapping.token,
                mapping.value,
            )

        return restored

    def validate(
        self,
        original: str,
        translated: str,
    ) -> bool:

        original_items = sorted(
            self._regex.findall(original)
        )

        translated_items = sorted(
            self._regex.findall(translated)
        )

        return original_items == translated_items