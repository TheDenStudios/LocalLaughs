from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from .database import connect, encode_tags, row_to_joke


@dataclass(frozen=True)
class JokeFilters:
    category: str | None = None
    safe: bool | None = None
    language: str | None = None
    tag: str | None = None


class JokeRepository:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list(self, filters: JokeFilters | None = None) -> list[dict[str, Any]]:
        where, params = self._where(filters)
        with connect(self.path) as db:
            rows = db.execute(
                f"""
                SELECT id, category, setup, punchline, tags, safe, language, created_at, updated_at
                FROM jokes
                {where}
                ORDER BY created_at DESC, id ASC
                """,
                params,
            ).fetchall()
        return [row_to_joke(row) for row in rows]

    def random(self, filters: JokeFilters | None = None) -> dict[str, Any] | None:
        where, params = self._where(filters)
        with connect(self.path) as db:
            row = db.execute(
                f"""
                SELECT id, category, setup, punchline, tags, safe, language, created_at, updated_at
                FROM jokes
                {where}
                ORDER BY RANDOM()
                LIMIT 1
                """,
                params,
            ).fetchone()
        return row_to_joke(row) if row else None

    def get(self, joke_id: str) -> dict[str, Any] | None:
        with connect(self.path) as db:
            row = db.execute(
                """
                SELECT id, category, setup, punchline, tags, safe, language, created_at, updated_at
                FROM jokes
                WHERE id = ?
                """,
                (joke_id,),
            ).fetchone()
        return row_to_joke(row) if row else None

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        joke = normalize_payload(payload, joke_id=str(uuid4()))
        with connect(self.path) as db:
            db.execute(
                """
                INSERT INTO jokes
                    (id, category, setup, punchline, tags, safe, language)
                VALUES
                    (:id, :category, :setup, :punchline, :tags, :safe, :language)
                """,
                encode_payload(joke),
            )
        created = self.get(joke["id"])
        if created is None:
            raise RuntimeError("Created joke could not be loaded")
        return created

    def update(self, joke_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        existing = self.get(joke_id)
        if existing is None:
            return None

        merged = normalize_payload({**existing, **payload}, joke_id=joke_id)
        with connect(self.path) as db:
            db.execute(
                """
                UPDATE jokes
                SET category = :category,
                    setup = :setup,
                    punchline = :punchline,
                    tags = :tags,
                    safe = :safe,
                    language = :language,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = :id
                """,
                encode_payload(merged),
            )
        return self.get(joke_id)

    def delete(self, joke_id: str) -> bool:
        with connect(self.path) as db:
            cursor = db.execute("DELETE FROM jokes WHERE id = ?", (joke_id,))
        return cursor.rowcount > 0

    def categories(self) -> list[str]:
        with connect(self.path) as db:
            rows = db.execute(
                "SELECT DISTINCT category FROM jokes ORDER BY category ASC"
            ).fetchall()
        return [row["category"] for row in rows]

    def tags(self) -> list[str]:
        tags: set[str] = set()
        for joke in self.list():
            tags.update(joke.get("tags", []))
        return sorted(tags)

    def _where(self, filters: JokeFilters | None) -> tuple[str, dict[str, Any]]:
        if not filters:
            return "", {}

        clauses: list[str] = []
        params: dict[str, Any] = {}
        if filters.category:
            clauses.append("LOWER(category) = LOWER(:category)")
            params["category"] = filters.category
        if filters.safe is not None:
            clauses.append("safe = :safe")
            params["safe"] = 1 if filters.safe else 0
        if filters.language:
            clauses.append("LOWER(language) = LOWER(:language)")
            params["language"] = filters.language
        if filters.tag:
            clauses.append("LOWER(tags) LIKE LOWER(:tag)")
            params["tag"] = f'%"{filters.tag}"%'

        if not clauses:
            return "", {}
        return f"WHERE {' AND '.join(clauses)}", params


def normalize_payload(payload: dict[str, Any], joke_id: str) -> dict[str, Any]:
    return {
        "id": joke_id,
        "category": str(payload["category"]).strip(),
        "setup": str(payload["setup"]).strip(),
        "punchline": str(payload["punchline"]).strip(),
        "tags": payload.get("tags", []),
        "safe": bool(payload.get("safe", True)),
        "language": str(payload.get("language", "en")).strip() or "en",
    }


def encode_payload(joke: dict[str, Any]) -> dict[str, Any]:
    return {
        **joke,
        "tags": encode_tags(joke.get("tags", [])),
        "safe": 1 if joke.get("safe", True) else 0,
    }

