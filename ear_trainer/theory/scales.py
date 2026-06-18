"""Scale construction."""

from ear_trainer.theory.notes import transpose

MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]


def major_scale(root: str) -> list[str]:
    """The 7 notes of the major scale starting at `root`."""
    return [transpose(root, interval) for interval in MAJOR_SCALE_INTERVALS]
