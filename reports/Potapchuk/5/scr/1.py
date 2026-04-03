from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

app = FastAPI(title="Rental of goods and services", version="0.1.0")


@app.get("/clients/", response_model=List[schemas.ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.post("/clients/", response_model=schemas.ClientResponse, status_code=201)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/{cl_id}", response_model=schemas.ClientResponse)
def get_client(cl_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.cl_id == cl_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client

@app.put("/clients/{cl_id}", response_model=schemas.ClientResponse)
def update_client(cl_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.cl_id == cl_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    for key, value in client.model_dump().items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.delete("/clients/{cl_id}")
def delete_client(cl_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.cl_id == cl_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    db.delete(db_client)
    db.commit()
    return {"detail": "Клиент успешно удалён"}


@app.get("/manufacturers/", response_model=List[schemas.ManufacturerResponse])
def get_manufacturers(db: Session = Depends(get_db)):
    return db.query(models.Manufacturer).all()

@app.post("/manufacturers/", response_model=schemas.ManufacturerResponse, status_code=201)
def create_manufacturer(man: schemas.ManufacturerCreate, db: Session = Depends(get_db)):
    db_man = models.Manufacturer(**man.model_dump())
    db.add(db_man)
    db.commit()
    db.refresh(db_man)
    return db_man

@app.get("/manufacturers/{man_id}", response_model=schemas.ManufacturerResponse)
def get_manufacturer(man_id: int, db: Session = Depends(get_db)):
    man = db.query(models.Manufacturer).filter(models.Manufacturer.man_id == man_id).first()
    if man is None:
        raise HTTPException(status_code=404, detail="Производитель не найден")
    return man

@app.put("/manufacturers/{man_id}", response_model=schemas.ManufacturerResponse)
def update_manufacturer(man_id: int, man: schemas.ManufacturerCreate, db: Session = Depends(get_db)):
    db_man = db.query(models.Manufacturer).filter(models.Manufacturer.man_id == man_id).first()
    if db_man is None:
        raise HTTPException(status_code=404, detail="Производитель не найден")
    for key, value in man.model_dump().items():
        setattr(db_man, key, value)
    db.commit()
    db.refresh(db_man)
    return db_man

@app.delete("/manufacturers/{man_id}")
def delete_manufacturer(man_id: int, db: Session = Depends(get_db)):
    db_man = db.query(models.Manufacturer).filter(models.Manufacturer.man_id == man_id).first()
    if db_man is None:
        raise HTTPException(status_code=404, detail="Производитель не найден")
    db.delete(db_man)
    db.commit()
    return {"detail": "Производитель успешно удалён"}


@app.get("/products/", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/products/", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{pr_id}", response_model=schemas.ProductResponse)
def get_product(pr_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.pr_id == pr_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.put("/products/{pr_id}", response_model=schemas.ProductResponse)
def update_product(pr_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.pr_id == pr_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{pr_id}")
def delete_product(pr_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.pr_id == pr_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(db_product)
    db.commit()
    return {"detail": "Товар успешно удалён"}


@app.get("/orders/", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@app.post("/orders/", response_model=schemas.OrderResponse, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{ord_id}", response_model=schemas.OrderResponse)
def get_order(ord_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.ord_id == ord_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@app.put("/orders/{ord_id}", response_model=schemas.OrderResponse)
def update_order(ord_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.ord_id == ord_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    for key, value in order.model_dump().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{ord_id}")
def delete_order(ord_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.ord_id == ord_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    db.delete(db_order)
    db.commit()
    return {"detail": "Заказ успешно удалён"}
