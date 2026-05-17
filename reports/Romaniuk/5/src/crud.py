# -*- coding: utf-8 -*-
"""CRUD operations for database."""

from datetime import date

from sqlalchemy import and_
from sqlalchemy.orm import Session

import models
import schemas


def create_station(db: Session, station: schemas.StationCreate):
    """Create a new station."""
    db_station = models.Station(**station.model_dump())
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station


def get_stations(db: Session, skip: int = 0, limit: int = 100):
    """Get all stations."""
    return db.query(models.Station).offset(skip).limit(limit).all()


def get_station(db: Session, station_id: int):
    """Get station by ID."""
    return db.query(models.Station).filter(models.Station.id == station_id).first()


def update_station(db: Session, station_id: int, station_data: schemas.StationCreate):
    """Update station."""
    db_station = get_station(db, station_id)
    if db_station:
        for key, value in station_data.model_dump().items():
            setattr(db_station, key, value)
        db.commit()
        db.refresh(db_station)
    return db_station


def delete_station(db: Session, station_id: int):
    """Delete station."""
    db_station = get_station(db, station_id)
    if db_station:
        db.delete(db_station)
        db.commit()
        return True
    return False



def create_train(db: Session, train: schemas.TrainCreate):
    """Create a new train."""
    db_train = models.Train(**train.model_dump())
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    return db_train


def get_trains(db: Session, skip: int = 0, limit: int = 100):
    """Get all trains."""
    return db.query(models.Train).offset(skip).limit(limit).all()


def get_train(db: Session, train_id: int):
    """Get train by ID."""
    return db.query(models.Train).filter(models.Train.id == train_id).first()


def update_train(db: Session, train_id: int, train_data: schemas.TrainCreate):
    """Update train."""
    db_train = get_train(db, train_id)
    if db_train:
        for key, value in train_data.model_dump().items():
            setattr(db_train, key, value)
        db.commit()
        db.refresh(db_train)
    return db_train


def delete_train(db: Session, train_id: int):
    """Delete train."""
    db_train = get_train(db, train_id)
    if db_train:
        db.delete(db_train)
        db.commit()
        return True
    return False



def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    """Create a new schedule."""
    db_schedule = models.Schedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_schedules(db: Session, skip: int = 0, limit: int = 100):
    """Get all schedules."""
    return db.query(models.Schedule).offset(skip).limit(limit).all()


def get_schedule(db: Session, schedule_id: int):
    """Get schedule by ID."""
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()


def update_schedule(db: Session, schedule_id: int, schedule_data: schemas.ScheduleCreate):
    """Update schedule."""
    db_schedule = get_schedule(db, schedule_id)
    if db_schedule:
        for key, value in schedule_data.model_dump().items():
            setattr(db_schedule, key, value)
        db.commit()
        db.refresh(db_schedule)
    return db_schedule


def delete_schedule(db: Session, schedule_id: int):
    """Delete schedule."""
    db_schedule = get_schedule(db, schedule_id)
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
        return True
    return False


def find_trains_by_station_and_date(db: Session, station_id: int, travel_date: date):
    """Найти поезда по станции и дате отправления."""
    results = (
        db.query(models.Schedule)
        .join(models.Train)
        .filter(and_(models.Train.departure_station_id == station_id, models.Schedule.departure_date == travel_date))
        .all()
    )
    return results


# ---------- Passenger operations ----------
def create_passenger(db: Session, passenger: schemas.PassengerCreate):
    """Create a new passenger."""
    db_passenger = models.Passenger(**passenger.model_dump())
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)
    return db_passenger


def get_passengers(db: Session, skip: int = 0, limit: int = 100):
    """Get all passengers."""
    return db.query(models.Passenger).offset(skip).limit(limit).all()


def get_passenger(db: Session, passenger_id: int):
    """Get passenger by ID."""
    return db.query(models.Passenger).filter(models.Passenger.id == passenger_id).first()


def update_passenger(db: Session, passenger_id: int, passenger_data: schemas.PassengerCreate):
    """Update passenger."""
    db_passenger = get_passenger(db, passenger_id)
    if db_passenger:
        for key, value in passenger_data.model_dump().items():
            setattr(db_passenger, key, value)
        db.commit()
        db.refresh(db_passenger)
    return db_passenger


def delete_passenger(db: Session, passenger_id: int):
    """Delete passenger."""
    db_passenger = get_passenger(db, passenger_id)
    if db_passenger:
        db.delete(db_passenger)
        db.commit()
        return True
    return False


def create_ticket(db: Session, ticket: schemas.TicketCreate):
    """Create a new ticket and reduce available seats."""
    schedule = db.query(models.Schedule).filter(models.Schedule.id == ticket.schedule_id).first()
    if schedule and schedule.available_seats > 0:
        schedule.available_seats -= 1
        db_ticket = models.Ticket(**ticket.model_dump())
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    return None


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    """Get all tickets."""
    return db.query(models.Ticket).offset(skip).limit(limit).all()


def get_ticket(db: Session, ticket_id: int):
    """Get ticket by ID."""
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()


def update_ticket(db: Session, ticket_id: int, ticket_data: schemas.TicketCreate):
    """Update ticket."""
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket:
        for key, value in ticket_data.model_dump().items():
            setattr(db_ticket, key, value)
        db.commit()
        db.refresh(db_ticket)
    return db_ticket


def delete_ticket(db: Session, ticket_id: int):
    """Delete ticket and restore available seats."""
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket:
        schedule = db.query(models.Schedule).filter(models.Schedule.id == db_ticket.schedule_id).first()
        if schedule:
            schedule.available_seats += 1
        db.delete(db_ticket)
        db.commit()
        return True
    return False
