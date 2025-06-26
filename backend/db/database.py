from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os
from dotenv import load_dotenv
from backend.db.base import Base


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()