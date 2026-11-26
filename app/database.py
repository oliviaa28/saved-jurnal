import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = (
    "postgresql+psycopg://"
    + os.getenv("DB_USER") + ":" + os.getenv("DB_PASSWORD") 
    + "@localhost:5433/" + os.getenv("DB_NAME")
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind= engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
