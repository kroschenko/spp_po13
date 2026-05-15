from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Session, Category, Supplier, Product, Service, Order

app = FastAPI(title="Справочник товаров и услуг")


class CategoryCreate(BaseModel):
    name: str


class SupplierCreate(BaseModel):
    name: str
    phone: str
    address: str


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category_id: int
    supplier_id: int


@app.get("/")
def root():
    return {"message": "Справочник товаров и услуг"}


@app.get("/categories")
def get_categories():
    db = Session()
    result = db.query(Category).all()
    db.close()
    return result


@app.post("/categories")
def create_category(cat: CategoryCreate):
    db = Session()
    new = Category(name=cat.name)
    db.add(new)
    db.commit()
    db.refresh(new)
    db.close()
    return new


@app.get("/suppliers")
def get_suppliers():
    db = Session()
    result = db.query(Supplier).all()
    db.close()
    return result


@app.post("/suppliers")
def create_supplier(sup: SupplierCreate):
    db = Session()
    new = Supplier(name=sup.name, phone=sup.phone, address=sup.address)
    db.add(new)
    db.commit()
    db.refresh(new)
    db.close()
    return new


@app.get("/products")
def get_products():
    db = Session()
    result = db.query(Product).all()
    db.close()
    return result


@app.post("/products")
def create_product(prod: ProductCreate):
    db = Session()
    new = Product(
        name=prod.name, price=prod.price, stock=prod.stock, category_id=prod.category_id, supplier_id=prod.supplier_id
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    db.close()
    return new


@app.put("/products/{product_id}")
def update_product(product_id: int, prod: ProductCreate):
    db = Session()
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(404, "Товар не найден")
    p.name = prod.name
    p.price = prod.price
    p.stock = prod.stock
    p.category_id = prod.category_id
    p.supplier_id = prod.supplier_id
    db.commit()
    db.close()
    return p


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = Session()
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(404, "Товар не найден")
    db.delete(p)
    db.commit()
    db.close()
    return {"message": "Товар удален"}


@app.get("/services")
def get_services():
    db = Session()
    result = db.query(Service).all()
    db.close()
    return result


@app.get("/orders")
def get_orders():
    db = Session()
    result = db.query(Order).all()
    db.close()
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
