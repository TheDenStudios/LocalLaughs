from pathlib import Path

from locallaughs import create_app
from locallaughs.config import Config


class TestConfig(Config):
    TESTING = True


def make_client(tmp_path: Path):
    seed_file = tmp_path / "seed.json"
    seed_file.write_text(
        """[
  {
    "id": "test-001",
    "category": "programming",
    "setup": "Why did the test pass?",
    "punchline": "Because the fixtures were stable.",
    "tags": ["testing"],
    "safe": true,
    "language": "en"
  }
]
""",
        encoding="utf-8",
    )

    class LocalTestConfig(TestConfig):
        JOKES_DB = tmp_path / "locallaughs.sqlite3"
        SEED_FILE = seed_file

    return create_app(LocalTestConfig).test_client()


def test_health(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_list_jokes(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/api/v1/jokes")

    assert response.status_code == 200
    body = response.get_json()
    assert body["count"] == 1
    assert body["jokes"][0]["id"] == "test-001"


def test_categories_and_tags(tmp_path):
    client = make_client(tmp_path)

    categories = client.get("/api/v1/categories").get_json()
    tags = client.get("/api/v1/tags").get_json()

    assert categories == {"categories": ["programming"]}
    assert tags == {"tags": ["testing"]}


def test_random_joke_filter_not_found(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/api/v1/jokes/random?category=dad")

    assert response.status_code == 404
    assert response.get_json()["error"] == "No joke matched the requested filters"


def test_create_joke(tmp_path):
    client = make_client(tmp_path)

    response = client.post(
        "/api/v1/jokes",
        json={
            "category": "tech",
            "setup": "Why did the API smile?",
            "punchline": "It got a 200 OK.",
            "tags": ["api"],
            "safe": True,
            "language": "en",
        },
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["id"]
    assert body["category"] == "tech"


def test_update_joke(tmp_path):
    client = make_client(tmp_path)

    response = client.put(
        "/api/v1/jokes/test-001",
        json={
            "category": "programming",
            "setup": "Why did the test evolve?",
            "punchline": "Because the API grew features.",
            "tags": ["testing", "api"],
            "safe": True,
            "language": "en",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["punchline"] == "Because the API grew features."


def test_delete_joke(tmp_path):
    client = make_client(tmp_path)

    response = client.delete("/api/v1/jokes/test-001")

    assert response.status_code == 204
    assert client.get("/api/v1/jokes/test-001").status_code == 404


def test_generate_joke(tmp_path):
    client = make_client(tmp_path)

    response = client.post(
        "/api/v1/jokes/generate",
        json={"category": "tech", "topic": "LocalLaughs"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["generated"] is True
    assert body["category"] == "tech"


def test_generate_and_save_joke(tmp_path):
    client = make_client(tmp_path)

    response = client.post(
        "/api/v1/jokes/generate",
        json={"category": "dad", "topic": "SQLite", "save": True},
    )

    assert response.status_code == 201
    joke_id = response.get_json()["id"]
    assert client.get(f"/api/v1/jokes/{joke_id}").status_code == 200


def test_create_joke_validation(tmp_path):
    client = make_client(tmp_path)

    response = client.post("/api/v1/jokes", json={"category": ""})

    assert response.status_code == 400
    assert "setup" in response.get_json()["errors"]

