import sqlalchemy as db

# Define the engine
engine = db.create_engine('sqlite:///database.db', echo=True)