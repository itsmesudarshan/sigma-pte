from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pte_platform.db")

# Render's Postgres connection strings use the "postgres://" scheme, but
# modern SQLAlchemy (1.4+) requires "postgresql://" — this is a well-known
# gotcha shared with Heroku-style URLs. Fix it here so the DATABASE_URL
# Render gives you can be pasted in directly with no manual editing.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
