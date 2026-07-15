from pathlib import Path


class Config:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    JOKES_DB = PROJECT_ROOT / "data" / "locallaughs.sqlite3"
    SEED_FILE = PROJECT_ROOT / "data" / "jokes.json"
    JSON_SORT_KEYS = False
