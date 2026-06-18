"""Chord construction: qualities, triads, and the diatonic chords of a major key."""

from dataclasses import dataclass

from ear_trainer.theory.notes import transpose
from ear_trainer.theory.scales import major_scale

# Triad quality -> (third interval, fifth interval) in semitones from the root.
TRIAD_INTERVALS = {
    "maj": (4, 7),
    "min": (3, 7),
    "dim": (3, 6),
}

# Quality of each scale-degree triad (I, ii, iii, IV, V, vi, vii) in a major key.
DIATONIC_QUALITIES = ["maj", "min", "min", "maj", "maj", "min", "dim"]
ROMAN_NUMERALS = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]

_QUALITY_SUFFIX = {"maj": "", "min": "m", "dim": "dim"}


@dataclass(frozen=True)
class Chord:
    root: str
    quality: str
    roman_numeral: str

    @property
    def name(self) -> str:
        return f"{self.root}{_QUALITY_SUFFIX[self.quality]}"

    @property
    def notes(self) -> tuple[str, str, str]:
        third, fifth = TRIAD_INTERVALS[self.quality]
        return (self.root, transpose(self.root, third), transpose(self.root, fifth))


def diatonic_triads(key_root: str) -> list[Chord]:
    """The 7 diatonic triads of the major key rooted at `key_root`."""
    scale = major_scale(key_root)
    return [
        Chord(root=scale[degree], quality=DIATONIC_QUALITIES[degree], roman_numeral=ROMAN_NUMERALS[degree])
        for degree in range(7)
    ]
