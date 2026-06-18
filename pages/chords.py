"""Chords exercise page.

Pick a root note, build a pool of chords to be quizzed on, then guess each
chord the app plays back. See specs/chords/chords.md for the full spec.
"""

import streamlit as st

from ear_trainer.audio.playback import to_wav_bytes
from ear_trainer.audio.soundfont import render_strum
from ear_trainer.exercises.chords import ChordExercise
from ear_trainer.theory.chords import Chord, chords_for_root
from ear_trainer.theory.notes import NOTE_NAMES
from ear_trainer.theory.shapes import get_shape, shape_to_midi_notes

st.set_page_config(page_title="Chords — Ear Trainer", page_icon="🎸", layout="wide")
st.title("🎸 Chords")

if "pool" not in st.session_state:
    st.session_state.pool: list[Chord] = []
if "exercise" not in st.session_state:
    st.session_state.exercise = ChordExercise()
if "selected_root" not in st.session_state:
    st.session_state.selected_root = None
if "current_chord" not in st.session_state:
    st.session_state.current_chord: Chord | None = None
if "current_audio" not in st.session_state:
    st.session_state.current_audio: bytes | None = None

pool: list[Chord] = st.session_state.pool
exercise: ChordExercise = st.session_state.exercise


def _toggle_chord(chord: Chord) -> None:
    if any(c.name == chord.name for c in pool):
        st.session_state.pool = [c for c in pool if c.name != chord.name]
    else:
        st.session_state.pool = [*pool, chord]


def _play_chord(chord: Chord) -> bytes:
    midi_notes = shape_to_midi_notes(get_shape(chord))
    samples = render_strum(midi_notes)
    return to_wav_bytes(samples)


left, middle, right = st.columns([1, 3, 1])

with left:
    st.subheader("Root")
    for note in NOTE_NAMES:
        if st.button(note, key=f"root_{note}", use_container_width=True):
            st.session_state.selected_root = note

with middle:
    st.subheader("Chords")
    root = st.session_state.selected_root
    if root is None:
        st.caption("Pick a root note to see its common chords.")
    else:
        chords = chords_for_root(root)
        cols = st.columns(len(chords))
        pool_names = {c.name for c in pool}
        for col, chord in zip(cols, chords):
            with col:
                selected = chord.name in pool_names
                if st.button(
                    chord.name,
                    key=f"chord_{root}_{chord.name}",
                    type="primary" if selected else "secondary",
                ):
                    _toggle_chord(chord)
                    st.rerun()

    st.divider()
    st.subheader("Selected chords")
    pool = st.session_state.pool
    if not pool:
        st.caption("No chords selected yet.")
    else:
        tray_cols = st.columns(len(pool) + 1)
        for col, chord in zip(tray_cols[:-1], pool):
            with col:
                guessing = st.session_state.current_chord is not None
                if st.button(chord.name, key=f"tray_{chord.name}", disabled=not guessing):
                    result = exercise.record_guess(
                        played=st.session_state.current_chord.name, guessed=chord.name
                    )
                    st.session_state.current_chord = None
                    st.session_state.current_audio = None
                    if result.correct:
                        st.toast(f"Correct! It was {result.played}.", icon="✅")
                    else:
                        st.toast(f"Wrong — that was {result.played}, you guessed {result.guessed}.", icon="❌")
                    st.rerun()
        with tray_cols[-1]:
            if st.button("▶ Play", key="play_button", disabled=not pool):
                if st.session_state.current_chord is None:
                    next_name = exercise.pick_next([c.name for c in pool])
                    st.session_state.current_chord = next(c for c in pool if c.name == next_name)
                st.session_state.current_audio = _play_chord(st.session_state.current_chord)
                st.rerun()

    if st.session_state.current_audio:
        st.audio(st.session_state.current_audio, format="audio/wav", autoplay=True)

with right:
    st.subheader("Scoreboard")
    correct, total = exercise.tally
    st.metric("Score", f"{correct}/{total}")
    for r in exercise.history:
        icon = "✅" if r.correct else "❌"
        st.write(f"{icon} played **{r.played}**, guessed **{r.guessed}**")
