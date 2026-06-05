from __future__ import annotations

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "db" / "feedback.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                station TEXT,
                station_en TEXT,
                lat REAL,
                lon REAL,
                category TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                confidence REAL NOT NULL,
                matched_keywords TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def clear_feedback() -> None:
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM feedback")


def save_feedback(result: dict) -> dict:
    init_db()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO feedback (
                text, station, station_en, lat, lon, category, sentiment,
                confidence, matched_keywords
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result["text"],
                result["station"],
                result["station_en"],
                result["lat"],
                result["lon"],
                result["category"],
                result["sentiment"],
                result["confidence"],
                json.dumps(result["matched_keywords"], ensure_ascii=False),
            ),
        )
        row = conn.execute(
            "SELECT * FROM feedback WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return row_to_record(row)


def list_feedback(limit: int | None = None) -> list[dict]:
    init_db()
    query = "SELECT * FROM feedback ORDER BY id DESC"
    params: tuple = ()
    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [row_to_record(row) for row in rows]


def row_to_record(row: sqlite3.Row) -> dict:
    record = dict(row)
    record["matched_keywords"] = json.loads(record["matched_keywords"])
    return record
