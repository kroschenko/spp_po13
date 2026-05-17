# -*- coding: utf-8 -*-
"""Database models for railway bureau."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Numeric, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Station(Base):
    """Station model - таблица станций."""
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    city = Column(String(100), nullable=False)
    address = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)

    # Связи
    departures = relationship('Train', foreign_keys='Train.departure_station_id', back_populates='departure_station')
    arrivals = relationship('Train', foreign_keys='Train.arrival_station_id', back_populates='arrival_station')


class Train(Base):
    """Train model - таблица поездов."""
    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(10), nullable=False, unique=True)
    name = Column(String(100))
    train_type = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)

    departure_station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    arrival_station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)

    # Связи
    departure_station = relationship('Station', foreign_keys=[departure_station_id], back_populates='departures')
    arrival_station = relationship('Station', foreign_keys=[arrival_station_id], back_populates='arrivals')
    schedules = relationship('Schedule', back_populates='train')

    __table_args__ = (
        CheckConstraint('capacity > 0', name='check_capacity_positive'),
    )


class Schedule(Base):
    """Schedule model - таблица расписания."""
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey('trains.id'), nullable=False)
    departure_date = Column(Date, nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_date = Column(Date, nullable=False)
    arrival_time = Column(Time, nullable=False)
    travel_duration = Column(Integer)
    price = Column(Numeric(10, 2), nullable=False)
    available_seats = Column(Integer, nullable=False)

    train = relationship('Train', back_populates='schedules')
    tickets = relationship('Ticket', back_populates='schedule')

    __table_args__ = (
        CheckConstraint('available_seats >= 0', name='check_seats_positive'),
        CheckConstraint('price > 0', name='check_price_positive'),
    )


class Passenger(Base):
    """Passenger model - таблица пассажиров."""
    __tablename__ = 'passengers'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    passport_number = Column(String(20), nullable=False, unique=True)
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

    tickets = relationship('Ticket', back_populates='passenger')


class Ticket(Base):
    """Ticket model - таблица билетов."""
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    passenger_id = Column(Integer, ForeignKey('passengers.id'), nullable=False)
    seat_number = Column(String(10), nullable=False)
    purchase_date = Column(DateTime, default=datetime.now)
    status = Column(String(20), default='active')  # active, cancelled, used

    schedule = relationship('Schedule', back_populates='tickets')
    passenger = relationship('Passenger', back_populates='tickets')
