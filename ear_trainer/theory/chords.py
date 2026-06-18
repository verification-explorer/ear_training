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
    "maj7": (4, 7, 11),
    "min7": (3, 7, 10),
    "maj9": (4, 7, 11, 14),
    "min9": (3, 7, 10, 14),
    "dom11": (4, 7, 10, 14, 17),
    "dom13": (4, 7, 10, 14, 17, 21),
}

# The qualities shown for a selected root, in display order. Extend this list to add more
# without changing how chords are built.
DEFAULT_QUALITIES = [
    "maj", "min", "maj7", "min7", "dom7", "sus4", "sus2", "maj9", "min9", "dom11", "dom13",
]

_QUALITY_SUFFIX = {
    "maj": "",
    "min": "m",
    "dim": "dim",
    "sus2": "sus2",
    "sus4": "sus4",
    "dom7": "7",
    "maj7": "maj7",
    "min7": "m7",
    "maj9": "maj9",
    "min9": "m9",
    "dom11": "11",
    "dom13": "13",
}


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
