"""
PO file handling.
"""

from __future__ import annotations

from pathlib import Path

import polib


class POFile:

    def __init__(self, filename: str | Path):

        self.path = Path(filename)
        self.po = polib.pofile(str(self.path))

    def untranslated_entries(self):

        for entry in self.po:

            if entry.obsolete:
                continue

            if not entry.msgid.strip():
                continue

            if entry.msgstr.strip():
                continue

            yield entry

    @property
    def total(self):

        return len(self.po)

    @property
    def translated(self):

        return sum(
            1
            for e in self.po
            if e.msgstr.strip()
        )

    @property
    def untranslated(self):

        return sum(
            1
            for e in self.po
            if e.msgid.strip()
            and not e.msgstr.strip()
            and not e.obsolete
        )

    def save(self, filename):

        self.po.save(str(filename))