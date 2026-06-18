"""Convert rendered audio buffers to bytes Streamlit can play."""

from io import BytesIO

import numpy as np
import soundfile as sf

from ear_trainer.config import SAMPLE_RATE


def to_wav_bytes(samples: np.ndarray) -> bytes:
    buffer = BytesIO()
    sf.write(buffer, samples, SAMPLE_RATE, format="WAV")
    return buffer.getvalue()
