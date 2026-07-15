from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from .generator import generate_joke
from .repository import JokeFilters, JokeRepository
from .validation import validate_generated_payload, validate_joke_payload

api = Blueprint("api", __name__)


def repository() -> JokeRepository:
    return JokeRepository(current_app.config["JOKES_DB"])


@api.get("/health")
def health():
    return jsonify({"status": "ok", "service": "LocalLaughs"})


@api.get("/api/v1/jokes")
def list_jokes():
    filters = parse_filters()
    jokes = repository().list(filters)
    return jsonify({"count": len(jokes), "jokes": jokes})


@api.get("/api/v1/categories")
def categories():
    return jsonify({"categories": repository().categories()})


@api.get("/api/v1/tags")
def tags():
    return jsonify({"tags": repository().tags()})


@api.get("/api/v1/jokes/random")
def random_joke():
    joke = repository().random(parse_filters())
    if joke is None:
        return jsonify({"error": "No joke matched the requested filters"}), 404
    return jsonify(joke)


@api.get("/api/v1/jokes/<joke_id>")
def get_joke(joke_id: str):
    joke = repository().get(joke_id)
    if joke is None:
        return jsonify({"error": "Joke not found"}), 404
    return jsonify(joke)


@api.post("/api/v1/jokes")
def create_joke():
    payload = request.get_json(silent=True) or {}
    errors = validate_joke_payload(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    joke = repository().create(payload)
    return jsonify(joke), 201


@api.put("/api/v1/jokes/<joke_id>")
def update_joke(joke_id: str):
    payload = request.get_json(silent=True) or {}
    errors = validate_joke_payload(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    joke = repository().update(joke_id, payload)
    if joke is None:
        return jsonify({"error": "Joke not found"}), 404
    return jsonify(joke)


@api.delete("/api/v1/jokes/<joke_id>")
def delete_joke(joke_id: str):
    deleted = repository().delete(joke_id)
    if not deleted:
        return jsonify({"error": "Joke not found"}), 404
    return "", 204


@api.post("/api/v1/jokes/generate")
def generate():
    payload = request.get_json(silent=True) or {}
    errors = validate_generated_payload(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    joke = generate_joke(payload)
    if payload.get("save") is True:
        joke = repository().create(joke)
    return jsonify(joke), 201 if payload.get("save") is True else 200


def parse_filters() -> JokeFilters:
    safe = request.args.get("safe")
    return JokeFilters(
        category=request.args.get("category"),
        safe=parse_bool(safe) if safe is not None else None,
        language=request.args.get("language"),
        tag=request.args.get("tag"),
    )


def parse_bool(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes"}:
        return True
    if normalized in {"0", "false", "no"}:
        return False
    return None
