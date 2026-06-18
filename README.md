# Ear Trainer 🎸👂

A free, open-source ear training app for guitar players, built with Python + Streamlit.

Play notes, chords, and progressions, guess what you hear, get scored, and track your
improvement over time. Made for beginner guitarists who want to train their ears without
paying for expensive apps.

## Status

🚧 Early stage, but the first exercise is playable. `database` (progress tracking across
sessions) is still a placeholder — scores reset when you restart the app.

## Features

- **Chords** — pick a root note, build a set of chords to be quizzed on (major, minor, sus2,
  sus4, dominant 7th, maj7, m7, maj9, m9, dom11, dom13), preview them, then guess each one as
  the app plays it back on a real guitar sound. See [`specs/chords/chords.md`](specs/chords/chords.md)
  for the full spec.
- More exercises (notes, intervals, progressions) are planned but not built yet.

## Project structure

```
ear_training/
├── app.py                  # Streamlit entry point (run this)
├── requirements.txt        # Python dependencies
├── pages/                  # Additional Streamlit pages (multipage app)
│   └── chords.py           # The Chords exercise
├── ear_trainer/            # Application package (the "brains", UI-agnostic)
│   ├── config.py           # Paths & app-wide settings
│   ├── theory/             # Music theory: notes, scales, chords, guitar voicings
│   ├── audio/              # SoundFont synthesis & playback (chords -> audio)
│   ├── exercises/          # Exercise round logic & scoring
│   └── database/           # SQLite storage for sessions & progress (not implemented yet)
├── specs/                  # One spec doc per feature, e.g. specs/chords/chords.md
├── assets/soundfonts/      # Optional bundled SoundFont samples (gitignored contents)
├── data/                   # Local SQLite database (gitignored, unused so far)
└── tests/                  # Unit tests (none yet)
```

## Getting started

```bash
# 1. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies (also needs the system libfluidsynth library)
pip install -r requirements.txt

# Optional but recommended: a better-quality GM soundfont than most systems
# ship with by default (used for chord playback)
sudo apt-get install fluid-soundfont-gm   # Debian/Ubuntu

# 3. Run the app
streamlit run app.py
```

The app opens in your browser at http://localhost:8501. The Chords exercise is at
http://localhost:8501/chords.

## License

MIT — free to use, learn from, and improve.
