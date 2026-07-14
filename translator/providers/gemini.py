"""
Gemini translation provider.
"""

from __future__ import annotations

import json

from google import genai
from google.genai import types

from translator.config import config
from translator.providers import register
from translator.providers.base import (
    BatchRequest,
    TranslationProvider,
    TranslationResult,
)


class GeminiProvider(TranslationProvider):
    """
    Google Gemini translation provider.
    """

    name = "gemini"
    requires_rate_limit = True

    SYSTEM_PROMPT = """
You are a professional software localization translator.

Translate software interface strings from English to Polish.

Rules:

- Return ONLY JSON.
- Do not add explanations.
- Do not translate placeholders.
- Preserve HTML.
- Preserve whitespace.
- Preserve punctuation.
- Use natural ERP terminology.

Return:

[
  {
    "id": 1,
    "translation": "Klient"
  }
]
"""

    def __init__(self) -> None:

        if not config.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=config.gemini_api_key,
        )

    def translate_batch(
        self,
        request: BatchRequest,
    ) -> list[TranslationResult]:

        payload = [
            {
                "id": item.id,
                "text": item.text,
            }
            for item in request.items
        ]

        response = self.client.models.generate_content(
            model=config.gemini_model,
            contents=[
                self.SYSTEM_PROMPT,
                json.dumps(
                    payload,
                    ensure_ascii=False,
                ),
            ],
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return self._parse_response(
            request,
            response.text,
        )
    def _parse_response(
        self,
        request: BatchRequest,
        response_text: str,
    ) -> list[TranslationResult]:
        """
        Parse Gemini JSON response into TranslationResult objects.
        """

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Gemini returned invalid JSON:\n{response_text}"
            ) from exc

        if not isinstance(data, list):
            raise RuntimeError(
                "Gemini response must be a JSON array."
            )

        translations: dict[int, str] = {}

        for item in data:

            if not isinstance(item, dict):
                continue

            item_id = item.get("id")
            translation = item.get("translation")

            if (
                isinstance(item_id, int)
                and isinstance(translation, str)
            ):
                translations[item_id] = translation

        results: list[TranslationResult] = []

        for source in request.items:

            translated = translations.get(source.id)

            if translated is None:
                results.append(
                    TranslationResult(
                        id=source.id,
                        original=source.text,
                        translated=source.text,
                        success=False,
                        error="Missing translation.",
                    )
                )
            else:
                results.append(
                    TranslationResult(
                        id=source.id,
                        original=source.text,
                        translated=translated,
                        success=True,
                    )
                )

        return results


register(GeminiProvider)        