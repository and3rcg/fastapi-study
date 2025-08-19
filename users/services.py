from sqlalchemy.orm import Session

import models
from . import schemas


def get_user(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_username(username: str, db: Session):
    return db.query(models.User).filter(models.User.username == username).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def hash_password(password: str):
    return password + "this is not properly hashed!"

def create_user(request: schemas.UserCreate, db: Session):
    hashed_password = hash_password(request.password)
    user_data = request.model_dump()
    user_data.pop("password")
    user_obj = models.User(**user_data, hashed_password=hashed_password)
    setattr(user_obj, "hashed_password", hashed_password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def update_user_password(user: models.User, request: schemas.UserUpdatePassword, db: Session):
    hashed_password = hash_password(request.password)
    setattr(user, "hashed_password", hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(user: models.User, db: Session):
    db.delete(user)
    db.commit()
