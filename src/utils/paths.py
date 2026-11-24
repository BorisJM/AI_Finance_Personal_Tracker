import json
from pathlib import Path

# Project root (folder that contains main.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DICTIONARIES_DIR = PROJECT_ROOT / "data" / "dictionaries"


def load_dictionary(file_name: str):
    """Load a JSON file from data/dictionaries, independent of the working directory."""
    with open(DICTIONARIES_DIR / file_name, "r", encoding="utf-8") as f:
        return json.load(f)
