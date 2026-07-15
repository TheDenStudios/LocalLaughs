REQUIRED_FIELDS = ("category", "setup", "punchline")
KNOWN_GENERATOR_CATEGORIES = {"programming", "dad", "tech"}


def validate_joke_payload(payload: dict) -> dict[str, str]:
    errors: dict[str, str] = {}

    for field in REQUIRED_FIELDS:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            errors[field] = "This field is required."

    tags = payload.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        errors["tags"] = "Tags must be a list of strings."

    language = payload.get("language", "en")
    if not isinstance(language, str) or len(language.strip()) < 2:
        errors["language"] = "Language must be a valid language code."

    return errors


def validate_generated_payload(payload: dict) -> dict[str, str]:
    errors: dict[str, str] = {}

    category = payload.get("category", "programming")
    if not isinstance(category, str) or category.strip().lower() not in KNOWN_GENERATOR_CATEGORIES:
        errors["category"] = "Category must be one of: dad, programming, tech."

    topic = payload.get("topic", "the API")
    if not isinstance(topic, str) or not topic.strip():
        errors["topic"] = "Topic must be a non-empty string."

    save = payload.get("save", False)
    if not isinstance(save, bool):
        errors["save"] = "Save must be a boolean."

    return errors
