from pathlib import Path
from sqlalchemy.orm import Session
from database.engine import engine
from database.services.import_service import ImportService

with Session(engine) as session:
    import_service = ImportService(session)

    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "raw" / "transactions.csv"

    # START IMPORT...
    import_service.import_transactions(file_path)