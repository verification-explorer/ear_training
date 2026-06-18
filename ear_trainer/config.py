"""App-wide paths and settings.

Centralizes filesystem locations so the rest of the code never hardcodes paths.
"""

from pathlib import Path

# Repository root (this file is at <root>/ear_trainer/config.py)
ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"

# Local SQLite database file (created on first use)
DATABASE_PATH = DATA_DIR / "ear_trainer.db"

# Audio defaults
SAMPLE_RATE = 44100  # Hz

# SoundFont used to render guitar audio. Prefer one bundled in the repo; fall
# back to a General MIDI soundfont commonly installed at the OS level.
_BUNDLED_SOUNDFONTS = sorted(ASSETS_DIR.glob("soundfonts/*.sf2"))
_SYSTEM_SOUNDFONT_FALLBACKS = [
    Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"),
    Path("/usr/share/sounds/sf2/default-GM.sf2"),
    Path("/usr/share/sounds/sf2/TimGM6mb.sf2"),
]
SOUNDFONT_PATH = next(
    (p for p in [*_BUNDLED_SOUNDFONTS, *_SYSTEM_SOUNDFONT_FALLBACKS] if p.exists()),
    None,
)

# General MIDI program number (0-indexed) for the chord playback instrument.
GUITAR_PROGRAM = 25  # Acoustic Guitar (steel)

# Strum timing
STRUM_DELAY_SECONDS = 0.03
NOTE_SUSTAIN_SECONDS = 1.5
