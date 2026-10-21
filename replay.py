import json
from pathlib import Path

CASSETTE_DIR = Path("cassettes")

def get_cassette_path(test_id: str) -> Path:
    CASSETTE_DIR.mkdir(exist_ok=True)
    return CASSETTE_DIR / f"{test_id}.json"

def load_cassette(test_id: str) -> dict | None:
    path = get_cassette_path(test_id)
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_cassette(test_id: str, data: dict):
    path = get_cassette_path(test_id)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)