# PO AI Translator

Professional AI translator for GNU gettext (`.po`) files.

## Features

- Gemini
- OpenAI
- Modular provider architecture
- Clean CLI
- Automatic `.po` handling

## Installation

```bash
pip install -r requirements.txt
```

## Environment

Create a `.env` file:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=gpt-5-mini
```

## Usage

Translate using Gemini:

```bash
python -m translator.cli hrms_pl.po --provider gemini
```

Translate using OpenAI:

```bash
python -m translator.cli hrms_pl.po --provider openai
```

Output:

```
hrms_pl_translated.po
```

## Project structure

```
translator/
    __init__.py
    cli.py
    config.py
    engine.py
    po.py

    providers/
        __init__.py
        base.py
        dummy.py
        gemini.py
        openai.py
```

## License

MIT