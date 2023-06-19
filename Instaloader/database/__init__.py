from Config import DATABASE_URL
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE = declarative_base()
SESSION = sessionmaker(bind=engine)()

def create_tables():
    BASE.metadata.create_all(engine)
        
