"""Pydantic schemas for request/response validation."""

from datetime import date
from typing import Optional

from pydantic import BaseModel


# Category schemas
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        orm_mode = True


# Item schemas
class ItemCreate(BaseModel):
    name: str
    category_id: int
    price_per_day: float
    quantity: int


class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True


# Customer schemas
class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        orm_mode = True


# Staff schemas
class StaffCreate(BaseModel):
    name: str
    position: str


class StaffResponse(StaffCreate):
    id: int

    class Config:
        orm_mode = True


# Rental schemas
class RentalCreate(BaseModel):
    item_id: int
    customer_id: int
    staff_id: int
    start_date: date
    end_date: date
    status: str = "active"


class RentalResponse(RentalCreate):
    id: int

    class Config:
        orm_mode = True
