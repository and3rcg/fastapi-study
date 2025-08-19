from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import SessionLocal

from . import services
from . import schemas
import models

users_router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@users_router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = services.get_all_users(db)
    return users

@users_router.post("/", response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = services.create_user(request, db)
    except IntegrityError:
        raise HTTPException(400, detail="Username or email already taken")
    return user

@users_router.patch("/update_password/{user_id}", response_model=schemas.User)
def update_password(request: schemas.UserUpdatePassword, db: Session = Depends(get_db)):
    user = services.get_user_by_username(request.username, db)

    if user is None:
        raise HTTPException(404, detail="User not found")

    updated_user = services.update_user_password(user, request, db)
    return updated_user


@users_router.delete("/")
def delete_user(request: schemas.UserDelete, db: Session = Depends(get_db)):
    user = services.get_user_by_username(request.username, db)

    if user is None:
        raise HTTPException(404, detail="User not found")

    services.delete_user(user, db)
    return "User deleted successfully!"
