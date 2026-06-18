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

- **Chord root (left, vertical)** — one button per root note (A, B, C, ...). Clicking a
  root treats it as the tonic of a major key.
- **Chords (middle, upper)** — populated after a root is picked, showing the 7 diatonic
  triads of that major key (I, ii, iii, IV, V, vi, vii°), one button each. Clicking a chord
  adds it to the selected tray; it stays clickable to add more chords after picking a
  different root too (selection accumulates across roots).
- **Selected chords (middle, lower)** — tray of every chord added so far. Clicking a chord
  here again removes it from the tray. A **Play** button sits at the right of this row.
- **Scoreboard (right, vertical)** — running history of rounds, newest on top: played chord,
  guessed chord, and correct/wrong, plus a running tally (e.g. "7/10 correct").

## Game flow

1. User selects one or more chords into the tray (via root → chords → tray, as above).
2. User presses **Play**. The app picks one chord at random from the tray and plays it,
   excluding whichever chord was played last (no immediate repeat).
3. User guesses by clicking one of the chords in the tray.
4. The round result (chord played, chord guessed, correct/wrong) is added to the top of the
   scoreboard's history list and the tally updates.
5. Before guessing, the user may press **Play** again to replay the *same* chord that's
   currently up for guessing (does not advance to a new chord).

## Chord vocabulary & voicing

- Chords are the 7 diatonic triads of the major key rooted at the selected note.
- Each chord is voiced as a real, open-position guitar chord shape (like a chord chart),
  not an arbitrary triad in some octave.
- For diatonic chords with no common open-position shape (e.g. some vii° chords, or
  sharp/flat roots), fall back to a barre chord shape or a generic shape covering the same
  notes.
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

- New logic needed in `ear_trainer/theory` (chord/scale/shape data: diatonic triads per
  major key, open-chord-shape lookup table) and `ear_trainer/audio` (SoundFont loading +
  strummed playback), per the dependency direction in `CLAUDE.md` (`theory` →
  `audio`/`exercises`).
- Scoring is in-memory only for this version — no `ear_trainer/database` wiring yet; the
  scoreboard resets on page reload/restart.

## Open questions

- Minimum number of chords that must be selected before the Play button is enabled.
- Exact strum timing (ms between notes) and chord sustain length.
- Which specific free guitar `.sf2` to use — needs sourcing and licensing check.
- Naming/labeling convention for accidentals (e.g. F#m vs Gbm) in keys with flats.
