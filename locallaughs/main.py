"""
CLI entry point for Locallaughs.

This module implements a very small command‑line interface that
- prints a random joke from the built‑in database, or
- accepts optional arguments to specify category, setup, etc.

The implementation is intentionally lightweight so you can extend it
later without having to refactor.
"""
import argparse
import json
import os
import random
from pathlib import Path

JOKES_DIR = Path(__file__).parent.parent / "jokes"
DEFAULT_JOKES_FILE = JOKES_DIR / "default_jokes.json"


def load_jokes(file_path: Path | str) -> list[dict]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Could not read jokes from {file_path}: {e}")


def pick_joke(jokes: list[dict], category: str | None = None) -> dict:
    if category:
        filtered = [j for j in jokes if j.get("category") == category]
        if not filtered:
            raise ValueError(f"No jokes found for category '{category}'")
        return random.choice(filtered)
    return random.choice(jokes)


def main() -> None:  # pragma: no cover - CLI entry point
    parser = argparse.ArgumentParser(description="LocalLaughs – a local joke generator")
    parser.add_argument("--setup", help="If provided, generate a punchline for this setup.")
    parser.add_argument("--category", help="Show a random joke from this category.")
    parser.add_argument("--file", default=str(DEFAULT_JOKES_FILE), help="Path to JSON file with jokes")

    args = parser.parse_args()

    jokes = load_jokes(args.file)
    if not jokes:
        raise RuntimeError("No jokes loaded.")

    if args.setup:
        # Very simple pattern‑matching: just echo the setup and a dummy punchline.
        print(f"🤖 LocalLaughs:\n  Setup: {args.setup}\n  Punchline: (AI generated, not implemented yet)\n")
    else:
        joke = pick_joke(jokes, args.category)
        print(f"🤖 LocalLaughs:\n  Setup: {joke.get('setup')}\n  Punchline: {joke.get('punchline')}\n")


if __name__ == "__main__":
    main()
