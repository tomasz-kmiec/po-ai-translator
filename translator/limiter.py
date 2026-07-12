"""
Simple rate limiter.

Ensures we don't exceed the configured requests-per-minute limit.
"""

from __future__ import annotations

import time
from collections import deque


class RateLimiter:
    """
    Sliding-window rate limiter.
    """

    def __init__(self, requests_per_minute: int) -> None:
        if requests_per_minute <= 0:
            raise ValueError("requests_per_minute must be > 0")

        self.requests_per_minute = requests_per_minute
        self._history: deque[float] = deque()

    def wait(self) -> None:
        """
        Wait until another request may be executed.
        """

        now = time.monotonic()

        while self._history and now - self._history[0] >= 60:
            self._history.popleft()

        if len(self._history) >= self.requests_per_minute:
            sleep_time = 60 - (now - self._history[0])

            if sleep_time > 0:
                print(
                    f"\n[INFO] Rate limit reached. Waiting {sleep_time:.1f} seconds...\n"
                )
                time.sleep(sleep_time)

            now = time.monotonic()

            while self._history and now - self._history[0] >= 60:
                self._history.popleft()

        self._history.append(time.monotonic())