# pylint: disable=too-few-public-methods
"""Модели БД."""
# pylint: disable=import-error
from sqlalchemy import Column, Integer, String, ForeignKey


from database import Base


class Depot(Base):
    """Модели БД."""
    __tablename__ = "depots"

    depot_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)


class Route(Base):
    """Модели БД."""
    __tablename__ = "routes"

    route_id = Column(Integer, primary_key=True)
    route_number = Column(String(20), nullable=False)

    type_id = Column(Integer, ForeignKey("transport_types.type_id"))
    depot_id = Column(Integer, ForeignKey("depots.depot_id"))


class Stop(Base):
    """Модели БД."""
    __tablename__ = "stops"

    stop_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class RouteStop(Base):
    """Модели БД."""
    __tablename__ = "route_stops"

    route_id = Column(Integer, ForeignKey("routes.route_id"), primary_key=True)
    stop_id = Column(Integer, ForeignKey("stops.stop_id"), primary_key=True)
    stop_order = Column(Integer, nullable=False)


class Driver(Base):
    """Модели БД."""
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)

    depot_id = Column(Integer, ForeignKey("depots.depot_id"))
