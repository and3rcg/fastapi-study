from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float
    description: str | None = None

class CreateItem(ItemBase):
    pass

class UpdateItem(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

class Item(ItemBase):
    id: int
    date_added: datetime

    class Config:
        from_attributes = True
