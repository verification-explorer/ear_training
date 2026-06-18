"""Chromatic note names and pitch-class arithmetic."""

NOTE_NAMES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def pitch_class(note_name: str) -> int:
    return NOTE_NAMES.index(note_name)


def note_name(pitch_class_value: int) -> str:
    return NOTE_NAMES[pitch_class_value % 12]


def transpose(note_name_: str, semitones: int) -> str:
    return note_name(pitch_class(note_name_) + semitones)
