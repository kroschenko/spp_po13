# pylint: disable=too-few-public-methods, duplicate-code
"""Схемы."""

from pydantic import BaseModel


# Depot
class DepotCreate(BaseModel):
    """Схемы."""
    name: str
    address: str


class DepotOut(BaseModel):
    """Схемы."""
    depot_id: int
    name: str
    address: str

    class Config:
        """Схемы."""
        from_attributes = True


# Route
class RouteCreate(BaseModel):
    """Схемы."""
    route_number: str
    type_id: int
    depot_id: int


class RouteOut(BaseModel):
    """Схемы."""
    route_id: int
    route_number: str
    type_id: int
    depot_id: int

    class Config:
        """Схемы."""
        from_attributes = True


# Stop
class StopCreate(BaseModel):
    """Схемы."""
    name: str


class StopOut(BaseModel):
    """Схемы."""
    stop_id: int
    name: str

    class Config:
        """Схемы."""
        from_attributes = True


# RouteStop
class RouteStopCreate(BaseModel):
    """Схемы."""
    route_id: int
    stop_id: int
    stop_order: int


class RouteStopOut(BaseModel):
    """Схемы."""
    route_id: int
    stop_id: int
    stop_order: int

    class Config:
        """Схемы."""
        from_attributes = True


# Driver
class DriverCreate(BaseModel):
    """Схемы."""
    full_name: str
    depot_id: int


class DriverOut(BaseModel):
    """Схемы."""
    driver_id: int
    full_name: str
    depot_id: int

    class Config:
        """Схемы."""
        from_attributes = True
