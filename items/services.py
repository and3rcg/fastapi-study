from sqlalchemy.orm import Session

from . import schemas
import models


def create_item(db: Session, item: schemas.CreateItem):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
