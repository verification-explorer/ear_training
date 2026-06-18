# Ear Trainer 🎸👂

A free, open-source ear training app for guitar players, built with Python + Streamlit.

Play notes, chords, and progressions, guess what you hear, get scored, and track your
improvement over time. Made for beginner guitarists who want to train their ears without
paying for expensive apps.

## Status

🚧 Early-stage skeleton — `theory`, `audio`, `exercises`, and `database` are placeholders
with no implementation yet. The app currently runs as a bare Streamlit shell.

## Features

> Coming soon — features are still being designed. The current code is a project skeleton.

## Project structure

```
ear_training/
├── app.py                  # Streamlit entry point (run this)
├── requirements.txt        # Python dependencies
├── pages/                  # Additional Streamlit pages (multipage app)
├── ear_trainer/            # Application package (the "brains", UI-agnostic)
│   ├── config.py           # Paths & app-wide settings
│   ├── theory/             # Music theory: notes, intervals, chords, scales
│   ├── audio/              # Sound synthesis & playback (notes -> audio)
│   ├── exercises/          # Exercise definitions & scoring logic
│   └── database/           # SQLite storage for sessions & progress
├── assets/                 # Static assets (e.g. SoundFont instrument samples)
├── data/                   # Local SQLite database (gitignored)
└── tests/                  # Unit tests
```

## Getting started

```bash
# 1. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens in your browser at http://localhost:8501.

## License

MIT — free to use, learn from, and improve.
