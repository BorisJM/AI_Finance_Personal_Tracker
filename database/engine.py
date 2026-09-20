import sqlalchemy as db
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database.db"

# Define the engine
engine = db.create_engine(f"sqlite:///{DATABASE_PATH}", echo=True)