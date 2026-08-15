from sqlalchemy.orm import Session
from database.engine import engine

with Session(engine) as session:
    session.add_all()
    session.commit()