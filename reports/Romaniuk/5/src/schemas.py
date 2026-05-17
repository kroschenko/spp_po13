"""Pydantic schemas for request/response validation."""
from datetime import date, time, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class StationBase(BaseModel):
    """Base schema for station."""
    name: str
    city: str
    address: Optional[str] = None


class StationCreate(StationBase):
    """Schema for creating a new station."""


class StationResponse(StationBase):
    """Schema for station response."""
    id: int
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class TrainBase(BaseModel):
    """Base schema for train."""
    number: str
    name: Optional[str] = None
    train_type: str
    capacity: int
    departure_station_id: int
    arrival_station_id: int


class TrainCreate(TrainBase):
    """Schema for creating a new train."""


class TrainResponse(TrainBase):
    """Schema for train response."""
    id: int

    class Config:
        """Pydantic config."""
        from_attributes = True


class ScheduleBase(BaseModel):
    """Base schema for schedule."""
    train_id: int
    departure_date: date
    departure_time: time
    arrival_date: date
    arrival_time: time
    travel_duration: Optional[int] = None
    price: Decimal
    available_seats: int


class ScheduleCreate(ScheduleBase):
    """Schema for creating a new schedule."""


class ScheduleResponse(ScheduleBase):
    """Schema for schedule response."""
    id: int

    class Config:
        """Pydantic config."""
        from_attributes = True


class PassengerBase(BaseModel):
    """Base schema for passenger."""
    first_name: str
    last_name: str
    passport_number: str
    phone: Optional[str] = None
    email: Optional[str] = None


class PassengerCreate(PassengerBase):
    """Schema for creating a new passenger."""


class PassengerResponse(PassengerBase):
    """Schema for passenger response."""
    id: int
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class TicketBase(BaseModel):
    """Base schema for ticket."""
    schedule_id: int
    passenger_id: int
    seat_number: str
    status: Optional[str] = "active"


class TicketCreate(TicketBase):
    """Schema for creating a new ticket."""


class TicketResponse(TicketBase):
    """Schema for ticket response."""
    id: int
    purchase_date: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
