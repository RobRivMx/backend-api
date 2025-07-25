# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# La única línea que cambiamos es esta, añadiendo pool_pre_ping=True
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para usar en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()