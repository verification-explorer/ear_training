"""Chords exercise page.

Pick a root note, build a pool of chords to be quizzed on, then guess each
chord the app plays back. See specs/chords/chords.md for the full spec.
"""

import numpy as np
import streamlit as st

from ear_trainer.audio.playback import to_wav_bytes
from ear_trainer.audio.soundfont import render_strum, warm_up
from ear_trainer.config import SAMPLE_RATE
from ear_trainer.exercises.chords import ChordExercise
from ear_trainer.theory.chords import Chord, chords_for_root
from ear_trainer.theory.notes import NOTE_NAMES
from ear_trainer.theory.shapes import get_shape, shape_to_midi_notes

st.set_page_config(page_title="Chords — Ear Trainer", page_icon="🎸", layout="wide")
st.title("🎸 Chords")

if "warmed_up" not in st.session_state:
    # Streamlit runs each browser session in its own worker thread; warm up
    # FluidSynth in this session's thread, once, before any real chord is
    # rendered. Confirmed necessary together with the lead-in padding below
    # and the always-mounted audio element — don't strip any of the three
    # without the user re-testing live audio first.
    warm_up()
    st.session_state.warmed_up = True

if "pool" not in st.session_state:
    st.session_state.pool: list[Chord] = []
if "exercise" not in st.session_state:
    st.session_state.exercise = ChordExercise()
if "selected_root" not in st.session_state:
    st.session_state.selected_root = "A"
if "simple_mode" not in st.session_state:
    st.session_state.simple_mode = False
if "current_chord" not in st.session_state:
    st.session_state.current_chord: Chord | None = None
if "audio_nonce" not in st.session_state:
    st.session_state.audio_nonce = 0
if "current_audio" not in st.session_state:
    # Seed with a real silent clip so the <audio> element mounts once, here,
    # rather than on the user's first real Play — never reset this to None
    # afterward (see the tray click handler below); a freshly-mounted
    # element has one-time browser startup latency that can clip the start
    # of playback, so the element must persist across the whole session.
    st.session_state.current_audio: bytes = to_wav_bytes(
        np.zeros((SAMPLE_RATE // 2, 2), dtype=np.float32)
    )

pool: list[Chord] = st.session_state.pool
exercise: ChordExercise = st.session_state.exercise


def _toggle_chord(chord: Chord) -> None:
    if any(c.name == chord.name for c in pool):
        st.session_state.pool = [c for c in pool if c.name != chord.name]
    else:
        st.session_state.pool = [*pool, chord]


_LEAD_IN_SECONDS = 0.2


def _play_chord(chord: Chord) -> bytes:
    """Render `chord` to WAV bytes.

    Prepends a brief silent lead-in: on the first playback in a browser
    session, there's a gap between the player's progress bar starting and
    audible sound actually arriving (confirmed by watching the bar vs. the
    sound) — the start of the real clip gets swallowed by browser playback
    startup latency. Padding the front with silence means that latency eats
    silence instead of the chord's attack.

    Also appends a few inaudible trailing-silence frames that vary each
    call, so repeated plays of the same chord produce distinct bytes —
    otherwise the audio widget sees identical data and the browser won't
    restart playback (no audible "repeat").
    """
    st.session_state.audio_nonce += 1
    midi_notes = shape_to_midi_notes(get_shape(chord))
    samples = render_strum(midi_notes)
    lead_in = np.zeros((int(_LEAD_IN_SECONDS * SAMPLE_RATE), samples.shape[1]), dtype=samples.dtype)
    trail_padding = np.zeros((st.session_state.audio_nonce % 5 + 1, samples.shape[1]), dtype=samples.dtype)
    return to_wav_bytes(np.concatenate([lead_in, samples, trail_padding]))


left, middle, right = st.columns([1, 3, 1])

with left:
    st.subheader("Root")
    for note in NOTE_NAMES:
        if st.button(note, key=f"root_{note}", use_container_width=True):
            st.session_state.selected_root = note

with middle:
    st.subheader("Chords")
    toggle_label = "Simple chords" if not st.session_state.simple_mode else "All chords"
    if st.button(toggle_label, key="quality_toggle"):
        st.session_state.simple_mode = not st.session_state.simple_mode
        st.rerun()

    root = st.session_state.selected_root
    if root is None:
        st.caption("Pick a root note to see its common chords.")
    else:
        chords = chords_for_root(root)
        if st.session_state.simple_mode:
            chords = [c for c in chords if c.quality in ("maj", "min")]
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
        if st.button("🧹 Clear all", key="clear_all"):
            st.session_state.pool = []
            st.session_state.current_chord = None
            st.rerun()

        tray_cols = st.columns(len(pool) + 1)
        for col, chord in zip(tray_cols[:-1], pool):
            with col:
                guessing = st.session_state.current_chord is not None
                if st.button(chord.name, key=f"tray_{chord.name}"):
                    if guessing:
                        result = exercise.record_guess(
                            played=st.session_state.current_chord.name, guessed=chord.name
                        )
                        st.session_state.current_chord = None
                        if result.correct:
                            st.toast(f"Correct! It was {result.played}.", icon="✅")
                        else:
                            st.toast(f"Wrong — that was {result.played}, you guessed {result.guessed}.", icon="❌")
                    else:
                        st.session_state.current_audio = _play_chord(chord)
                    st.rerun()
        with tray_cols[-1]:
            play_label = "🔁 Repeat" if st.session_state.current_chord is not None else "▶ Play"
            if st.button(play_label, key="play_button", disabled=not pool):
                if st.session_state.current_chord is None:
                    next_name = exercise.pick_next([c.name for c in pool])
                    st.session_state.current_chord = next(c for c in pool if c.name == next_name)
                st.session_state.current_audio = _play_chord(st.session_state.current_chord)
                st.rerun()

    st.audio(st.session_state.current_audio, format="audio/wav", autoplay=True)

with right:
    st.subheader("Scoreboard")
    correct, total = exercise.tally
    st.metric("Score", f"{correct}/{total}")
    if exercise.history and st.button("🧹 Clear history", key="clear_history"):
        exercise.history.clear()
        st.rerun()
    for r in exercise.history:
        icon = "✅" if r.correct else "❌"
        st.write(f"{icon} played **{r.played}**, guessed **{r.guessed}**")
