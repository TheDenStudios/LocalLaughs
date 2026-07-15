from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask

SCHEMA = """
CREATE TABLE IF NOT EXISTS jokes (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    setup TEXT NOT NULL,
    punchline TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '[]',
    safe INTEGER NOT NULL DEFAULT 1,
    language TEXT NOT NULL DEFAULT 'en',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_jokes_category ON jokes(category);
CREATE INDEX IF NOT EXISTS idx_jokes_language ON jokes(language);
CREATE INDEX IF NOT EXISTS idx_jokes_safe ON jokes(safe);
"""


def init_database(app: Flask) -> None:
    db_path = Path(app.config["JOKES_DB"])
    seed_path = Path(app.config["SEED_FILE"])
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with connect(db_path) as db:
        db.executescript(SCHEMA)
        if _is_empty(db) and seed_path.exists():
            _seed(db, seed_path)


def connect(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db


def row_to_joke(row: sqlite3.Row) -> dict[str, Any]:
    joke = dict(row)
    joke["tags"] = json.loads(joke.get("tags") or "[]")
    joke["safe"] = bool(joke.get("safe", 1))
    return joke


def encode_tags(tags: list[str] | None) -> str:
    return json.dumps(tags or [])


def _is_empty(db: sqlite3.Connection) -> bool:
    row = db.execute("SELECT COUNT(*) AS count FROM jokes").fetchone()
    return int(row["count"]) == 0


def _seed(db: sqlite3.Connection, seed_path: Path) -> None:
    jokes = json.loads(seed_path.read_text(encoding="utf-8"))
    for joke in jokes:
        db.execute(
            """
            INSERT OR IGNORE INTO jokes
                (id, category, setup, punchline, tags, safe, language)
            VALUES
                (:id, :category, :setup, :punchline, :tags, :safe, :language)
            """,
            {
                "id": joke["id"],
                "category": joke["category"],
                "setup": joke["setup"],
                "punchline": joke["punchline"],
                "tags": encode_tags(joke.get("tags", [])),
                "safe": 1 if joke.get("safe", True) else 0,
                "language": joke.get("language", "en"),
            },
        )
