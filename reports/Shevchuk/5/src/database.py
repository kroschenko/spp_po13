"""Database connection settings for lab 5."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/education_db"

engine = create_engine(DATABASE_URL)
SESSION_LOCAL = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
