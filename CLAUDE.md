# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

This is an early-stage skeleton. `ear_trainer/theory`, `ear_trainer/audio`, `ear_trainer/exercises`, and
`ear_trainer/database` currently contain only docstring placeholders describing their intended future
content — there is no implementation yet. `app.py` is a placeholder Streamlit home page. When asked to
build features, you are filling in this skeleton rather than refactoring existing logic.

## Commands

```bash
# Activate the existing venv (already created at ./venv)
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

There is no test runner, linter, or CI configured yet. `tests/` exists but is empty
(only `__init__.py`). If you add tests, standard `pytest` conventions apply since no
framework is wired up otherwise.

## Architecture

The app is a Streamlit multipage app split into a UI layer and a UI-agnostic logic package:

- `app.py` — Streamlit entry point / home page.
- `pages/` — additional Streamlit pages (Streamlit's multipage convention: each file here
  becomes a page, run via `streamlit run app.py`).
- `ear_trainer/` — the "brains" of the app, intentionally decoupled from Streamlit so the same
  logic could power a different front-end later:
  - `theory/` — pure music theory logic: notes, intervals, chords, scales. No audio or UI.
  - `audio/` — turns `theory` output (notes/chords) into audio buffers/playback. Depends on `theory`.
  - `exercises/` — defines ear-training exercises (identify note/chord/interval/progression),
    generates questions, scores answers. Depends on `theory` and `audio`.
  - `database/` — SQLite persistence for practice sessions/answers/scores, for progress tracking
    over time.
  - `config.py` — single source of truth for filesystem paths (`ROOT_DIR`, `ASSETS_DIR`,
    `DATA_DIR`, `DATABASE_PATH`) and app-wide constants (e.g. `SAMPLE_RATE`). Other modules should
    import paths/settings from here rather than hardcoding them.
- `assets/soundfonts/` — SoundFont instrument samples (gitignored contents; only `.gitkeep` tracked).
- `data/` — local SQLite DB file, created on first use at runtime (gitignored).

Expected dependency direction: `theory` → `audio`/`exercises` → `database`/UI. Keep `theory` free of
audio and Streamlit imports so it stays UI-agnostic per the stated design intent.
