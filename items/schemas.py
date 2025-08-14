from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float
    description: str | None = None

class CreateItem(ItemBase):
    pass

class Item(ItemBase):
    id: int
    date_added: datetime

    class Config:
        orm_mode = True
