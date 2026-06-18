"""Progress page.

Shows a difficulty-adjusted skill rating over time, plus which chords get
confused with which. See specs/progress/progress.md for the full spec.
"""

import pandas as pd
import streamlit as st

from ear_trainer.database.rounds import fetch_rounds
from ear_trainer.exercises.rating import confusion_counts, elo_rating_series

st.set_page_config(page_title="Progress — Ear Trainer", page_icon="📈", layout="wide")
st.title("📈 Progress")

rounds = fetch_rounds("chords")

if not rounds:
    st.caption("No rounds played yet — head to the Chords page and start guessing.")
else:
    st.subheader("Skill rating over time")
    series = elo_rating_series(rounds)
    df = pd.DataFrame(series, columns=["timestamp", "rating"]).set_index("timestamp")
    st.line_chart(df)
    st.caption(
        "Rating rises more for a correct guess on a bigger chord pool (harder) than a "
        "smaller one (easier), so sessions of different difficulty are comparable on one line."
    )

    st.subheader("Most confused chord pairs")
    pairs = confusion_counts(rounds)
    if not pairs:
        st.caption("No wrong guesses yet — nice.")
    else:
        st.dataframe(
            pd.DataFrame(
                [{"Played": played, "Guessed as": guessed, "Times": count} for (played, guessed), count in pairs]
            ),
            hide_index=True,
        )
