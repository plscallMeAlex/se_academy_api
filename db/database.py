# This file for creating an instance of the database connection and session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import get_settings

settings = get_settings()
engine = create_engine(settings.DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = get_db
