# LocalLaughs

LocalLaughs is a private, local-first JokeAPI and joke engine built with Flask.

No cloud dependency, no telemetry, no account system by default. The API serves and manages a local SQLite joke collection, seeded from JSON, and includes a small template-based generator that runs fully on your machine.

## Features

- Flask app factory structure
- Versioned REST API under `/api/v1`
- Local SQLite joke storage
- JSON seed data for first boot
- Template-based local joke generation
- CLI companion via `python -m locallaughs`
- Random joke endpoint with filters
- Joke CRUD endpoints
- Category and tag endpoints
- Health check endpoint
- Pytest coverage for the main API behavior

## Project Structure

```text
.
├── app.py
├── data/
│   └── jokes.json
├── locallaughs/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── generator.py
│   ├── repository.py
│   ├── routes.py
│   └── validation.py
├── requirements.txt
├── requirements-dev.txt
└── tests/
    └── test_api.py
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Run

```bash
flask --app app run --debug
```

The API will run at:

```text
http://127.0.0.1:5000
```

## CLI

The CLI keeps the original "joke engine for your machine" feel while the Flask API handles HTTP use cases.

```bash
# Print a random local joke
python -m locallaughs random

# Filter by category or tag
python -m locallaughs random --category programming
python -m locallaughs random --tag testing

# Generate a local template joke
python -m locallaughs generate --category tech --topic "LocalLaughs"

# Generate and save the joke to SQLite
python -m locallaughs generate --category dad --topic SQLite --save

# Add a joke manually
python -m locallaughs add \
  --category programming \
  --setup "Why did the API smile?" \
  --punchline "It got a 200 OK." \
  --tags api flask

# Run the API server
python -m locallaughs serve --port 5000
```

## Endpoints

### Health

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "LocalLaughs"
}
```

### List jokes

```http
GET /api/v1/jokes
```

Optional filters:

- `category`
- `language`
- `safe=true|false`
- `tag`

Example:

```bash
curl "http://127.0.0.1:5000/api/v1/jokes?category=programming&safe=true"
```

### List categories

```http
GET /api/v1/categories
```

### List tags

```http
GET /api/v1/tags
```

### Random joke

```http
GET /api/v1/jokes/random
```

Example:

```bash
curl "http://127.0.0.1:5000/api/v1/jokes/random"
```

### Get one joke

```http
GET /api/v1/jokes/<joke_id>
```

Example:

```bash
curl "http://127.0.0.1:5000/api/v1/jokes/local-001"
```

### Create joke

```http
POST /api/v1/jokes
Content-Type: application/json
```

Example:

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/jokes" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "programming",
    "setup": "Why did the API smile?",
    "punchline": "It got a 200 OK.",
    "tags": ["api"],
    "safe": true,
    "language": "en"
  }'
```

Required fields:

- `category`
- `setup`
- `punchline`

Optional fields:

- `tags`
- `safe`
- `language`

### Update joke

```http
PUT /api/v1/jokes/<joke_id>
Content-Type: application/json
```

The payload uses the same fields as joke creation.

### Delete joke

```http
DELETE /api/v1/jokes/<joke_id>
```

### Generate joke

```http
POST /api/v1/jokes/generate
Content-Type: application/json
```

Example:

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/jokes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "tech",
    "topic": "LocalLaughs",
    "save": false
  }'
```

Supported generator categories:

- `programming`
- `dad`
- `tech`

Set `"save": true` to store the generated joke in the local SQLite database.

## Data Format

Jokes are stored in local SQLite at `data/locallaughs.sqlite3`.

On first boot, the database is seeded from `data/jokes.json`:

```json
[
  {
    "id": "local-001",
    "category": "programming",
    "setup": "Why do Python developers prefer dark mode?",
    "punchline": "Because light attracts bugs.",
    "tags": ["python", "developer"],
    "safe": true,
    "language": "en"
  }
]
```

## Tests

```bash
pytest
```

## Roadmap

- Add pagination for large joke collections
- Add optional API key authentication
- Add import/export tools for JSON and CSV joke files
- Add OpenAPI documentation
- Add optional local LLM generation backend

## License

MIT

