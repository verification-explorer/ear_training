"""Chord-identification exercise: round selection, guessing, and scoring."""

import random
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoundResult:
    played: str
    guessed: str

    @property
    def correct(self) -> bool:
        return self.played == self.guessed


@dataclass
class ChordExercise:
    history: list[RoundResult] = field(default_factory=list)

    def pick_next(self, pool: list[str]) -> str:
        """Pick a random chord from `pool` (the same chord can come up twice in a row)."""
        return random.choice(pool)

    def record_guess(self, played: str, guessed: str) -> RoundResult:
        result = RoundResult(played=played, guessed=guessed)
        self.history.insert(0, result)
        return result

    @property
    def tally(self) -> tuple[int, int]:
        correct = sum(1 for r in self.history if r.correct)
        return correct, len(self.history)
