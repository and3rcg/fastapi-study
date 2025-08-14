from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal

from . import services
from . import schemas

items_router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@items_router.get("/")
def read_root():
    return {"Hello": "World"}

@items_router.post("/", response_model=schemas.Item)
def create_item(item: schemas.CreateItem, db: Session = Depends(get_db)):
    item = services.create_item(db, item)
    return item


@items_router.get("/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}
