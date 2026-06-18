# Feature: Chords

## Overview

An ear-training exercise where the user picks which chords to be quizzed on, the app plays
them back in random order on a guitar sound, and the user identifies each chord by ear.
See `specs/chords/ear_train_app.png` for the layout sketch this is based on.

## Scope

This spec covers only the Chords exercise. The diagram's "Chords / Notes / Intervals" tab
switcher is out of scope for now — Notes and Intervals are separate, future features with
their own specs. No stub navigation is needed yet.

## UI layout

Four panels on one screen:

- **Chord root (left, vertical)** — one button per root note (A, B, C, ...).
- **Chords (middle, upper)** — populated after a root is picked, showing a curated set of
  common chords built directly on that root (e.g. root A → A, Am, Asus2, Asus4), one button
  each. No notion of "key" — each chord stands on its own. Clicking a chord adds it to the
  selected tray; it stays clickable to add more chords after picking a different root too
  (selection accumulates across roots).
- **Selected chords (middle, lower)** — tray of every chord added so far. Clicking a chord
  here again removes it from the tray. A **Play** button sits at the right of this row. A
  **Clear all** button above the tray empties it in one click and cancels any round in
  progress.
- **Scoreboard (right, vertical)** — running history of rounds, newest on top: played chord,
  guessed chord, and correct/wrong, plus a running tally (e.g. "7/10 correct"). A
  **Clear history** button (shown once there's history) resets the history and tally.

## Game flow

1. User selects one or more chords into the tray (via root → chords → tray, as above).
2. **Preview**: while no round is active (before the first Play, or right after a guess),
   clicking a chord in the tray just plays that chord — no scoring, no round started. This
   lets the user ear-train on the selected chords before being quizzed on them.
3. User presses **Play**. The app picks one chord at random from the tray and plays it,
   excluding whichever chord was played last (no immediate repeat). This starts a round, and
   the button's label changes to **Repeat**.
4. Once a round is active, clicking a chord in the tray submits it as a guess instead of
   previewing it.
5. The round result (chord played, chord guessed, correct/wrong) is added to the top of the
   scoreboard's history list and the tally updates.
6. While a round is active, the user may press **Repeat** as many times as they want to
   replay the *same* chord that's currently up for guessing (does not advance to a new
   chord). Once a guess is submitted, the round ends and the button reverts to **Play**,
   ready to start the next round.

## Chord vocabulary & voicing

- For a selected root, the chords window shows a curated, expandable list of qualities built
  directly on that root — no scale or key context involved.
- Currently ships 5 qualities: **major, minor, sus2, sus4, dominant 7th** (e.g. root A → A, Am,
  Asus2, Asus4, A7). More qualities (m7, maj7, diminished, augmented, ...) are expected to be
  added later as a simple list extension, not a redesign.
- Each chord is voiced as a real, open-position guitar chord shape (like a chord chart),
  not an arbitrary triad in some octave.
- For root/quality combinations with no common open-position shape, fall back to a barre
  chord shape (major/minor) or a generic shape covering the same notes (everything else).
- Needs a chord-shape data table (root + quality → fret/string positions) living in
  `ear_trainer/theory`.

## Audio

- Played via SoundFont synthesis (`pyfluidsynth`), not numpy-generated tones, since the app
  is for guitar players and should sound like a guitar.
- Notes within a chord are triggered as a staggered **strum** (quick roll), not a
  simultaneous block chord.
- Requires a guitar `.sf2` SoundFont file in `assets/soundfonts/` (currently only a
  `.gitkeep` placeholder) and uncommenting `pyfluidsynth` in `requirements.txt`.

## Technical notes

- New logic needed in `ear_trainer/theory` (chord/quality/shape data: per-root chord
  construction, open-chord-shape lookup table) and `ear_trainer/audio` (SoundFont loading +
  strummed playback), per the dependency direction in `CLAUDE.md` (`theory` →
  `audio`/`exercises`).
- Scoring is in-memory only for this version — no `ear_trainer/database` wiring yet; the
  scoreboard resets on page reload/restart.

## Open questions

- Minimum number of chords that must be selected before the Play button is enabled.
- Exact strum timing (ms between notes) and chord sustain length.
- Naming/labeling convention for accidentals (e.g. F# vs Gb roots).
- Which qualities to add next after dom7 (m7? maj7? diminished? augmented?) and in what order.
