"""SQLite persistence for exercise rounds (played/guessed chord, pool context)."""

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone

from ear_trainer.config import DATABASE_PATH


@dataclass(frozen=True)
class RoundRecord:
    timestamp: datetime
    played: str
    guessed: str
    pool_size: int
    pool: list[str]

    @property
    def correct(self) -> bool:
        return self.played == self.guessed


def _connect() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                exercise TEXT NOT NULL,
                played TEXT NOT NULL,
                guessed TEXT NOT NULL,
                pool_size INTEGER NOT NULL,
                pool_json TEXT NOT NULL
            )
            """
        )


def record_round(exercise: str, played: str, guessed: str, pool: list[str]) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO rounds (timestamp, exercise, played, guessed, pool_size, pool_json) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(),
                exercise,
                played,
                guessed,
                len(pool),
                json.dumps(pool),
            ),
        )


def fetch_rounds(exercise: str) -> list[RoundRecord]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT timestamp, played, guessed, pool_size, pool_json FROM rounds "
            "WHERE exercise = ? ORDER BY timestamp ASC",
            (exercise,),
        ).fetchall()
    return [
        RoundRecord(
            timestamp=datetime.fromisoformat(timestamp),
            played=played,
            guessed=guessed,
            pool_size=pool_size,
            pool=json.loads(pool_json),
        )
        for timestamp, played, guessed, pool_size, pool_json in rows
    ]


init_db()
