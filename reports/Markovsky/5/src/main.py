from datetime import date
from typing import Optional, List
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy_db import (
    add_manufacturer, get_all_manufacturers, update_manufacturer_country, delete_manufacturer,
    add_category,
    add_component, get_all_components, get_components_by_category,
    update_component_price, update_component_quantity, delete_component,
    add_build, get_build_details, delete_build,
    add_component_to_build
)

app = FastAPI(title="Компьютерная сборка API")


class ManufacturerCreate(BaseModel):
    name: str
    country: Optional[str] = None
    founded_year: Optional[int] = None


class ManufacturerResponse(ManufacturerCreate):
    id: int


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(CategoryCreate):
    id: int


class ComponentCreate(BaseModel):
    name: str
    price: float
    manufacturer_id: Optional[int] = None
    category_id: Optional[int] = None
    stock_quantity: int = 0


class ComponentResponse(ComponentCreate):
    id: int


class BuildCreate(BaseModel):
    name: str
    purpose: Optional[str] = None
    total_price: Optional[float] = None


class BuildResponse(BuildCreate):
    id: int
    build_date: date


class BuildComponentCreate(BaseModel):
    build_id: int
    component_id: int
    quantity: int = 1


class BuildComponentResponse(BuildComponentCreate):
    id: int


class BuildDetailResponse(BuildResponse):
    components: List[dict]


@app.post("/manufacturers/", response_model=ManufacturerResponse)
def create_manufacturer(manufacturer: ManufacturerCreate):
    try:
        new_manufacturer = add_manufacturer(
            name=manufacturer.name,
            country=manufacturer.country,
            founded_year=manufacturer.founded_year
        )
        return new_manufacturer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/manufacturers/", response_model=List[ManufacturerResponse])
def read_manufacturers():
    manufacturers = get_all_manufacturers()
    return manufacturers


@app.put("/manufacturers/{manufacturer_id}/country")
def update_manufacturer_country_endpoint(manufacturer_id: int, new_country: str):
    try:
        update_manufacturer_country(manufacturer_id, new_country)
        return {"message": "Страна производителя обновлена"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.delete("/manufacturers/{manufacturer_id}")
def delete_manufacturer_endpoint(manufacturer_id: int):
    try:
        delete_manufacturer(manufacturer_id)
        return {"message": "Производитель удален"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate):
    try:
        new_category = add_category(
            name=category.name,
            description=category.description
        )
        return new_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/components/", response_model=ComponentResponse)
def create_component(component: ComponentCreate):
    try:
        new_component = add_component(
            name=component.name,
            price=component.price,
            manufacturer_id=component.manufacturer_id,
            category_id=component.category_id,
            stock_quantity=component.stock_quantity
        )
        return new_component
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/components/", response_model=List[ComponentResponse])
def read_components():
    components = get_all_components()
    return components


@app.get("/components/category/{category_id}", response_model=List[ComponentResponse])
def read_components_by_category(category_id: int):
    components = get_components_by_category(category_id)
    return components


@app.put("/components/{component_id}/price")
def update_component_price_endpoint(component_id: int, new_price: float):
    try:
        update_component_price(component_id, new_price)
        return {"message": "Цена компонента обновлена"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.put("/components/{component_id}/quantity")
def update_component_quantity_endpoint(component_id: int, new_quantity: int):
    try:
        update_component_quantity(component_id, new_quantity)
        return {"message": "Количество компонента обновлено"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.delete("/components/{component_id}")
def delete_component_endpoint(component_id: int):
    try:
        delete_component(component_id)
        return {"message": "Компонент удален"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/builds/", response_model=BuildResponse)
def create_build(build: BuildCreate):
    try:
        new_build = add_build(
            name=build.name,
            purpose=build.purpose,
            total_price=build.total_price
        )
        return new_build
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/builds/{build_id}", response_model=BuildDetailResponse)
def read_build_details(build_id: int):
    build = get_build_details(build_id)
    if build:
        build_dict = {
            "id": build.id,
            "name": build.name,
            "build_date": build.build_date,
            "total_price": build.total_price,
            "purpose": build.purpose,
            "components": []
        }
        for bc in build.components:
            build_dict["components"].append({
                "component_id": bc.component.id,
                "component_name": bc.component.name,
                "quantity": bc.quantity,
                "price": bc.component.price
            })
        return build_dict
    raise HTTPException(status_code=404, detail="Сборка не найдена")


@app.delete("/builds/{build_id}")
def delete_build_endpoint(build_id: int):
    try:
        delete_build(build_id)
        return {"message": "Сборка удалена"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/build-components/", response_model=BuildComponentResponse)
def add_component_to_build_endpoint(bc: BuildComponentCreate):
    try:
        new_bc = add_component_to_build(
            build_id=bc.build_id,
            component_id=bc.component_id,
            quantity=bc.quantity
        )
        return new_bc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    #   http://127.0.0.1:8000/docs
    #   http://127.0.0.1:8000/redoc
