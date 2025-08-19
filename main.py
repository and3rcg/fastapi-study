from fastapi import FastAPI

import models
from database import engine

from items.routes import items_router
from users.routes import users_router
from items.schemas import Item
from users.schemas import User

# 1. Create an instance of the FastAPI class
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# 2. Include the items router
app.include_router(items_router)
app.include_router(users_router)

Item.model_rebuild()
User.model_rebuild()
