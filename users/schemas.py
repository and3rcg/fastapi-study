from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    email: str
    username: str

class UserUpdatePassword(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserDelete(BaseModel):
    username: str

class User(BaseModel):
    id: int
    email: str
    username: str

    model_config = ConfigDict(from_attributes=True)
