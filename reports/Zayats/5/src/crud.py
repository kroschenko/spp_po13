"""Crud"""
# pylint: disable=import-error
from sqlalchemy.orm import Session
import models
import schemas


# Depot
def create_depot(db: Session, data: schemas.DepotCreate):
    """Создать депо."""
    obj = models.Depot(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_depots(db: Session):
    """Получить все депо."""
    return db.query(models.Depot).all()


# Route
def create_route(db: Session, data: schemas.RouteCreate):
    """Создать маршрут."""
    obj = models.Route(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_routes(db: Session):
    """Получить маршруты."""
    return db.query(models.Route).all()


# Stop
def create_stop(db: Session, data: schemas.StopCreate):
    """Создать остановку."""
    obj = models.Stop(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_stops(db: Session):
    """Получить остановки."""
    return db.query(models.Stop).all()


# RouteStop
def create_route_stop(db: Session, data: schemas.RouteStopCreate):
    """Создать связь маршрут-остановка."""
    obj = models.RouteStop(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_route_stops(db: Session):
    """Получить связи."""
    return db.query(models.RouteStop).all()


# Driver
def create_driver(db: Session, data: schemas.DriverCreate):
    """Создать водителя."""
    obj = models.Driver(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_drivers(db: Session):
    """Получить водителей."""
    return db.query(models.Driver).all()
