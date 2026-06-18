# Feature: Progress

## Overview

A page showing whether the user is actually improving at the Chords exercise over time, even
though practice sessions vary in difficulty (a 2-chord pool is easier to guess right than a
5-chord pool). Naive "% correct" isn't comparable across sessions of different difficulty, so
progress is tracked via a single difficulty-adjusted skill rating instead, plus a breakdown of
which specific chords keep getting confused with which.

## Scope

Tracks the Chords exercise only for now. The data model (`exercise` column) is deliberately
generic so future exercises (notes, intervals, progressions) can share the same `rounds` table
and this same progress page later, without a redesign.

## Data model

SQLite table `rounds` (`ear_trainer/database/rounds.py`), one row per guess:

- `timestamp` — when the round was guessed.
- `exercise` — which exercise produced it (`"chords"` today).
- `played` / `guessed` — chord names.
- `pool_size` / `pool_json` — how many chords were available that round, and the full pool (for
  the confusion breakdown and any future difficulty refinements).

The skill rating is **not** stored — it's recomputed from the raw round log every time the
Progress page loads. This keeps one source of truth and means the rating formula can be tuned
later without corrupting historical data.

## Algorithm: difficulty-adjusted rating

A simplified Elo rating (`ear_trainer/exercises/rating.py`), the same idea adaptive learning
platforms and tests use to compare performance across different difficulty levels:

- Player starts at `rating = 1000`.
- Each round's difficulty ("opponent rating") is derived from that round's pool size:
  `item_rating = 1000 + 200 * log2(pool_size)` — bigger pool = tougher opponent.
- Expected score `E = 1 / (1 + 10 ** ((item_rating - player_rating) / 400))`.
- After the round, `player_rating += 24 * (actual - E)`, where `actual` is 1 (correct) or 0
  (wrong).

Net effect: a correct guess on a hard (big) pool raises the rating more than a correct guess on
an easy (small) pool; a wrong guess on an easy pool drops it more than a wrong guess on a hard
pool. One continuous line is then comparable regardless of which pool size was practiced that
day.

Separately, `confusion_counts()` tallies wrong `(played, guessed)` pairs, most-frequent first —
this is what tells the user *which* chords to focus on; the rating line only tells them *whether
it's working overall*.

## UI

A new page (`pages/progress.py`), separate from the Chords exercise page since this is meant to
span future exercises too:

- **Skill rating over time** — a line chart of the rating after each round.
- **Most confused chord pairs** — a table of wrong-guess pairs and how often each happened.
- If no rounds have been played yet, shows a prompt to go play the Chords exercise first.

## Technical notes

- `ear_trainer/database/rounds.py` — schema, `init_db()` (idempotent, runs at import time),
  `record_round()`, `fetch_rounds()`.
- `ear_trainer/exercises/rating.py` — pure functions (`elo_rating_series`, `confusion_counts`)
  operating on `RoundRecord`s; no database import, so they stay testable in isolation. The UI
  layer (`pages/progress.py`) wires `fetch_rounds()` and the rating functions together.
- `pages/chords.py` calls `record_round()` right alongside the existing in-memory
  `exercise.record_guess()` call, so every guess is persisted as well as shown live on that
  page's scoreboard.

## Open questions

- Whether difficulty should eventually also factor in chord *similarity* within a pool (e.g.
  A vs Am is plausibly harder to distinguish than A vs G), not just pool size.
- Whether the `K` factor and difficulty-scale constants need tuning once there's real usage
  data.
- Whether to add a manual "reset progress" control later, mirroring the existing "Clear
  history" button on the Chords page.
