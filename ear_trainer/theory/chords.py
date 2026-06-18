"""Chord construction: build common chord qualities directly on a given root."""

from dataclasses import dataclass

from ear_trainer.theory.notes import transpose

# Quality -> chord tone intervals in semitones from the root (root itself implied).
QUALITY_INTERVALS = {
    "maj": (4, 7),
    "min": (3, 7),
    "dim": (3, 6),
    "sus2": (2, 7),
    "sus4": (5, 7),
    "dom7": (4, 7, 10),
}

# The qualities shown for a selected root, in display order. Extend this list to add more
# (e.g. m7, maj7, diminished, augmented) without changing how chords are built.
DEFAULT_QUALITIES = ["maj", "min", "sus2", "sus4", "dom7"]

_QUALITY_SUFFIX = {"maj": "", "min": "m", "dim": "dim", "sus2": "sus2", "sus4": "sus4", "dom7": "7"}


@dataclass(frozen=True)
class Chord:
    root: str
    quality: str

    @property
    def name(self) -> str:
        return f"{self.root}{_QUALITY_SUFFIX[self.quality]}"

    @property
    def notes(self) -> tuple[str, ...]:
        return (self.root, *(transpose(self.root, i) for i in QUALITY_INTERVALS[self.quality]))


def chords_for_root(root: str) -> list[Chord]:
    """The curated set of common chords built directly on `root` (no scale/key context)."""
    return [Chord(root=root, quality=quality) for quality in DEFAULT_QUALITIES]
