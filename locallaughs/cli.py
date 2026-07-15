from __future__ import annotations

import argparse
import json
import subprocess
import sys

from flask import current_app

from . import create_app
from .generator import generate_joke
from .repository import JokeFilters, JokeRepository


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "serve":
        command = [
            sys.executable,
            "-m",
            "flask",
            "--app",
            "app",
            "run",
            "--host",
            args.host,
            "--port",
            str(args.port),
        ]
        return subprocess.call(command)

    app = create_app()
    with app.app_context():
        repo = JokeRepository(current_app.config["JOKES_DB"])
        if args.command == "random":
            joke = repo.random(JokeFilters(category=args.category, tag=args.tag))
            if joke is None:
                print("No joke matched those filters.", file=sys.stderr)
                return 1
            print_joke(joke)
            return 0

        if args.command == "add":
            joke = repo.create(
                {
                    "category": args.category,
                    "setup": args.setup,
                    "punchline": args.punchline,
                    "tags": args.tags or [],
                    "safe": not args.unsafe,
                    "language": args.language,
                }
            )
            print(json.dumps(joke, indent=2))
            return 0

        if args.command == "generate":
            joke = generate_joke(
                {
                    "category": args.category,
                    "topic": args.topic,
                    "language": args.language,
                }
            )
            if args.save:
                joke = repo.create(joke)
            print_joke(joke)
            return 0

    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="locallaughs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    random_parser = subparsers.add_parser("random", help="Print a random local joke")
    random_parser.add_argument("--category")
    random_parser.add_argument("--tag")

    add_parser = subparsers.add_parser("add", help="Add a joke to the local database")
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--setup", required=True)
    add_parser.add_argument("--punchline", required=True)
    add_parser.add_argument("--tags", nargs="*")
    add_parser.add_argument("--language", default="en")
    add_parser.add_argument("--unsafe", action="store_true")

    generate_parser = subparsers.add_parser("generate", help="Generate a local template joke")
    generate_parser.add_argument("--category", default="programming")
    generate_parser.add_argument("--topic", default="the API")
    generate_parser.add_argument("--language", default="en")
    generate_parser.add_argument("--save", action="store_true")

    serve_parser = subparsers.add_parser("serve", help="Run the Flask API")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=5000)

    return parser


def print_joke(joke: dict) -> None:
    print(f"[{joke['category']}] {joke['setup']}")
    print(joke["punchline"])

