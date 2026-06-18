"""Render guitar chord shapes to audio via a SoundFont (pyfluidsynth)."""

import fluidsynth
import numpy as np

from ear_trainer.config import (
    GUITAR_PROGRAM,
    NOTE_SUSTAIN_SECONDS,
    SAMPLE_RATE,
    SOUNDFONT_PATH,
    STRUM_DELAY_SECONDS,
)

_RENDER_CHUNK_FRAMES = 256


def render_strum(midi_notes: list[int]) -> np.ndarray:
    """Render a strummed chord (notes triggered low-to-high with a slight roll).

    Returns a float32 array of shape (n_frames, 2) in [-1, 1].
    """
    if SOUNDFONT_PATH is None:
        raise RuntimeError(
            "No SoundFont found. Place a .sf2 file under assets/soundfonts/, "
            "or install a system General MIDI soundfont."
        )

    synth = fluidsynth.Synth(samplerate=SAMPLE_RATE)
    try:
        sfid = synth.sfload(str(SOUNDFONT_PATH))
        synth.program_select(0, sfid, 0, GUITAR_PROGRAM)

        total_seconds = STRUM_DELAY_SECONDS * len(midi_notes) + NOTE_SUSTAIN_SECONDS
        total_frames = int(total_seconds * SAMPLE_RATE)
        note_on_frames = [
            int(i * STRUM_DELAY_SECONDS * SAMPLE_RATE) for i in range(len(midi_notes))
        ]
        pending = sorted(zip(note_on_frames, midi_notes))

        chunks = []
        frame = 0
        while frame < total_frames:
            while pending and pending[0][0] <= frame:
                _, midi_note = pending.pop(0)
                synth.noteon(0, midi_note, 100)
            n = min(_RENDER_CHUNK_FRAMES, total_frames - frame)
            chunks.append(synth.get_samples(n))
            frame += n

        for midi_note in midi_notes:
            synth.noteoff(0, midi_note)
    finally:
        synth.delete()

    samples = np.concatenate(chunks).astype(np.float32) / 32768.0
    return samples.reshape(-1, 2)
