from sqlalchemy.orm import Session

from . import schemas
import models


def create_item(db: Session, item: schemas.CreateItem):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def list_items(db: Session, offset: int, limit: int = 100):
    db_items = db.query(models.Item).offset(offset).limit(limit).all()
    return db_items

def get_item(db: Session, id: int):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    return db_item

def update_item(db: Session, db_item: models.Item, item: schemas.UpdateItem):
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, db_item: models.Item):
    db.delete(db_item)
    db.commit()
