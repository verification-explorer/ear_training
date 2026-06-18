"""Chord construction: build common chord qualities directly on a given root."""

from dataclasses import dataclass

from ear_trainer.theory.notes import transpose

# Quality -> (interval to 2nd chord tone, interval to 3rd chord tone) in semitones from the root.
QUALITY_INTERVALS = {
    "maj": (4, 7),
    "min": (3, 7),
    "dim": (3, 6),
    "sus2": (2, 7),
    "sus4": (5, 7),
}

# The qualities shown for a selected root, in display order. Extend this list to add more
# (e.g. 7ths, diminished, augmented) without changing how chords are built.
DEFAULT_QUALITIES = ["maj", "min", "sus2", "sus4"]

_QUALITY_SUFFIX = {"maj": "", "min": "m", "dim": "dim", "sus2": "sus2", "sus4": "sus4"}


@dataclass(frozen=True)
class Chord:
    root: str
    quality: str

    @property
    def name(self) -> str:
        return f"{self.root}{_QUALITY_SUFFIX[self.quality]}"

    @property
    def notes(self) -> tuple[str, str, str]:
        second, third = QUALITY_INTERVALS[self.quality]
        return (self.root, transpose(self.root, second), transpose(self.root, third))


def chords_for_root(root: str) -> list[Chord]:
    """The curated set of common chords built directly on `root` (no scale/key context)."""
    return [Chord(root=root, quality=quality) for quality in DEFAULT_QUALITIES]
