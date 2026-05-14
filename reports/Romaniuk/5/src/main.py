# -*- coding: utf-8 -*-
"""FastAPI application for Railway Bureau."""

from datetime import date
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Railway Bureau", description="Справочное бюро ж/д вокзала")


@app.post("/stations/", response_model=schemas.StationResponse)
def create_station(station: schemas.StationCreate, db: Session = Depends(get_db)):
    """Create a new station."""
    return crud.create_station(db, station)


@app.get("/stations/", response_model=List[schemas.StationResponse])
def get_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all stations with pagination."""
    return crud.get_stations(db, skip, limit)


@app.get("/stations/{station_id}", response_model=schemas.StationResponse)
def get_station(station_id: int, db: Session = Depends(get_db)):
    """Get station by ID."""
    station = crud.get_station(db, station_id)
    if not station:
        raise HTTPException(404, "Station not found")
    return station


@app.put("/stations/{station_id}", response_model=schemas.StationResponse)
def update_station(station_id: int, station: schemas.StationCreate, db: Session = Depends(get_db)):
    """Update station by ID."""
    result = crud.update_station(db, station_id, station)
    if not result:
        raise HTTPException(404, "Station not found")
    return result


@app.delete("/stations/{station_id}")
def delete_station(station_id: int, db: Session = Depends(get_db)):
    """Delete station by ID."""
    if not crud.delete_station(db, station_id):
        raise HTTPException(404, "Station not found")
    return {"message": "Station deleted"}



@app.post("/trains/", response_model=schemas.TrainResponse)
def create_train(train: schemas.TrainCreate, db: Session = Depends(get_db)):
    """Create a new train."""
    return crud.create_train(db, train)


@app.get("/trains/", response_model=List[schemas.TrainResponse])
def get_trains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all trains with pagination."""
    return crud.get_trains(db, skip, limit)


@app.get("/trains/{train_id}", response_model=schemas.TrainResponse)
def get_train(train_id: int, db: Session = Depends(get_db)):
    """Get train by ID."""
    train = crud.get_train(db, train_id)
    if not train:
        raise HTTPException(404, "Train not found")
    return train


@app.put("/trains/{train_id}", response_model=schemas.TrainResponse)
def update_train(train_id: int, train: schemas.TrainCreate, db: Session = Depends(get_db)):
    """Update train by ID."""
    result = crud.update_train(db, train_id, train)
    if not result:
        raise HTTPException(404, "Train not found")
    return result


@app.delete("/trains/{train_id}")
def delete_train(train_id: int, db: Session = Depends(get_db)):
    """Delete train by ID."""
    if not crud.delete_train(db, train_id):
        raise HTTPException(404, "Train not found")
    return {"message": "Train deleted"}


@app.post("/schedules/", response_model=schemas.ScheduleResponse)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    """Create a new schedule."""
    return crud.create_schedule(db, schedule)


@app.get("/schedules/", response_model=List[schemas.ScheduleResponse])
def get_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all schedules with pagination."""
    return crud.get_schedules(db, skip, limit)


@app.get("/schedules/{schedule_id}", response_model=schemas.ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Get schedule by ID."""
    schedule = crud.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(404, "Schedule not found")
    return schedule


@app.put("/schedules/{schedule_id}", response_model=schemas.ScheduleResponse)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    """Update schedule by ID."""
    result = crud.update_schedule(db, schedule_id, schedule)
    if not result:
        raise HTTPException(404, "Schedule not found")
    return result


@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Delete schedule by ID."""
    if not crud.delete_schedule(db, schedule_id):
        raise HTTPException(404, "Schedule not found")
    return {"message": "Schedule deleted"}


@app.get("/schedules/search/by-station/")
def search_by_station(station_id: int, travel_date: date, db: Session = Depends(get_db)):
    """Search schedules by station ID and travel date."""
    return crud.find_trains_by_station_and_date(db, station_id, travel_date)


@app.post("/passengers/", response_model=schemas.PassengerResponse)
def create_passenger(passenger: schemas.PassengerCreate, db: Session = Depends(get_db)):
    """Create a new passenger."""
    return crud.create_passenger(db, passenger)


@app.get("/passengers/", response_model=List[schemas.PassengerResponse])
def get_passengers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all passengers with pagination."""
    return crud.get_passengers(db, skip, limit)


@app.get("/passengers/{passenger_id}", response_model=schemas.PassengerResponse)
def get_passenger(passenger_id: int, db: Session = Depends(get_db)):
    """Get passenger by ID."""
    passenger = crud.get_passenger(db, passenger_id)
    if not passenger:
        raise HTTPException(404, "Passenger not found")
    return passenger


@app.put("/passengers/{passenger_id}", response_model=schemas.PassengerResponse)
def update_passenger(passenger_id: int, passenger: schemas.PassengerCreate, db: Session = Depends(get_db)):
    """Update passenger by ID."""
    result = crud.update_passenger(db, passenger_id, passenger)
    if not result:
        raise HTTPException(404, "Passenger not found")
    return result


@app.delete("/passengers/{passenger_id}")
def delete_passenger(passenger_id: int, db: Session = Depends(get_db)):
    """Delete passenger by ID."""
    if not crud.delete_passenger(db, passenger_id):
        raise HTTPException(404, "Passenger not found")
    return {"message": "Passenger deleted"}



@app.post("/tickets/", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    """Create a new ticket."""
    result = crud.create_ticket(db, ticket)
    if not result:
        raise HTTPException(400, "No available seats")
    return result


@app.get("/tickets/", response_model=List[schemas.TicketResponse])
def get_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tickets with pagination."""
    return crud.get_tickets(db, skip, limit)


@app.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get ticket by ID."""
    ticket = crud.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    return ticket


@app.put("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(ticket_id: int, ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    """Update ticket by ID."""
    result = crud.update_ticket(db, ticket_id, ticket)
    if not result:
        raise HTTPException(404, "Ticket not found")
    return result


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Delete ticket by ID."""
    if not crud.delete_ticket(db, ticket_id):
        raise HTTPException(404, "Ticket not found")
    return {"message": "Ticket deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
