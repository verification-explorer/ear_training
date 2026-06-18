"""Guitar voicings: maps a Chord to fret positions on standard-tuned strings.

Strings are ordered low to high (low E, A, D, G, B, high E). A fret of `None`
means the string is muted/not played.

Resolution order:
1. A curated open-position shape, for the handful of chords that have one.
2. A movable barre shape (built from the open-E or open-A template), for any
   other major/minor chord.
3. A generic per-string nearest-fret search, for anything else (e.g. the
   diminished vii° chords, which have no common open or barre shape).
"""

from ear_trainer.theory.chords import TRIAD_INTERVALS, Chord
from ear_trainer.theory.notes import pitch_class

# Low E, A, D, G, B, high E
OPEN_STRING_PITCH_CLASSES = [7, 0, 5, 10, 2, 7]
OPEN_STRING_MIDI = [40, 45, 50, 55, 59, 64]

MAX_FRET_SEARCH = 4

# Hand-played open-position shapes (frets relative to the nut; None = muted).
CURATED_OPEN_SHAPES: dict[str, list[int | None]] = {
    "E": [0, 2, 2, 1, 0, 0],
    "Em": [0, 2, 2, 0, 0, 0],
    "A": [None, 0, 2, 2, 2, 0],
    "Am": [None, 0, 2, 2, 1, 0],
    "D": [None, None, 0, 2, 3, 2],
    "Dm": [None, None, 0, 2, 3, 1],
    "G": [3, 2, 0, 0, 0, 3],
    "C": [None, 3, 2, 0, 1, 0],
}


def _barre_shape(root_pc: int, quality: str) -> list[int | None]:
    """Movable barre chord, built from the open-E or open-A shape template."""
    barre_from_e = (root_pc - OPEN_STRING_PITCH_CLASSES[0]) % 12
    barre_from_a = (root_pc - OPEN_STRING_PITCH_CLASSES[1]) % 12

    if barre_from_e <= barre_from_a:
        b = barre_from_e
        return [b, b + 2, b + 2, b + 1 if quality == "maj" else b, b, b]
    b = barre_from_a
    return [None, b, b + 2, b + 2, b + 2 if quality == "maj" else b + 1, b]


def _generic_shape(chord_tone_pcs: set[int]) -> list[int | None]:
    """Nearest chord-tone fret per string, muting strings with none in range."""
    shape: list[int | None] = []
    for open_pc in OPEN_STRING_PITCH_CLASSES:
        fret = next(
            (f for f in range(MAX_FRET_SEARCH + 1) if (open_pc + f) % 12 in chord_tone_pcs),
            None,
        )
        shape.append(fret)
    return shape


def get_shape(chord: Chord) -> list[int | None]:
    if chord.name in CURATED_OPEN_SHAPES:
        return CURATED_OPEN_SHAPES[chord.name]

    if chord.quality in ("maj", "min"):
        return _barre_shape(pitch_class(chord.root), chord.quality)

    third, fifth = TRIAD_INTERVALS[chord.quality]
    root_pc = pitch_class(chord.root)
    chord_tone_pcs = {root_pc, (root_pc + third) % 12, (root_pc + fifth) % 12}
    return _generic_shape(chord_tone_pcs)


def shape_to_midi_notes(shape: list[int | None]) -> list[int]:
    """MIDI note numbers for a shape, low string to high, skipping muted strings."""
    return [
        OPEN_STRING_MIDI[i] + fret
        for i, fret in enumerate(shape)
        if fret is not None
    ]
