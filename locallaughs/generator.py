from __future__ import annotations

import random
from typing import Any
from uuid import uuid4

TEMPLATES = {
    "programming": [
        (
            "Why did the {topic} function refuse to run?",
            "Because it had too many unresolved issues.",
        ),
        (
            "Why did the developer bring {topic} to standup?",
            "Because every sprint needs a little runtime comedy.",
        ),
    ],
    "dad": [
        (
            "Why did {topic} cross the road?",
            "To prove it was not just a setup.",
        ),
        (
            "What did {topic} say after a long day?",
            "I am totally punchlined out.",
        ),
    ],
    "tech": [
        (
            "Why did the server invite {topic} over?",
            "Because it needed someone to handle the requests.",
        ),
        (
            "Why was {topic} great at networking?",
            "It always knew how to make a connection.",
        ),
    ],
}


def generate_joke(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    category = str(payload.get("category", "programming")).strip().lower() or "programming"
    topic = str(payload.get("topic", "the API")).strip() or "the API"
    language = str(payload.get("language", "en")).strip() or "en"

    templates = TEMPLATES.get(category, TEMPLATES["programming"])
    setup_template, punchline = random.choice(templates)

    return {
        "id": f"generated-{uuid4()}",
        "category": category,
        "setup": setup_template.format(topic=topic),
        "punchline": punchline,
        "tags": ["generated", category],
        "safe": True,
        "language": language,
        "generated": True,
    }

