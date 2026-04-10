"""Модель игрока."""

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Player(Base):  # pylint: disable=too-few-public-methods
    """ORM-модель игрока."""

    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date)
    country_id = Column(Integer, ForeignKey("countries.id"))

    country = relationship("Country", back_populates="players")
    stats = relationship("PlayerStat", back_populates="player")
