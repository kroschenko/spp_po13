"""SQLAlchemy ORM models."""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    price_per_day = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

    category = relationship("Category", back_populates="items")
    rentals = relationship("Rental", back_populates="item")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)

    rentals = relationship("Rental", back_populates="customer")


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)

    rentals = relationship("Rental", back_populates="staff")


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    staff_id = Column(Integer, ForeignKey("staff.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, default="active")

    item = relationship("Item", back_populates="rentals")
    customer = relationship("Customer", back_populates="rentals")
    staff = relationship("Staff", back_populates="rentals")
