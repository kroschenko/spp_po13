from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(20))
    address = Column(String(500))


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Integer, default=60)
    category_id = Column(Integer, ForeignKey("categories.id"))


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    total = Column(Float, default=0)
    status = Column(String(50), default="новый")
    customer_name = Column(String(200))


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


engine = create_engine("sqlite:///catalog.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def init_db():
    db = Session()

    if db.query(Category).count() == 0:
        db.add_all([Category(name="Электроника"), Category(name="Мебель"), Category(name="Услуги")])
        db.commit()

    if db.query(Supplier).count() == 0:
        db.add_all(
            [
                Supplier(name="ООО Поставка", phone="8-800-123-45-67", address="Москва"),
                Supplier(name="ИП Иванов", phone="8-912-345-67-89", address="СПб"),
            ]
        )
        db.commit()

    if db.query(Product).count() == 0:
        db.add_all(
            [
                Product(name="Ноутбук", price=50000, stock=10, category_id=1, supplier_id=1),
                Product(name="Телефон", price=30000, stock=20, category_id=1, supplier_id=1),
                Product(name="Стул", price=5000, stock=15, category_id=2, supplier_id=2),
                Product(name="Стол", price=10000, stock=5, category_id=2, supplier_id=2),
            ]
        )
        db.commit()

    if db.query(Service).count() == 0:
        db.add_all(
            [
                Service(name="Ремонт", price=2000, duration=60, category_id=3),
                Service(name="Доставка", price=500, duration=30, category_id=3),
            ]
        )
        db.commit()

    db.close()


init_db()
