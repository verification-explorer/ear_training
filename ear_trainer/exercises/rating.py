"""Difficulty-adjusted skill rating and confusion analytics over round history.

Pure functions over `RoundRecord`s (from `ear_trainer.database.rounds`) — no database import
here, so this stays testable in isolation; the UI layer wires fetch + compute together.
"""

import math
from collections import Counter

from ear_trainer.database.rounds import RoundRecord

STARTING_RATING = 1000.0
K_FACTOR = 24.0
DIFFICULTY_SCALE = 200.0


def _item_rating(pool_size: int) -> float:
    """Harder (bigger) pools are treated as a tougher "opponent" to beat."""
    return STARTING_RATING + DIFFICULTY_SCALE * math.log2(max(pool_size, 1))


def elo_rating_series(rounds: list[RoundRecord]) -> list[tuple[object, float]]:
    """Player's skill rating after each round, recomputed from the raw log each time."""
    rating = STARTING_RATING
    series = []
    for round_ in rounds:
        item_rating = _item_rating(round_.pool_size)
        expected = 1 / (1 + 10 ** ((item_rating - rating) / 400))
        actual = 1.0 if round_.correct else 0.0
        rating += K_FACTOR * (actual - expected)
        series.append((round_.timestamp, rating))
    return series


def confusion_counts(rounds: list[RoundRecord]) -> list[tuple[tuple[str, str], int]]:
    """Wrong-guess (played, guessed) pairs, most frequent first."""
    counts = Counter((r.played, r.guessed) for r in rounds if not r.correct)
    return counts.most_common()
