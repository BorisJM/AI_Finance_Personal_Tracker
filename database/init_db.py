from database.base import Base
from database.engine import engine
from database import models

Base.metadata.create_all(engine)