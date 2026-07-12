"""
Command Line Interface.
"""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from translator.config import config
from translator.engine import TranslatorEngine
from translator.po import POFile
from translator.providers import get

# Rejestracja providerów
import translator.providers.dummy  # noqa: F401

console = Console()


@click.command()
@click.argument(
    "input_file",
    type=click.Path(
        exists=True,
        dir_okay=False,
        path_type=Path,
    ),
)
@click.option(
    "--provider",
    default="dummy",
    show_default=True,
)
@click.option(
    "--output",
    type=click.Path(
        dir_okay=False,
        path_type=Path,
    ),
)
def main(
    input_file: Path,
    provider: str,
    output: Path | None,
) -> None:

    po = POFile(input_file)

    engine = TranslatorEngine(
        provider=get(provider),
        requests_per_minute=config.requests_per_minute,
    )

    console.print(f"[cyan]Provider:[/cyan] {provider}")
    console.print(f"[cyan]Entries:[/cyan] {po.untranslated}")

    entries = list(po.untranslated_entries())

    batch_size = config.batch_size

    translated = 0

    for start in range(0, len(entries), batch_size):

        batch = entries[start:start + batch_size]

        texts = [e.msgid for e in batch]

        translations = engine.translate_batch(texts)

        for entry, text in zip(batch, translations):
            entry.msgstr = text
            translated += 1

        console.print(
            f"[green]Translated:[/green] {translated}/{po.untranslated}"
        )

    if output is None:
        output = (
            config.output_dir
            / f"{input_file.stem}_translated.po"
        )

    po.save(output)

    console.print()
    console.print(f"[bold green]Saved:[/bold green] {output}")


if __name__ == "__main__":
    main()