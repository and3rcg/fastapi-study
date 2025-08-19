from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None

    owner_id: int

class CreateItem(BaseModel):
    name: str
    price: float
    description: str | None = None

    owner_id: int

class UpdateItem(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

class Item(ItemBase):
    date_added: datetime

    model_config = ConfigDict(from_attributes=True)
