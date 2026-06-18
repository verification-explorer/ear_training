# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

The **Chords** exercise (`pages/chords.py` + `ear_trainer/theory`, `ear_trainer/audio`,
`ear_trainer/exercises`) is implemented and working — see `specs/chords/chords.md` for the
full feature spec. `ear_trainer/database` is still a docstring placeholder with no
implementation; no exercise persists data yet (scoring is in-memory only, reset on restart).

Features live under `specs/<feature>/<feature>.md` (one directory per feature, e.g.
`specs/chords/chords.md`). When building a new exercise, add its spec there following the same
structure (Overview, Scope, UI layout, Game flow, vocabulary/voicing or equivalent, Technical
notes, Open questions) before or alongside implementation.

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
framework is wired up otherwise. So far, verification has been done ad hoc via
`streamlit.testing.v1.AppTest` click-throughs and booting the real app — see commit history
on `pages/chords.py` for the pattern.

### Audio dependency

Chord playback uses SoundFont synthesis via `pyfluidsynth` (in `requirements.txt`), which
needs the system `libfluidsynth` library installed. `ear_trainer/config.py` resolves
`SOUNDFONT_PATH` by checking `assets/soundfonts/*.sf2` first, then falling back to system
soundfonts (FluidR3 GM, installed via `sudo apt-get install fluid-soundfont-gm` — much better
quality than the tiny default `TimGM6mb.sf2` some systems ship with).

## Architecture

The app is a Streamlit multipage app split into a UI layer and a UI-agnostic logic package:

- `app.py` — Streamlit entry point / home page.
- `pages/` — additional Streamlit pages (Streamlit's multipage convention: each file here
  becomes a page, run via `streamlit run app.py`). Currently: `chords.py`.
- `ear_trainer/` — the "brains" of the app, intentionally decoupled from Streamlit so the same
  logic could power a different front-end later:
  - `theory/` — pure music theory logic, no audio or UI:
    - `notes.py` — chromatic note names and pitch-class arithmetic.
    - `scales.py` — major scale construction.
    - `chords.py` — `Chord` dataclass, `QUALITY_INTERVALS` (root-relative semitone intervals
      per quality — generalized to variable-length tuples, not fixed-size triads),
      `DEFAULT_QUALITIES` (the ordered list of qualities shown per root; append to extend),
      `chords_for_root()`.
    - `shapes.py` — maps a `Chord` to a guitar fret-per-string voicing: curated open-position
      shapes first, then movable E-shape/A-shape barre templates (`_E_SHAPE_OFFSETS`/
      `_A_SHAPE_OFFSETS`, keyed by quality), then a generic nearest-fret-per-string fallback
      for anything else.
  - `audio/` — turns `theory` output into audio. Depends on `theory`.
    - `soundfont.py` — renders a strummed chord via `pyfluidsynth`; `warm_up()` must be called
      once per Streamlit session (see `pages/chords.py`) to avoid a glitchy first render.
    - `playback.py` — numpy samples → WAV bytes for `st.audio`.
  - `exercises/` — exercise round/scoring logic. Depends on `theory` and `audio`.
    - `chords.py` — `ChordExercise`: random chord selection from a pool, guess recording,
      running history and tally.
  - `database/` — still a placeholder. Future home for SQLite persistence of sessions/scores.
  - `config.py` — single source of truth for filesystem paths (`ROOT_DIR`, `ASSETS_DIR`,
    `DATA_DIR`, `DATABASE_PATH`, `SOUNDFONT_PATH`) and app-wide constants (`SAMPLE_RATE`,
    `GUITAR_PROGRAM`, `STRUM_DELAY_SECONDS`, `NOTE_SUSTAIN_SECONDS`). Other modules should
    import paths/settings from here rather than hardcoding them.
- `assets/soundfonts/` — optional bundled SoundFont samples (gitignored contents; only
  `.gitkeep` tracked) — checked before system soundfonts, see `config.SOUNDFONT_PATH`.
- `data/` — local SQLite DB file, created on first use at runtime (gitignored, unused so far).
- `specs/<feature>/` — one spec doc per feature (e.g. `specs/chords/chords.md`). Check here for
  the intended UI/UX and design decisions before changing exercise behavior.

Expected dependency direction: `theory` → `audio`/`exercises` → `database`/UI. Keep `theory` free of
audio and Streamlit imports so it stays UI-agnostic per the stated design intent.

## Streamlit-specific gotchas learned on this project

- **Stale local variables across `st.rerun()`**: if a session-state list is reassigned (not
  mutated in place) inside a callback, re-fetch it from `st.session_state` before using it
  later in the same script run — a local variable captured before the reassignment will be
  stale.
- **Click handlers that change widget-affecting state should `st.rerun()` immediately** — widgets
  rendered earlier in the same run (e.g. a button's `disabled` state) won't reflect state changes
  made later in that same run otherwise.
- **Identical `st.audio` bytes won't replay** — if the same audio data is set twice in a row, the
  browser doesn't restart playback. Vary the bytes slightly (e.g. inaudible trailing padding) if
  the same clip needs to audibly replay.
- **First audio playback in a browser session can clip its start** — there's a real one-time
  browser/FluidSynth warm-up cost; see the lead-in silence padding and `warm_up()` call in
  `pages/chords.py` / `ear_trainer/audio/soundfont.py` before changing that audio pipeline.
