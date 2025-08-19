from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import SessionLocal

from . import services
from . import schemas as item_schemas

items_router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@items_router.post("/", response_model=item_schemas.Item)
def create_item(request: item_schemas.CreateItem, db: Session = Depends(get_db)):
    item = services.create_item(db, request)
    return item

@items_router.get("/", response_model=list[item_schemas.Item])
def list_items(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = services.list_items(db, offset, limit)
    return items

@items_router.get("/{item_id}", response_model=item_schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = services.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail = "Item not found")
    return item

@items_router.patch("/{item_id}", response_model=item_schemas.Item)
def update_item(item_id: int, request: item_schemas.UpdateItem, db: Session = Depends(get_db)):
    item = services.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail = "Item not found")
    item = services.update_item(db, item, request)
    return item

@items_router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = services.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail = "Item not found")
    services.delete_item(db, item)
    return "Deleted successfully"
