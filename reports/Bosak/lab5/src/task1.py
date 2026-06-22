"""Module for transport database API."""

from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

DATABASE_URL = "sqlite:///transport.db"

engine = create_engine(DATABASE_URL, echo=True)
SESSION_LOCAL = sessionmaker(bind=engine)
Base = declarative_base()


# ==================== PYDANTIC MODELS ====================

class RouteCreate(BaseModel):
    """Schema for creating a route."""
    number: str
    start_point: str
    end_point: str


class RouteUpdate(BaseModel):
    """Schema for updating a route."""
    number: str
    start_point: str
    end_point: str


class BusCreate(BaseModel):
    """Schema for creating a bus."""
    route_id: int
    model: str
    year: int
    capacity: int


class BusUpdate(BaseModel):
    """Schema for updating a bus."""
    route_id: int
    model: str
    year: int
    capacity: int


class DriverCreate(BaseModel):
    """Schema for creating a driver."""
    bus_id: int
    name: str
    license_number: str
    phone: str


class DriverUpdate(BaseModel):
    """Schema for updating a driver."""
    bus_id: int
    name: str
    license_number: str
    phone: str


class StopCreate(BaseModel):
    """Schema for creating a stop."""
    name: str
    address: str
    latitude: int
    longitude: int


class StopUpdate(BaseModel):
    """Schema for updating a stop."""
    name: str
    address: str
    latitude: int
    longitude: int


class TripCreate(BaseModel):
    """Schema for creating a trip."""
    bus_id: int
    route_id: int
    driver_id: int
    trip_date: datetime
    trip_time: str


class TripUpdate(BaseModel):
    """Schema for updating a trip."""
    bus_id: int
    route_id: int
    driver_id: int
    trip_date: datetime
    trip_time: str


# ==================== SQLALCHEMY MODELS ====================

class Route(Base):
    """Route table."""
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    start_point = Column(String, nullable=False)
    end_point = Column(String, nullable=False)

    buses = relationship("Bus", back_populates="route")


class Bus(Base):
    """Bus table."""
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)

    route = relationship("Route", back_populates="buses")
    driver = relationship("Driver", back_populates="bus", uselist=False)
    trips = relationship("Trip", back_populates="bus")


class Driver(Base):
    """Driver table."""
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), unique=True)
    name = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    phone = Column(String)

    bus = relationship("Bus", back_populates="driver")
    trips = relationship("Trip", back_populates="driver")


class Stop(Base):
    """Stop table."""
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    latitude = Column(Integer)
    longitude = Column(Integer)


class Trip(Base):
    """Trip table."""
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    route_id = Column(Integer, ForeignKey("routes.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    trip_date = Column(DateTime, nullable=False)
    trip_time = Column(String, nullable=False)

    bus = relationship("Bus", back_populates="trips")
    route = relationship("Route")
    driver = relationship("Driver", back_populates="trips")


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Get database session."""
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()


# ==================== ROUTES ====================

@app.post("/routes/")
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    """Create new route."""
    db_route = Route(
        number=route.number,
        start_point=route.start_point,
        end_point=route.end_point
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


@app.get("/routes/")
def get_routes(db: Session = Depends(get_db)):
    """Get all routes."""
    return db.query(Route).all()


@app.put("/routes/{route_id}")
def update_route(route_id: int, route: RouteUpdate, db: Session = Depends(get_db)):
    """Update route."""
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    db_route.number = route.number
    db_route.start_point = route.start_point
    db_route.end_point = route.end_point
    db.commit()
    return db_route


@app.delete("/routes/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    """Delete route."""
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    db.delete(db_route)
    db.commit()
    return {"status": "удалён"}


# ==================== BUSES ====================

@app.post("/buses/")
def create_bus(bus: BusCreate, db: Session = Depends(get_db)):
    """Create new bus."""
    db_bus = Bus(
        route_id=bus.route_id,
        model=bus.model,
        year=bus.year,
        capacity=bus.capacity
    )
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus


@app.get("/buses/")
def get_buses(db: Session = Depends(get_db)):
    """Get all buses."""
    return db.query(Bus).all()


@app.put("/buses/{bus_id}")
def update_bus(bus_id: int, bus: BusUpdate, db: Session = Depends(get_db)):
    """Update bus."""
    db_bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(status_code=404, detail="Автобус не найден")
    db_bus.route_id = bus.route_id
    db_bus.model = bus.model
    db_bus.year = bus.year
    db_bus.capacity = bus.capacity
    db.commit()
    return db_bus


@app.delete("/buses/{bus_id}")
def delete_bus(bus_id: int, db: Session = Depends(get_db)):
    """Delete bus."""
    db_bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(status_code=404, detail="Автобус не найден")
    db.delete(db_bus)
    db.commit()
    return {"status": "удалён"}


# ==================== DRIVERS ====================

@app.post("/drivers/")
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    """Create new driver."""
    db_driver = Driver(
        bus_id=driver.bus_id,
        name=driver.name,
        license_number=driver.license_number,
        phone=driver.phone
    )
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


@app.get("/drivers/")
def get_drivers(db: Session = Depends(get_db)):
    """Get all drivers."""
    return db.query(Driver).all()


@app.put("/drivers/{driver_id}")
def update_driver(driver_id: int, driver: DriverUpdate, db: Session = Depends(get_db)):
    """Update driver."""
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Водитель не найден")
    db_driver.bus_id = driver.bus_id
    db_driver.name = driver.name
    db_driver.license_number = driver.license_number
    db_driver.phone = driver.phone
    db.commit()
    return db_driver


@app.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    """Delete driver."""
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Водитель не найден")
    db.delete(db_driver)
    db.commit()
    return {"status": "удалён"}


# ==================== STOPS ====================

@app.post("/stops/")
def create_stop(stop: StopCreate, db: Session = Depends(get_db)):
    """Create new stop."""
    db_stop = Stop(
        name=stop.name,
        address=stop.address,
        latitude=stop.latitude,
        longitude=stop.longitude
    )
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    return db_stop


@app.get("/stops/")
def get_stops(db: Session = Depends(get_db)):
    """Get all stops."""
    return db.query(Stop).all()


@app.put("/stops/{stop_id}")
def update_stop(stop_id: int, stop: StopUpdate, db: Session = Depends(get_db)):
    """Update stop."""
    db_stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not db_stop:
        raise HTTPException(status_code=404, detail="Остановка не найдена")
    db_stop.name = stop.name
    db_stop.address = stop.address
    db_stop.latitude = stop.latitude
    db_stop.longitude = stop.longitude
    db.commit()
    return db_stop


@app.delete("/stops/{stop_id}")
def delete_stop(stop_id: int, db: Session = Depends(get_db)):
    """Delete stop."""
    db_stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not db_stop:
        raise HTTPException(status_code=404, detail="Остановка не найдена")
    db.delete(db_stop)
    db.commit()
    return {"status": "удалён"}


# ==================== TRIPS ====================

@app.post("/trips/")
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    """Create new trip."""
    db_trip = Trip(
        bus_id=trip.bus_id,
        route_id=trip.route_id,
        driver_id=trip.driver_id,
        trip_date=trip.trip_date,
        trip_time=trip.trip_time
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


@app.get("/trips/")
def get_trips(db: Session = Depends(get_db)):
    """Get all trips."""
    return db.query(Trip).all()


@app.put("/trips/{trip_id}")
def update_trip(trip_id: int, trip: TripUpdate, db: Session = Depends(get_db)):
    """Update trip."""
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Рейс не найден")
    db_trip.bus_id = trip.bus_id
    db_trip.route_id = trip.route_id
    db_trip.driver_id = trip.driver_id
    db_trip.trip_date = trip.trip_date
    db_trip.trip_time = trip.trip_time
    db.commit()
    return db_trip


@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Delete trip."""
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Рейс не найден")
    db.delete(db_trip)
    db.commit()
    return {"status": "удалён"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
