"""Ear Trainer — Streamlit entry point.

Run with:
    streamlit run app.py

This is the app's home page. Individual exercises will live as separate pages
in the `pages/` directory and as logic in the `ear_trainer/` package.
"""

import streamlit as st

st.set_page_config(
    page_title="Ear Trainer",
    page_icon="🎸",
    layout="centered",
)

st.title("🎸 Ear Trainer")
st.subheader("Train your ears, level up your guitar playing.")

st.write(
    "Welcome! This app will play notes, chords, and progressions for you to "
    "identify by ear — and track your progress over time."
)

st.info("🚧 Under construction. Features are coming soon.", icon="🚧")
