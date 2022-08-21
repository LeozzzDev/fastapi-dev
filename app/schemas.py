from datetime import datetime
from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True

class CreatePostRequest(BaseModel):
    title: str
    content: str
    published: bool = True

class UpdatePostRequest(BaseModel):
    title: str
    content: str
    published: bool = True

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUSerRequest(BaseModel):
    email: EmailStr
    password: str
