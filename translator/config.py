"""
Application configuration.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Config:
    """
    Global application configuration.
    """

    source_language: str = "en"
    target_language: str = "pl"

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    batch_size: int = int(os.getenv("BATCH_SIZE", "10"))

    requests_per_minute: int = int(
        os.getenv("REQUESTS_PER_MINUTE", "5")
    )

    input_dir: Path = Path("input")
    output_dir: Path = Path("output")
    cache_dir: Path = Path("cache")
    logs_dir: Path = Path("logs")

    def create_directories(self) -> None:
        for directory in (
            self.input_dir,
            self.output_dir,
            self.cache_dir,
            self.logs_dir,
        ):
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )


config = Config()
config.create_directories()