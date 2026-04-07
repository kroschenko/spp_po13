"""Настройки подключения к базе данных и базовый класс моделей."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:Azino888@localhost:5432/spp"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

SessionLocal = sessionmaker(  # pylint: disable=invalid-name
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

Base = declarative_base()
