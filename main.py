from fastapi import FastAPI

import models
from database import engine
from items.routes import items_router

# 1. Create an instance of the FastAPI class
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# 2. Include the items router
app.include_router(items_router)
