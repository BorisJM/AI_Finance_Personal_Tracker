from database.base import metadata_obj
from database.engine import engine

metadata_obj.create_all(engine)